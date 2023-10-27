from django.contrib import admin
from users.models import Users

# Register your models here.

# class AuthorAdmin(admin.ModelAdmin):
#     pass

admin.site.register(Users)
