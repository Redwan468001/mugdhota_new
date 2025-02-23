from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from content.models import Content
from . models import User
from . forms import UserCreationF
import random
from itertools import chain

# Create your views here.

# User Profile
def userDashboard(request, username):
    user = get_object_or_404(User, username=username)

    posts = Content.objects.filter(writer=user)
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

    return render(request, 'user_profile.html', context)


# Total Posts
def user_total_content(request, username):
    user = get_object_or_404(User, username=username)
    all_posts = Content.objects.filter(writer=user)

    context = {
        'user': user,
        'all_posts': all_posts,
    }

    return render(request, 'total_contents.html', context)


# Published Post
def user_published_content(request, username):
    user = get_object_or_404(User, username=username)
    all_posts = Content.objects.filter(writer=user, status=1)

    count = len(all_posts)
    context = {
        'user': user,
        'all_posts': all_posts,
        'count': count,
    }

    return render(request, 'users_content.html', context)


# Pending Post
def user_pending_content(request, username):
    user = get_object_or_404(User, username=username)
    all_posts = Content.objects.filter(writer=user, status=2)

    count = len(all_posts)
    context = {
        'user': user,
        'all_posts': all_posts,
        'count': count,
    }

    return render(request, 'users_content.html', context)


# Refuge Post
def user_refuge_content(request, username):
    user = get_object_or_404(User, username=username)
    all_posts = Content.objects.filter(writer=user, status=3)

    count = all_posts.count()
    context = {
        'user': user,
        'all_posts': all_posts,
        'count': count,
    }

    return render(request, 'user_refuge_content.html', context)


# User Registration from
def user_registration(request):
    if request.method == 'POST':
        form = UserCreationF(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone')

            if User.objects.filter(phone=phone_number).exists():
                messages.error(request, 'You already have an account with this phone number.')
                return render(request, 'registration.html', {'form': form})

            user = form.save(commit=False)
            user.username = form.clean_username()
            otp = str(random.randint(10000, 99999))
            print(otp)

            request.session['otp'] = otp

            # ✅ Store password in session
            request.session['user_info'] = {
                'username': user.username,
                'name': form.cleaned_data.get('name'),
                'email': form.cleaned_data.get('email'),
                'phone_number': phone_number,
                'password': form.cleaned_data.get('password1')  # Django's UserCreationForm uses 'password1'
            }

            return redirect('verify_otp')

    else:
        form = UserCreationF()

    return render(request, 'registration.html', {'form': form})


# Verify OTP
def verify_otp(request):
    
    if request.method == 'POST':
        user_input_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp', '')

        if user_input_otp == stored_otp:
            user_data = request.session.get('user_info', {})

            user = User.objects.create(
                username=user_data['username'],
                name=user_data['name'],
                email=user_data['email'],
                phone=user_data['phone_number'],
            )
            user.set_password(user_data['password'])
            user.save()

            messages.success(request, 'OTP verify Successfully')
            login(request, user)
            messages.info(request, f"You are now logged in as {user_data['name']}")

            return redirect('home')
        
        else:
            # Invalid OTP
            messages.error(request, 'Invalid OTP. Please try again.')

    # Handle the case where the request is not a POST request or if OTP validation fails
    return render(request, 'verify_otp.html')


# Log-in view
User = get_user_model()

def logIn(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        try:
            user = User.objects.get(phone=phone)  # Check if user exists
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('log_in')  # Redirect back to login page

        # Authenticate using the phone number
        user = authenticate(request, username=phone, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {user.name}")
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, "Invalid phone or password. Please try again.")
            return redirect('log_in')  # Redirect back to login page

    return render(request, 'log_in.html')


# Log out view
def log_out(request):
    logout(request)
    return redirect('home')




