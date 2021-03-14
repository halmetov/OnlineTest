from django.db import models
from datetime import datetime

# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=300)
    logo = models.ImageField(upload_to='upload', blank=True)
    status = models.IntegerField(default=0, blank=True)
    rating = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title

class Class(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Test(models.Model):
    title = models.CharField(max_length=300, blank=True, default="")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    clas = models.ForeignKey(Class, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    limit = models.IntegerField(default=40)
    description = models.TextField()

    def __str__(self):
        return f'{self.subject} {self.clas} {self.title}'



class TestItem(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.TextField()
    answer_1 = models.TextField()
    answer_2 = models.TextField()
    answer_3 = models.TextField()
    answer_4 = models.TextField()
    answer_5 = models.TextField()
    correct_answer = models.IntegerField()

    def __str__(self):
        return str(self.id) + ' ' + self.question

class User(models.Model):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    clas = models.ForeignKey(Class, on_delete=models.CASCADE)
    ball = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class UserTestItem(models.Model):
    title = models.CharField(max_length=200, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField()
    ball = models.IntegerField(default=0)
    count_question = models.IntegerField(default=0)
    true_question = models.IntegerField(default=0)
    questions = models.CharField(max_length=300, default='', blank=True)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}  {self.test.title} {self.id}'


class UserTestItemVariant(models.Model):
    user_test_item = models.ForeignKey(UserTestItem, on_delete=models.CASCADE)
    test_item = models.ForeignKey(TestItem, on_delete=models.CASCADE)
    user_variant = models.IntegerField(default=0)
    correct_variant = models.IntegerField(default=0)
    ball = models.IntegerField(default=0)


    def __str__(self):
        return self.user_test_item.user.last_name + ' ' + str(self.test_item.id)






class SurveyCategory(models.Model):
    title = models.CharField(max_length=300, blank=True)
    icon = models.CharField(max_length=300, blank=True)
    status = models.IntegerField(default=0, blank=True)
    rating = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title


class Survey(models.Model):
    title = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to='upload', blank=True)
    category = models.ForeignKey(SurveyCategory, on_delete=models.CASCADE)
    date = models.DateTimeField()
    mini_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(max_length=600, blank=True)
    rating = models.IntegerField(default=0, blank=True)
    status = models.IntegerField(default=0, blank=True)
    view = models.IntegerField(default=0)

    def __str__(self):
        return  self.title

class Question(models.Model):
    CHOISE = (
        ('single', 'Можно выбрать один ответ'),
        ('multi', 'Можно выбрать много ответов')
    )
    question_type = models.CharField(max_length=6, choices=CHOISE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to='upload', blank=True)
    var1 = models.CharField(max_length=300, blank=True)
    var2 = models.CharField(max_length=300, blank=True)
    var3 = models.CharField(max_length=300, blank=True)
    var4 = models.CharField(max_length=300, blank=True)
    var5 = models.CharField(max_length=300, blank=True)
    var6 = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'{self.question_type} {self.survey.title}'

class UserSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_item = models.ForeignKey(Survey, on_delete=models.CASCADE)
    date = models.DateTimeField()
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}  {self.survey_item.title} {self.id}'


class UserSurveyItem(models.Model):
    user_survey = models.ForeignKey(UserSurvey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choosen_variant = models.CharField(max_length=300)
    date = models.DateTimeField()

    def __str__(self):
        return self.user_survey.user.last_name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(blank=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0, blank=True)
    status = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.user.user.last_name

