from functools import reduce
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max, F

from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,
                                    GenericAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from rest_framework import status

from .serializers import QuizSerializer, QuestionSerializer, QuizQuestionAnswerSerializer, UserQuizSerializer
from .models import Quiz, UserQuiz, QuizQuestionAnswer, Question, ChoiceAnswer, TextAnswer
from users.models import CustomUser
from rest_framework.response import Response


# Create your views here.
class QuizzesList(ListCreateAPIView):
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizSerializer


class QuizDetail(RetrieveUpdateDestroyAPIView):
    # TODO: author can update/delete the quize
    # TODO: display how many people took the quiz and etc...
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = 'slug'


class QuizResults(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserQuizSerializer
    queryset = UserQuiz.objects.all()

    def get_object(self):
        # return UserQuiz
        username = self.kwargs['username']
        user = get_object_or_404(CustomUser, username=username)

        quiz_slug = self.kwargs['quiz_slug']
        quiz = get_object_or_404(Quiz, slug=quiz_slug)

        userquiz = get_object_or_404(UserQuiz, user=user, quiz=quiz)

        if userquiz.is_completed:
            return userquiz
        else:
            raise NotFound('The user didn\'t take the quiz or hasn\'t finished it yet!')


class QuestionQuiz(GenericAPIView):
    ''' 
    This one is responsible for starting the quiz 
    And for fidning the next question the user needs to answer
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    lookup_field = 'slug'

    def get_next_question(self, user_quiz):
        # finding next question
        answered_questions = QuizQuestionAnswer.objects.filter(user_quiz=user_quiz)
        prev_question_order = answered_questions.aggregate(Max('question__order'))['question__order__max']
        print('order >> ', prev_question_order)
        try:
            next_question = user_quiz.quiz.questions.get(order=prev_question_order + 1)
        except TypeError:
            # user created quiz but never answered a single question
            next_question = user_quiz.quiz.questions.get(order=0)
        except Question.DoesNotExist:
            user_quiz.is_completed = True
            user_quiz.date_finished = timezone.now()
            user_quiz.save()
            next_question = {}

        return next_question

    def get(self, *args, **kwargs):
        user = self.request.user
        quiz = self.get_object()

        user_quiz, created = UserQuiz.objects.get_or_create(user=user, quiz=quiz)

        if user_quiz.is_completed:
            # TODO#2: display results
            return Response({"message": "You have already finished this quiz"}, 
                            status=status.HTTP_200_OK)

        next_question = None
        if created:
            # next question is the first one
            next_question = quiz.questions.get(order=0)
        else:
            next_question = self.get_next_question(user_quiz)
            if type(next_question) == dict:
                return Response(next_question, status=status.HTTP_200_OK)

        next_question_s = QuestionSerializer(next_question)
        return Response(next_question_s.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwrags):
        user = self.request.user
        quiz = self.get_object()
        user_quiz, created = UserQuiz.objects.get_or_create(user=user, quiz=quiz)
        try:
            question_id = self.request.data['question_id']
            question = quiz.questions.get(id=question_id)
            if QuizQuestionAnswer.objects.filter(question=question, user_quiz=user_quiz).exists():
                return Response({"error": "You have already answered this question!"})

            if question.variant == 'SS':
                choice_id = self.request.data['choice_id']
                choice_answer = question.choices.get(id=choice_id)
                if choice_answer.is_correct:
                    user_quiz.score = F('score') + 1
                QuizQuestionAnswer.objects.create(question=question, choice_answer=choice_answer, 
                                                  user_quiz=user_quiz)
            elif question.variant == 'MS':
                choices_ids = self.request.data['choices_ids']
                print(choices_ids)
                correct_answers = 0
                for choice_id in choices_ids:
                    choice_answer = question.choices.get(id=choice_id)
                    if choice_answer.is_correct:
                        correct_answers += 1
                    QuizQuestionAnswer.objects.create(question=question, choice_answer=choice_answer, 
                                                      user_quiz=user_quiz)
                if len(choices_ids) == correct_answers:
                    user_quiz.score = F('score') + 1

            elif question.variant == 'T':
                answer = self.request.data['answer']
                if question.correct_answer.lower() == answer.lower():
                    user_quiz.score = F('score') + 1
                users_answer = TextAnswer.objects.create(question=question, title=answer)
                QuizQuestionAnswer.objects.create(question=question, users_answer=users_answer, 
                                                  user_quiz=user_quiz)
            user_quiz.save()
            user_quiz.refresh_from_db()
        except KeyError:
            return Response({"error": "Question or Answer were not provided!"},
                        status=status.HTTP_400_BAD_REQUEST)
        except (Question.DoesNotExist, ChoiceAnswer.DoesNotExist):
            return Response({"error": "Incorrect data!"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            print(exc)
            return Response({"error": "Something went wrong!"})
                            
        next_question = self.get_next_question(user_quiz)
        if type(next_question) == dict:
            # TODO: user answered all the questions => redirect to result page
            # OR display a 'submit' button when there's an option to change the
            # answers
            username = user.username
            slug = quiz.slug
            return redirect(f'/api/{username}/{slug}/results/')
        next_question_s = QuestionSerializer(next_question)
        
        return Response(next_question_s.data, status=status.HTTP_201_CREATED)

