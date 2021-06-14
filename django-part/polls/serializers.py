from rest_framework import serializers
from django.db.models import Max
from .models import Quiz, Question, ChoiceAnswer, QuizQuestionAnswer, UserQuiz


class QuizSerializer(serializers.ModelSerializer):
    questions_info = serializers.SerializerMethodField()
    user_quiz_status = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'desc', 'slug', 'date_created', 'is_active', 'questions_info', 'user_quiz_status']
        read_only_fields = ['slug']
        extra_kwargs = {
            'is_active': {'write_only': True}
        }

    def get_questions_info(self, obj):
        result = {
            'count': obj.questions.count()
        }
        user = self.context['request'].user
        if not user.is_anonymous:
            try:
                user_quiz = UserQuiz.objects.get(user=user, quiz=obj)
                qqas = user_quiz.quizquestionanswer_set.all()
                if qqas.exists():
                    last_answered_question = qqas.aggregate(last_answered_question=Max('question__order'))['last_answered_question']
                    result['last_answered_question'] = last_answered_question
            except UserQuiz.DoesNotExist:
                return result
        return result

    def get_user_quiz_status(self, obj):
        user = self.context['request'].user
        if not user.is_anonymous:
            user_quiz = UserQuiz.objects.filter(user=user, quiz=obj)
            print(f'user quiz {user_quiz}')
            if user_quiz.exists():
                if user_quiz[0].is_completed:
                    return 'COMPLETED'
                else:
                    return 'STARTED'
            else:
                return 'NOT STARTED'
        else:
            return ''


class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()
    questions_info = serializers.SerializerMethodField()
    quiz = serializers.ReadOnlyField(source='quiz.title')

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'title', 'variant', 'choices', 'questions_info']
    
    def get_choices(self, obj):
        choices = obj.choices.all()
        choice_s = ChoiceSerializer(choices, many=True)
        return choice_s.data

    def get_questions_info(self, obj):
        result = {}
        print(f'context: {self.context}')
        user = self.context['request'].user
        questions_order = obj.quiz.questions.values_list('order')
        user_quiz = UserQuiz.objects.get(quiz=obj.quiz, user=user)
        answered_questions = user_quiz.quizquestionanswer_set.values_list('question__order').distinct()
        result.update(questions_order=[i[0] for i in questions_order], answered_questions=[i[0] for i in answered_questions])

        answer = [] # user's answer to this question
        qqas = user_quiz.quizquestionanswer_set.filter(question=obj)
        if obj.variant == 'T':
            for qqa in qqas:
                answer.append(qqa.users_answer.title)
        else:
            for qqa in qqas:
                answer.append(qqa.choice_answer.title)
        result['answer'] = answer
        return result


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