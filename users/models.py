from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    image_text = models.CharField(max_length=200)
    image = models.ImageField(upload_to="storage/")
    OCRtext = models.CharField(max_length=500, default="No text extracted")
