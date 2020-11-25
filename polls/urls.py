from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.QuizzesList.as_view(), name='quiz-list'),
    path('quizzes/<str:slug>/', views.QuizDetail.as_view(), name='quiz-detail'),
]