import os

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class NeuralModel(models.Model):
    model_name = models.FileField(upload_to='models/%Y/%m/%d')
    model_type = models.CharField(null=False, max_length=50)
    uploaded_at = models.DateTimeField(null=False, auto_now_add=True)
    
    def delete(self, *args, **kwargs):
        self.model_name.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.model_type


class ImageManager(models.Model):
    file_name = models.ImageField(upload_to='images/%Y/%m/%d')
    uploaded_at = models.DateTimeField(null=False, auto_now_add=True)
    predicted = models.BooleanField(default=False)
    model_prediction = models.CharField(null=True, max_length=25)
    accuracy = models.FloatField(null=True, blank=True)
    info_from_user = models.CharField(null=True, max_length=25)
    session_key = models.CharField(max_length=150, null=True, blank=True)
    model_type = models.ForeignKey(NeuralModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def delete(self, *args, **kwargs):
        self.file_name.delete()
        super().delete(*args, **kwargs)
    
    def filename(self):
        return os.path.basename(self.file_name.name)

    def absolute_path(self):
        return f'media/{self.file_name}'

    def __str__(self):
        return self.file_name.name
    