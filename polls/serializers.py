from rest_framework import serializers
from .models import Quiz


    # title = models.CharField(max_length=100)
    # desc = models.CharField(max_length=500)
    # is_active = models.BooleanField()
    # slug = models.SlugField()
    # image = models.ImageField()
    # date_created = models.DateTimeField(auto_now_add=True)
    # user = models.ManyToManyField(User, related_name='quizes', through='UserQuiz')

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['title', 'desc', 'slug', 'date_created', 'is_active']
        read_only_fields = ['slug']
        extra_kwargs = {
            'is_active': {'write_only': True}
        }