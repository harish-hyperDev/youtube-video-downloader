from django.db import models
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class Video(models.Model):
    title = models.CharField(max_length=150)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    
    def __str__(self):
        return self.title