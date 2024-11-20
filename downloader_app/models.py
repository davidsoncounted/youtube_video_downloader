from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.URLField()
    video_url = models.URLField()