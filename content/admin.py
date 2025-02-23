from django.contrib import admin
from . models import Category, SubCategory, Tag, Content, ReviewedComment, ContentStatus

# Register your models here.
class ReviewedCommentTabular(admin.TabularInline):
    model = ReviewedComment
    extra = 1


class ContentAdmin(admin.ModelAdmin):
    inlines = [ReviewedCommentTabular]
    list_display = ('title', 'author', 'writer', 'create_at', 'status')


admin.site.register(Content, ContentAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Tag)
admin.site.register(ReviewedComment)
admin.site.register(ContentStatus)
