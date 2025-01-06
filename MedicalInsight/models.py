from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to='category_img', blank=True, null=True)

    def __str__(self):
        return self.name
    

# Medical Science 
class MedicalScience(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=False)
    title = models.CharField(max_length=255, blank=False)
    content = RichTextUploadingField()
    feature_image = models.ImageField(upload_to='medical_image', blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title