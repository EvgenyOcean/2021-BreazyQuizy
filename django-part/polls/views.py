from functools import reduce
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max, F

from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,
                                    GenericAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from rest_framework import status

from .serializers import QuizSerializer, QuestionSerializer, UserQuizSerializer
from .models import Quiz, UserQuiz, QuizQuestionAnswer, Question, ChoiceAnswer, TextAnswer
from users.models import CustomUser
from rest_framework.response import Response


# Create your views here.
class QuizzesList(ListCreateAPIView):
    '''
    Lists all the available quizzes
    '''
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizSerializer


class QuizDetail(RetrieveUpdateDestroyAPIView):
    '''
    Displays quiz description, title, how many people took the quiz, average score
    Allows a quiz author to update, delete his quiz
    '''
    # TODO: author can update/delete the quize
    # TODO: display how many people took the quiz and etc...
    permission_classes = [AllowAny]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = 'slug'


class QuizResults(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserQuizSerializer
    queryset = UserQuiz.objects.all()

    def get_object(self):
        # return UserQuiz
        username = self.request.user.username
        user = get_object_or_404(CustomUser, username=username)
        quiz_slug = self.kwargs['slug']
        quiz = get_object_or_404(Quiz, slug=quiz_slug)
        userquiz = get_object_or_404(UserQuiz, user=user, quiz=quiz)

        if userquiz.is_completed:
            return userquiz
        else:
            raise NotFound('You haven\'t completed the quiz yet!')


class QuizQuestion(GenericAPIView):
    ''' 
    Starts the quiz, displays questions, accepts answers
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        quiz = self.get_object()
        questions = quiz.questions
        current_question = questions.filter(order=kwargs['order'])
        print(f'>>> {current_question}')
        if current_question.exists():
            user_quiz, created = UserQuiz.objects.get_or_create(user=user, quiz=quiz)
            serializer = QuestionSerializer(current_question[0], context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User answered the last question"}, status=status.HTTP_200_OK) 

    def post(self, request, *args, **kwargs):
        user = self.request.user
        quiz = self.get_object()
        questions = quiz.questions
        user_quiz, created = UserQuiz.objects.get_or_create(user=user, quiz=quiz)
        if user_quiz.is_completed:
            return Response({"message": "You have already finished this quiz"}, 
                            status=status.HTTP_200_OK)
        is_submitted = request.data.get('submitted')
        if is_submitted:
            score = 0
            user_quiz.is_completed = True
            user_quiz.date_finished = timezone.now()
            serializer = UserQuizSerializer(user_quiz)
            data = serializer.data
            for question, answers in data['results'].items():
                if set(answers['user_answers']) == set(answers['correct_answers']):
                    score += 1
            user_quiz.score = score
            user_quiz.save()
            return redirect(f'/api/quizzes/{kwargs["slug"]}/results/')

        try:
            question = quiz.questions.get(order=kwargs['order'])
        except Question.DoesNotExist:
            return Response({"message": "User answered the last question"}, status=status.HTTP_201_CREATED)

        try:
            qqa = QuizQuestionAnswer.objects.filter(question=question, user_quiz=user_quiz)
            if qqa.exists():
                qqa.delete()

            if question.variant == 'SS':
                choice_id = self.request.data['choice_id']
                choice_answer = question.choices.get(id=choice_id)
                QuizQuestionAnswer.objects.create(question=question, choice_answer=choice_answer, 
                                                  user_quiz=user_quiz)
            elif question.variant == 'MS':
                choices_ids = self.request.data['choices_ids']
                for choice_id in choices_ids:
                    choice_answer = question.choices.get(id=choice_id)
                    QuizQuestionAnswer.objects.create(question=question, choice_answer=choice_answer, 
                                                      user_quiz=user_quiz)
            elif question.variant == 'T':
                answer = self.request.data['answer']
                users_answer = TextAnswer.objects.create(question=question, title=answer)
                QuizQuestionAnswer.objects.create(question=question, users_answer=users_answer, 
                                                  user_quiz=user_quiz)
        except KeyError:
            return Response({"error": "Question or Answer were not provided!"},
                        status=status.HTTP_400_BAD_REQUEST)
        except (Question.DoesNotExist, ChoiceAnswer.DoesNotExist):
            return Response({"error": "Incorrect data!"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            print(exc)
            return Response({"error": "Something went wrong!"})
                                    
        return Response(status=status.HTTP_201_CREATED)