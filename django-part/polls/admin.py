import nested_admin
from django.contrib import admin
from .models import Quiz, Question, ChoiceAnswer, UserQuiz, QuizQuestionAnswer

#######################
# NESTED ADMIN FOR CREATING NEW QUIZES/QUESTIONS/CHOICES
#######################

# choices
class ChoiceAnswerInline(nested_admin.NestedTabularInline):
    model = ChoiceAnswer
    extra = 3


# this one will contain choices for the quesion
class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    extra = 3
    inlines = [ChoiceAnswerInline]


# this one will be the main wrapper wrapper
class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]


#######################
# CONTRIB.ADMIN FOR USER-QUIZ AND QUIZ-QUESTION-ANSWER
#######################

class QuizQuestionAnswerInline(admin.StackedInline):
    model = QuizQuestionAnswer
    extra = 3


class UserQuizAdmin(admin.ModelAdmin):
    inlines = [QuizQuestionAnswerInline]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(ChoiceAnswer)
admin.site.register(UserQuiz, UserQuizAdmin)
admin.site.register(QuizQuestionAnswer)