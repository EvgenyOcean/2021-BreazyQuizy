from rest_framework import serializers
from .models import Quiz


class QuizSerializer(serializers.ModelSerializer):
    number_of_questions = serializers.SerializerMethodField()
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'desc', 'slug', 'date_created', 'is_active', 'number_of_questions']
        read_only_fields = ['slug']
        extra_kwargs = {
            'is_active': {'write_only': True}
        }

    def get_number_of_questions(self, obj):
        return obj.questions.count()