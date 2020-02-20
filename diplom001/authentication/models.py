from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    bonuses = models.PositiveIntegerField(default=1000)
    total_bonuses = models.PositiveIntegerField(default=0, blank=True, null=True)
    avatar = models.ImageField(upload_to='pic_folder/', blank=True, null=True)

    def __str__(self):
        return self.username
