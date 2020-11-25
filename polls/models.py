from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class QuestionVariant(models.TextChoices):
    SINGLE = "SS", "Single Selection",
    MULTIPLE = "MS", "Multiple Selection",
    TEXT = "T", "Text Answer",

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    is_active = models.BooleanField()
    slug = models.SlugField(blank=True)
    image = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField(User, related_name='quizes', through='UserQuiz')

    def save(self, *args, **kwargs):
        slugified_title = slugify(self.title)
        self.slug = slugified_title
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['date_created']
    
    def __str__(self):
        return self.title
    

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    variant = models.CharField(choices=QuestionVariant.choices, max_length=2)
    order = models.IntegerField(default=0)
    # only if vatiant is T
    correct_answer = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(variant__in=QuestionVariant.values), name="%(app_label)s_%(class)s_variant_valid")
        ]

    def __str__(self):
        return self.title


class ChoiceAnswer(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        variant = self.question.variant
        if variant == 'MS' or variant == 'SS':
            super().save(*args, **kwargs)
        else: 
            return "You can't create option for text-answer-required question!"

    def __str__(self):
        return self.title

class TextAnswer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    title = models.TextField()

    def save(self, *args, **kwargs):
        variant = self.question.variant
        if variant == 'T':
            super().save(*args, **kwargs)
        else: 
            return "You can't create text answer for forced-choice question!"

    def __str__(self):
        return self.title

class UserQuiz(models.Model):
    '''
    to store who takes what quiz and when that who started it
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    date_started = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        representation = f'{self.user.username } took {self.quiz.title}'
        return representation


class QuizQuestionAnswer(models.Model):
    '''
    to store exact answers users gave to the specific questions
    '''
    user_quiz = models.ForeignKey(UserQuiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # only if question variant == "SS" or "MS"
    choice_answer = models.ForeignKey(ChoiceAnswer, on_delete=models.CASCADE, null=True, blank=True)
    # only if question variant == "T"
    users_answer = models.ForeignKey(TextAnswer, on_delete=models.CASCADE, null=True, blank=True)