from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('requester', 'Requester'),
        ('provider', 'Provider'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    # add additional fields in here as name and email are not included in the AbstractUser model
    name = models.CharField(max_length=255, null=True, blank=True)  # Adding a name field
    email = models.EmailField(unique=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.TextField(blank=True)
    service_areas = models.CharField(max_length=255, blank=True)
    preferences = models.TextField(blank=True)
    privacy_settings = models.BooleanField(default=True)
    latitude = models.FloatField(null=True, blank=True)# latitude and longitude are used to store the user's location
    longitude = models.FloatField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}'s profile"
