from rest_framework import serializers
from .models import Quiz, Question, ChoiceAnswer, QuizQuestionAnswer, UserQuiz


class QuizSerializer(serializers.ModelSerializer):
    number_of_questions = serializers.SerializerMethodField()
    user_quiz_status = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'desc', 'slug', 'date_created', 'is_active', 'number_of_questions', 'user_quiz_status']
        read_only_fields = ['slug']
        extra_kwargs = {
            'is_active': {'write_only': True}
        }

    def get_number_of_questions(self, obj):
        return obj.questions.count()

    def get_user_quiz_status(self, obj):
        user = self.context['request'].user
        user_quiz = UserQuiz.objects.filter(user=user, quiz=obj)
        if user_quiz.exists():
            if user_quiz[0].is_completed:
                return 'COMPLETED'
            else:
                return 'STARTED'
        else:
            return 'NOT STARTED'


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
        if question.variant == "SS" or question.variant == "MS":
            users_answer = obj.choice_answer.title
            is_correct = obj.choice_answer.is_correct

            correct_answers = question.choices.filter(is_correct=True)

            return {"users_answer": users_answer, "is_correct": is_correct, 
                    "correct_answer": correct_answer}
        elif question.variant == 'T':
            question.correct_answer 


class UserQuizSerializer(serializers.ModelSerializer):
    '''
    Maybe you can display results here
    '''
    results = serializers.SerializerMethodField()

    def get_results(self, user_quiz):
        results = {}
        questions = user_quiz.quiz.questions.all()
        for question in questions:
            question_title = question.title
            if question.variant == 'T':
                correct_answers_list = [question.correct_answer]
                user_answers_list = [QuizQuestionAnswer.objects.get(user_quiz=user_quiz, question=question).users_answer.title]
            else:
                correct_answers = question.choices.filter(is_correct=True)
                correct_answers_list = list(map(lambda el: el.title, correct_answers))
                user_answers = QuizQuestionAnswer.objects.filter(user_quiz=user_quiz, question=question)
                user_answers_list = list(map(lambda el: el.choice_answer.title, user_answers))
                
            results[question_title] = {
                'user_answers': user_answers_list,
                'correct_answers': correct_answers_list
            }
        return results

    class Meta:
        model = UserQuiz
        fields = ['score', 'results', 'date_started', 'date_finished']