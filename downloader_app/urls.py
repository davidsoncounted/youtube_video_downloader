from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video-converter', views.video_converter, name='video-converter'),
]