from django.shortcuts import render, redirect, get_object_or_404
from . models import MedicalInsight, Category
from config.models import ContentStatus
from . forms import MediUploadForm
from django.utils.timezone import now
from datetime import datetime, timedelta

# Create your views here.

def medicalinsight(request):
    posts = MedicalInsight.objects.all()
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

# Get Ip Address
def get_client_ip(request):
    """Get the client IP address from request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Single post
def single_post(request, slug):
    post = get_object_or_404(MedicalInsight, slug=slug)

    client_ip = get_client_ip(request)  # Get user's IP address
    session_key = f'viewed_post_{post.id}_{client_ip}'  # Unique session key

    # Retrieve last view time and convert it back to datetime
    last_view_time_str = request.session.get(session_key)
    last_view_time = None
    if last_view_time_str:
        try:
            last_view_time = datetime.fromisoformat(last_view_time_str)  # Convert from string
        except ValueError:
            last_view_time = None  # If the format is incorrect, reset it

    # Check if the post was viewed from this IP in the last 10 minutes
    if not last_view_time or now() - timedelta(minutes=10) > last_view_time:
        post.views += 1
        post.save(update_fields=['views'])  # Save only the 'views' field
        request.session[session_key] = now().isoformat()

    context = {
        'post': post,
    }
    return render(request, 'single.html', context)


# Category wise content
def singlecategory(request, category):
    category_obj = get_object_or_404(Category, name=category)
    posts = MedicalInsight.objects.filter(category=category_obj).order_by('-create_at')
    all_posts = MedicalInsight.objects.all()
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


# Upload Art and Literature
def uploadmedicalcnt(request):
    form = MediUploadForm()
    if request.method == "POST":
        form = MediUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if not post.slug:
                post.slug = post.title.replace(" ", "-").lower()

                # Ensure the slug is unique by checking if it already exists in the database
                original_slug = post.slug
                counter = 1
                while MedicalInsight.objects.filter(slug=post.slug).exists():
                    post.slug = f"{original_slug}-{counter}"
                    counter += 1

            post.writer = request.user
            content_status = ContentStatus.objects.get(name='Pending')
            post.status = content_status
            post.save()
            return redirect('home')

        else:
            form = MediUploadForm()

    return render(request, 'upload_content.html', {'form': form})


