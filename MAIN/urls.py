from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home' ),
    path('forum/',views.forum,name='forum' ),
    path('policy/',views.policy,name='policy' ),
    path('send_comment/',views.send_comment,name='send_comment' ),
]