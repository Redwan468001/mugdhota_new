from django.shortcuts import render, redirect, get_object_or_404
from itertools import chain
from content.models import Content
from django.utils.timezone import now, timedelta, datetime

# Create your views here.
def home(request):
    posts = Content.objects.filter(status=1).order_by('-create_at')
    stories = []
    novels = []
    for post in posts:
        if post.sub_category.name == 'Novel':
            novels.append(post)
        elif post.sub_category.name == 'Story':
            stories.append(post)

    art_posts = posts.order_by('-views')

    most_popular_posts = sorted(art_posts, key=lambda post:post.views, reverse=True)

    context = {
        'posts': posts,
        'novels': novels,
        'stories': stories,
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
def singlepost(request, slug):

    all_posts = Content.objects.all()
    categories = []
    for post in all_posts:
        if post.category not in categories:
            categories.append(post.category)

    post = get_object_or_404(Content, slug=slug)
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