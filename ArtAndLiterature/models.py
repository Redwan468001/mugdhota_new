from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
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
    slug = models.SlugField(unique=True, blank=True, null=True)
    author = models.CharField(max_length=255, default="Mugdhota", blank=False)
    content = RichTextUploadingField()
    feature_image = models.ImageField(upload_to='medical_image', blank=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    approved_by = models.CharField(max_length=255, default="Mugdhota")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it doesn't exist
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while ArtAndLiterature.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug  # Assign unique slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.author}"
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(ArtAndLiterature, on_delete=models.PROTECT)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    
