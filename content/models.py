from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from User.models import User


# Create your models here.

class ContentStatus(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


# Tag
class Tag(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


# Category
class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to='category_img', blank=True, null=True)

    def __str__(self):
        return self.name


# Sub Category
class SubCategory(models.Model):
    name = models.CharField(max_length=255, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    image = models.ImageField(upload_to='category_img', blank=True, null=True)

    def __str__(self):
        return self.name


# Content Part
class Content(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=False)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, blank=False)
    title = models.CharField(max_length=255, blank=False)
    slug = models.CharField(max_length=255, unique=True, blank=True, null=True)
    author = models.CharField(max_length=255, default="Mugdhota", blank=False)
    content = RichTextUploadingField()
    feature_image = models.ImageField(upload_to='medical_image', blank=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    approved_by = models.CharField(max_length=255, default="Mugdhota")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=1)
    status = models.ForeignKey(ContentStatus, on_delete=models.CASCADE, blank=True, null=True, default=2)
    tags = models.ManyToManyField(Tag, blank=True)
    reviewed_by = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.author}"


# Revision Comments
class ReviewedComment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='reviewed_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=355, blank=False)
    reviewd_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment



# Comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.PROTECT)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

