from django.shortcuts import render
from . models import ArtAndLiterature

# Create your views here.
def artandliterature(request):
    posts = ArtAndLiterature.objects.all()

    context = {
        'posts': posts,
    }

    return render(request, 'index.html', context)

