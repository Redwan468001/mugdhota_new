from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from User.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to='category_img', blank=True, null=True)

    def __str__(self):
        return self.name
    

class ArtAndLiterature(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=False)
    title = models.CharField(max_length=255, blank=False)
    content = RichTextUploadingField()
    feature_image = models.ImageField(upload_to='medical_image', blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(ArtAndLiterature, on_delete=models.PROTECT)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    
