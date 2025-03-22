from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.base.models import BaseModel




class CustomUser(AbstractUser, BaseModel):

    GENDER_CHOICES = (
    ("male", "Erkak"),
    ("female", "Ayol"),
    )

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="user_avatars/", blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.username