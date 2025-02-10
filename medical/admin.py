from django.contrib import admin
from . models import MedicalInsight, Category

# Register your models here.
admin.site.register(MedicalInsight)
admin.site.register(Category)