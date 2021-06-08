from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.QuizzesList.as_view(), name='quiz-list'),
    path('quizzes/<str:slug>/', views.QuizDetail.as_view(), name='quiz-detail'),
    path('quizzes/<str:slug>/<int:order>/', views.QuizQuestion.as_view(), name='quiz-question'),
    path('quizzes/<str:slug>/results/', views.QuizResults.as_view(), name='quiz-results'),
]