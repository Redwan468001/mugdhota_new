from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    title = 'Test run'
    context = {
        'title': title,
    }
    return render(request, 'index.html', context)
