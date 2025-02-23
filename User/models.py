from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from datetime import datetime

# Create your models here.

class Gender(models.Model):
    gender = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.gender
    

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, blank=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField()
    phone_validator = RegexValidator(regex=r'^\+?1?\d{11}', message="Phone number must be entered in the format: '01234567899'. Up to 11 digits allowed.")
    phone = models.CharField(validators=[phone_validator], max_length=11, null=False, unique=True)
    bio = models.TextField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    joined = models.DateField(auto_now=True)

    # User Controller
    is_admin = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    is_subscriber = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone'

    def get_user_role(self):
        if self.is_admin:
            return "Admin"
        elif self.is_author:
            return "Author"
        else:
            return "Subscriber"


    def __str__(self):
        return self.name

def set_username(sender, instance, **kwargs):
    # Check if the user is new (not being updated)
    if instance.pk is None:
        # Remove spaces and convert to lowercase
        base_username = instance.username

        # Check if the initial username is already taken
        if User.objects.filter(username=base_username).exists():
            # Initialize the serial number
            serial_number = 1

            while True:
                # Create the username with the serial number
                username = f"{base_username}{serial_number}"

                # Check if the username is unique
                if not User.objects.filter(username=username).exists():
                    break

                # Increment the serial number and try again
                serial_number += 1

            instance.username = username.replace(' ', '').lower()

# Connect the signal
models.signals.pre_save.connect(set_username, sender=User)


