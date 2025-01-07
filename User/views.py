from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from . models import User
from . forms import UserCreationForm
import random

# Create your views here.

# User Registration from
def user_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone')
            # Check if the phone number already exists
            if User.objects.filter(phone=phone_number).exists():
                messages.error(request, 'You have already an account with this phone number. Please log-in your account or choose another phone number')
                return (request, '', {'form': form, 'show_alert': True})
        
            user = form.save(commit=False)
            user.username = form.clean_username()
            otp = str(random.randint(10000, 99999))
            print(otp)

            request.session['otp'] = otp

            # Save the user instance in the session for later retrieval
            request.session['user_info'] = {
                'username': user.username,
                'name': form.cleaned_data.get('name'),
                'email': form.cleaned_data.get('email'),
                'phone_number': phone_number,
            }

            return redirect('verify_otp')
        
        else:
            for field, errors in form.error.items():
                for error in errors:
                    messages.error(request, f'{field.capitalized()}: {error}')
    
    else:
        form = UserCreationForm()

    return render(request, 'registration.html', {'form': form})


# Verify OTP
def verify_otp(request):
    
    if request.method == 'POST':
        user_input_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp', '')

        if user_input_otp == stored_otp:
            user_data = request.session.get('user_info', {})

            user = User.objects.create_user(
                username = user_data['username'],
                name = user_data['name'],
                email = user_data['email'],
                phone = user_data['phone_number'],
            )

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
def log_in(request):

    if request.method == "POST":
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(phone=phone, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {user.name}")
            next_url = request.GET.get('next', reverse('home'))
            return redirect(next_url)

        else:
            messages.error(request, "Invalid phone or password. Please try again.")

    return render(request, 'log_in.html')






