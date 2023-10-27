from django.urls import path
from home import views

urlpatterns = [
    path('', views.Dashboard.as_view()),
    path('post', views.PostQuestion.as_view()),
    path('add-reply', views.AddReply.as_view()),
    path('toggle-like', views.ToggleLike.as_view()),
]