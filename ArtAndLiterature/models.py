from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from config.models import ContentStatus, Tag
from User.models import User
from config.models import RevisedBy, RevisedComment


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to='category_img', blank=True, null=True)

    def __str__(self):
        return self.name


class ArtAndLiterature(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=False)
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
    reviewed_comments = models.ForeignKey(RevisedComment, on_delete=models.CASCADE, blank=True, null=True)

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

