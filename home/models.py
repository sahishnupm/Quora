from django.db import models
from users.models import Users

# Create your models here.

class Question(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    updated_by = models.DateTimeField()

    class Meta:
        db_table = 'questions'


class QuestionDetails(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    responds = models.CharField(max_length=255)
    respondand_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    responds_time = models.DateField()

    class Meta:
        db_table = 'question_details'


class Likes(models.Model):
    question_id = models.ForeignKey(QuestionDetails, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(Users, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'