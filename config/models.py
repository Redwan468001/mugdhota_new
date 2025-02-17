from django.db import models
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


# Revision user
class RevisedBy(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    revised_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Revision Comments
class RevisedComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=355, blank=False)
    revised_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment