from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    full_name = models.CharField(null=True, max_length=120)
    id_card = models.IntegerField()
    is_driver = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    username = models.CharField(unique=False, max_length=20, null=True, default=None)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'age', 'id_card', 'first_name', 'last_name', 'username']