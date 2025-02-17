from django.shortcuts import render, redirect
from itertools import chain
from ArtAndLiterature.models import ArtAndLiterature
from medical.models import MedicalInsight
from django.utils.timezone import now, timedelta, datetime

# Create your views here.
def home(request):
    posts = ArtAndLiterature.objects.filter(status=1).order_by('-create_at')
    stories = []
    novels = []
    for post in posts:
        if post.category.name == 'Novel':
            novels.append(post)
        elif post.category.name == 'Story':
            stories.append(post)

    medicals = MedicalInsight.objects.filter(status=1).order_by('-create_at')


    art_posts = posts.order_by('-views')
    medi_posts = medicals.order_by('-views')

    most_popular_posts = sorted(chain(art_posts, medi_posts), key=lambda post:post.views, reverse=True)

    context = {
        'posts': posts,
        'novels': novels,
        'stories': stories,
        'medicals': medicals,
        'most_popular_posts': most_popular_posts,
    }
    return render(request, 'index.html', context)


# Get Ip Address
def get_client_ip(request):
    """Get the client IP address from request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Universal Single Post
def universalsinglepost(request, slug):

    all_posts = ArtAndLiterature.objects.all()
    categories = []
    for post in all_posts:
        if post.category not in categories:
            categories.append(post.category)

    post = (ArtAndLiterature.objects.filter(slug=slug).first() or
            MedicalInsight.objects.filter(slug=slug).first())
    tags = post.tags

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
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'single.html', context)