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
            # finding next question 
            answered_questions = QuizQuestionAnswer.objects.filter(user_quiz=user_quiz)
            prev_question_order = answered_questions.aggregate(Max('question__order'))['question__order__max']
            try:
                next_question = quiz.questions.get(order=prev_question_order + 1)
            except Question.DoesNotExist:
                # user answered the last question
                results = QuizQuestionAnswerSerializer(answered_questions, many=True).data
                score = reduce(lambda count, result: count+1 if result['users_answer']['is_correct'] else count, results, 0)
                user_quiz.is_completed = True
                user_quiz.date_finished = timezone.now()
                user_quiz.score = score
                user_quiz.save()
                return Response({"questions_info": results, "score": score}, status=status.HTTP_200_OK)

        next_question_s = QuestionSerializer(next_question)
        return Response(next_question_s.data, status=status.HTTP_200_OK)