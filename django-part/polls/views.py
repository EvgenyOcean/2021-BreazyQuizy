from django.shortcuts import render, get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import QuizSerializer
from .models import Quiz


# Create your views here.
class QuizzesList(ListCreateAPIView):
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizSerializer

class QuizDetail(RetrieveUpdateDestroyAPIView):
    # TODO: set permissions
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = 'slug'
