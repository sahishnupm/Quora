from django.contrib import admin
from home.models import Question, QuestionDetails, Likes

# Register your models here.

admin.site.register(Question)
admin.site.register(QuestionDetails)
admin.site.register(Likes)