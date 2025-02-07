from django.shortcuts import render, get_object_or_404
from . models import ArtAndLiterature
from . models import Category

# Create your views here.
def artandliterature(request):
    posts = ArtAndLiterature.objects.all()
    title = 'Art And Literature'
    categories = []
    for post in posts:
        if post.category not in categories:
            categories.append(post.category)

    context = {
        'posts': posts,
        'categories': categories,
        'title': title,
    }

    return render(request, 'page.html', context)


# Single post
def single_post(request, slug):
    post = get_object_or_404(ArtAndLiterature, slug=slug)
    context = {
        'post': post,
    }
    return render(request, 'single.html', context)



# Category wise content
def singlecategory(request, category):
    category_obj = get_object_or_404(Category, name=category)
    posts = ArtAndLiterature.objects.filter(category=category_obj)
    all_posts = ArtAndLiterature.objects.all()
    categories = []
    for post in all_posts:
        if post.category not in categories:
            categories.append(post.category)

    context = {
        'category_obj': category_obj,
        'posts': posts,
        'categories': categories,
    }

    return render(request, 'page.html', context)