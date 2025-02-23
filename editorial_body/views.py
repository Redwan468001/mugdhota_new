from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from content.models import Content
from User.models import User
from . forms import EditUserUploadedContent, reviewedcommentformset
from content.models import Tag, ReviewedComment
from itertools import chain
from django.contrib import messages

# Create your views here.
def is_editor(user):
    return user.is_authenticated and user.is_editor


@login_required(login_url='log_in')
@user_passes_test(is_editor)
def management_dashboard(request, username):
    user = get_object_or_404(User, username=username)
    # Own Content
    posts = Content.objects.all()
    total_posts = len(posts)
    published_posts = []
    pending_posts = []
    refuged_posts = []

    for pp in posts:
        if pp.status.name == 'Published':
            published_posts.append(pp)
        if pp.status.name == 'Pending':
            pending_posts.append(pp)
        if pp.status.name == 'Denay':
            refuged_posts.append(pp)

    total_published_posts = len(published_posts)
    total_pending_posts = len(pending_posts)
    total_refuges_posts = len(refuged_posts)

    context = {
        'user': user,
        'total_posts': total_posts,
        'total_published_posts': total_published_posts,
        'total_pending_posts': total_pending_posts,
        'total_refuges_posts': total_refuges_posts,
    }

    return render(request, 'management_profile.html', context)


# User Uploaded All Post
@login_required(login_url='log_in')
@user_passes_test(is_editor)
def user_uploaded_all_content(request):

    all_posts = Content.objects.all()
    count = len(all_posts)
    context = {
        'all_posts': all_posts,
        'count': count,
    }

    return render(request, 'users_content.html', context)


# User Uploaded Published Post
@login_required(login_url='log_in')
@user_passes_test(is_editor)
def user_published_content(request):

    all_posts = Content.objects.filter(status=1)
    count = len(all_posts)
    context = {
        'all_posts': all_posts,
        'count': count,
    }

    return render(request, 'users_content.html', context)


# User Uploaded pending Post
@login_required(login_url='log_in')
@user_passes_test(is_editor)
def user_pending_content(request):

    all_posts = Content.objects.filter(status=2)
    count = len(all_posts)
    context = {
        'all_posts': all_posts,
        'count': count,
    }

    return render(request, 'users_content.html', context)


# User Uploaded refuged Post
@login_required(login_url='log_in')
@user_passes_test(is_editor)
def user_refuged_content(request):

    all_posts = Content.objects.filter(status=3)
    count = len(all_posts)
    context = {
        'all_posts': all_posts,
        'count': count,
    }

    return render(request, 'm_refuged_content.html', context)


# Edit User Uploaded Post
@login_required(login_url='log_in')
@user_passes_test(is_editor)
def edituseruploadedpost(request, slug):
    user = request.user
    post = get_object_or_404(Content, slug=slug)
    if request.method == 'POST':
        form = EditUserUploadedContent(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.reviewed_by = user.username
            post.save()

            # Save Review comment
            reviewcnt = reviewedcommentformset(request.POST)
            if reviewcnt.is_valid():
                instances = reviewcnt.save(commit=False)
                for instance in instances:
                    instance.content = post
                    instance.user = request.user
                    instance.save()

            messages.success(request, 'Successfully updated')

            selected_tag = form.cleaned_data.get('tags')
            if selected_tag:
                post.tags.set(selected_tag)
            new_tags_name = form.cleaned_data.get('new_tags', [])
            if new_tags_name:
                new_tags = [Tag.objects.get_or_create(name=tag)[0] for tag in new_tags_name ]
                post.tags.add(*new_tags)

            return redirect('user_pending_content')

    else:
        form = EditUserUploadedContent(instance=post)
        reviewedcommentform = reviewedcommentformset()

    content = {
        'form': form,
        'reviewedcommentform': reviewedcommentform,
    }

    return render(request, 'editor_edit_content.html', content)