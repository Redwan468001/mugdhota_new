from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils.timezone import now, timedelta, datetime
from django.contrib.auth.decorators import login_required
from . models import Content, ContentStatus, Tag, Category, SubCategory
from . forms import ContentUploadForm
from django.contrib import messages

# Create your views here.
def artandliterature(request):
    posts = Content.objects.filter(category=1)
    sub_categories = SubCategory.objects.filter(category=1)
    title = 'Art And Literature'

    context = {
        'posts': posts,
        'title': title,
        'sub_categories': sub_categories,
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


# Category wise content
def singlecategory(request, category):
    category_obj = get_object_or_404(SubCategory, name=category)
    posts = Content.objects.filter(sub_category=category_obj).order_by('-create_at')
    categories = []
    sub_categories = []
    for post in posts:
        if post.category not in categories:
            categories.append(post.category)
            sub_categories = SubCategory.objects.filter(category=post.category)

    context = {
        'category_obj': category_obj,
        'posts': posts,
        'categories': categories,
        'sub_categories': sub_categories,
    }

    return render(request, 'page.html', context)


# Upload Art and Literature
@login_required(login_url='log_in')
def uploadContent(request):
    form = ContentUploadForm()
    if request.method == "POST":
        form = ContentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            # Generate a unique slug if not provided
            if not post.slug:
                post.slug = post.title.replace(" ", "-").lower()
                original_slug = post.slug
                counter = 1
                while Content.objects.filter(slug=post.slug).exists():
                    post.slug = f"{original_slug}-{counter}"
                    counter += 1

            post.writer = request.user
            content_status = ContentStatus.objects.get(name='Pending')
            post.status = content_status

            post.save()  # Save the instance first to populate the 'id'

            selected_tags = form.cleaned_data.get('tags')  # Get selected tags
            if selected_tags:
                post.tags.set(selected_tags)  # Use .set() to update the tags for this object

            # Optionally, handle new tags here (if you allow users to create new tags)
            new_tag_names = form.cleaned_data.get('new_tags', [])
            if new_tag_names:
                # Create new tags if they don't exist
                new_tags = [Tag.objects.get_or_create(name=tag)[0] for tag in new_tag_names]
                post.tags.add(*new_tags)

            # return redirect('home')

        return redirect('home')
    else:
        form = ContentUploadForm()

    return render(request, 'upload_content.html', {'form': form})


@login_required(login_url='log_in')
def editContent(request, slug):
    post = get_object_or_404(Content, slug=slug)
    form = ContentUploadForm(instance=post)
    if request.method == "POST":
        form = ContentUploadForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()

            messages.success(request, 'Successfully edit content')

            selected_tags = form.cleaned_data.get('tags')
            if selected_tags:
                post.tags.set(selected_tags)

            new_tags_name = form.cleaned_data.get('new_tags', [])
            if new_tags_name:
                new_tags = [Tag.objects.get_or_create(name=tag)[0] for tag in new_tags_name ]
                post.tags.add(*new_tags)

            return redirect('profile', request.user.username)

        else:
            form = ContentUploadForm()

    return render(request, 'upload_content.html', {'form':form})


# Delete views
@login_required(login_url='log_in')
def deletecontent(request, slug):
    post = get_object_or_404(Content, slug=slug)

    if request.user != post.writer and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this post.")
        return redirect('usercontent', request.user.username)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('usercontent', request.user.username)

    return render(request, 'delete.html', {'post': post})


def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategory = SubCategory.objects.filter(category_id=category_id)
    return JsonResponse(list(subcategory.values('id', 'name')), safe=False)