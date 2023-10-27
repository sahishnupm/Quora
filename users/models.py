from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)




# from mongoengine import Document, StringField

# class Users(Document):
#     username = StringField(required=True, max_length=15)
#     password = StringField(required=True)

# class UsersDao():

#     def get(self,name):
#         return Users.objects(name=name).first()
    
#     def post(self,username,password):
#         return Users.objects(username=username,password=password).first()
    
# users_dao = UsersDao()