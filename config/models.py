from django.db import models

# Create your models here.
class ContentStatus(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name