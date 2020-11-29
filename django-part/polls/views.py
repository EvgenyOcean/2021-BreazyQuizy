from functools import reduce
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.db.models import Max 

from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,
                                    GenericAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .serializers import QuizSerializer, QuestionSerializer, QuizQuestionAnswerSerializer
from .models import Quiz, UserQuiz, QuizQuestionAnswer, Question
from rest_framework.response import Response


# Create your views here.
class QuizzesList(ListCreateAPIView):
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizSerializer


class QuizDetail(RetrieveUpdateDestroyAPIView):
    # TODO#3: set permissions, only author can manipulate the quiz
    # TODO#4: if this quiz has been completed by the user => display his results
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = 'slug'


class QuestionQuiz(GenericAPIView):
    ''' 
    This one is responsible for starting the quiz 
    And for fidning the next question the user needs to answer
    '''
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    lookup_field = 'slug'

    def get_next_question(self, user_quiz):
        # finding next question
        answered_questions = QuizQuestionAnswer.objects.filter(user_quiz=user_quiz)
        prev_question_order = answered_questions.aggregate(Max('question__order'))['question__order__max']
        try:
            next_question = user_quiz.quiz.questions.get(order=prev_question_order + 1)
        except TypeError:
            # user created quiz but never answered a single question
            next_question = user_quiz.quiz.questions.get(order=0)
        except Question.DoesNotExist:
            # user answered the last question
            results = QuizQuestionAnswerSerializer(answered_questions, many=True).data
            score = reduce(lambda count, result: count+1 if result['users_answer']['is_correct'] else count, results, 0)
            user_quiz.is_completed = True
            user_quiz.date_finished = timezone.now()
            user_quiz.score = score
            user_quiz.save()
            next_question = {"questions_info": results, "score": score}
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
            choice_id = self.request.data['choice_id']
        except KeyError:
            return Response({"error": "Question or Answer were not provided!"},
                        status=status.HTTP_400_BAD_REQUEST)
        
        try:
            question = quiz.questions.get(id=question_id)
            choice_answer = question.choices.get(id=choice_id)
        except Exception:
            return Response({"error": "This question or choice doesn't belog!"},
                            status=status.HTTP_400_BAD_REQUEST)
                            
        if QuizQuestionAnswer.objects.filter(question=question, user_quiz=user_quiz).exists():
            return Response({"error": "You have already answered this question!"})

        QuizQuestionAnswer.objects.create(question=question, choice_answer=choice_answer, 
                                        user_quiz=user_quiz)
        next_question = self.get_next_question(user_quiz)
        if type(next_question) == dict:
            return Response(next_question, status=status.HTTP_200_OK)
        next_question_s = QuestionSerializer(next_question)
        
        return Response(next_question_s.data, status=status.HTTP_201_CREATED)

