from rest_framework import serializers
from .models import Quiz, Question, ChoiceAnswer, QuizQuestionAnswer


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


class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()
    quiz = serializers.ReadOnlyField(source='quiz.title')

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'title', 'variant', 'choices']
    
    def get_choices(self, obj):
        choices = obj.choices.all()
        choice_s = ChoiceSerializer(choices, many=True)
        return choice_s.data


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ChoiceAnswer
        fields = ['id', 'title']


class QuizQuestionAnswerSerializer(serializers.ModelSerializer):
    question = serializers.ReadOnlyField(source='question.title')
    users_answer = serializers.SerializerMethodField()

    class Meta:
        model = QuizQuestionAnswer
        fields = ['question', 'users_answer']

    def get_users_answer(self, obj):
        question = obj.question
        if question.variant == "SS":
            users_answer = obj.choice_answer.title
            is_correct = obj.choice_answer.is_correct
            correct_answer = question.choices.get(is_correct=True).title
            return {"users_answer": users_answer, "is_correct": is_correct, 
                    "correct_answer": correct_answer}

