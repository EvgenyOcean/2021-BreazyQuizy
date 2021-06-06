from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.QuizzesList.as_view(), name='quiz-list'),
    path('quizzes/<str:slug>/', views.QuizDetail.as_view(), name='quiz-detail'),
    path('quizzes/<str:slug>/test/', views.QuestionQuiz.as_view(), name='question-quiz'),
    path('<str:username>/<str:quiz_slug>/results/', views.QuizResults.as_view(), name='quiz-results'),
]