from django.shortcuts import render, redirect
from ArtAndLiterature.models import ArtAndLiterature

# Create your views here.
def home(request):
    posts = ArtAndLiterature.objects.all().order_by('-create_at')
    stories = []
    novels = []
    for post in posts:
        if post.category.name == 'Novel':
            novels.append(post)
        elif post.category.name == 'Story':
            stories.append(post)

    context = {
        'posts': posts,
        'novels': novels,
        'stories': stories,
    }
    return render(request, 'index.html', context)
