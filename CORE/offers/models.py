from django.db import models
from accounts.models import User
from django.utils import timezone

class Offer(models.Model):
    CATEGORY_CHOICES = (
        ('food', 'Food'),
        ('water', 'Water'),
        ('clothing', 'Clothing'),
        ('shelter', 'Shelter'),
        ('medical', 'Medical Supplies'),
        ('other', 'Other'),
        # Add more as needed
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='No title given')
    description = models.TextField(default='No description given')
    location = models.CharField(max_length=255, default='No was location given')# add a more detailed address later
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='Pending')
    quantity = models.IntegerField(default=1)
    availability_start = models.DateTimeField(default=timezone.now)
    availability_end = models.DateTimeField(default=timezone.now)
    #availability_start = models.DateTimeField(default='2021-01-01T00:00')
    #availability_end = models.DateTimeField(default='2021-01-01T00:00')
    #created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_offers', blank=True)
    def __str__(self):
        return self.title