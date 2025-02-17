from django.contrib import admin
from . models import ContentStatus, Tag, RevisedBy, RevisedComment

# Register your models here.
admin.site.register(ContentStatus)
admin.site.register(Tag)
admin.site.register(RevisedBy)
admin.site.register(RevisedComment)
