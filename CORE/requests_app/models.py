from django.db import models
from accounts.models import User
from django.utils import timezone

class Request(models.Model):
    CATEGORY_CHOICES = (
        ('food', 'Food'),
        ('water', 'Water'),
        ('clothing', 'Clothing'),
        ('shelter', 'Shelter'),
        ('medical', 'Medical Supplies'),
        ('other', 'Other'),
        # Add more as needed
    )
    URGENCY_LEVELS = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='No title given')
    description = models.TextField(default='No description given')
    location = models.CharField(max_length=255, default='No location given')# add a more detailed address later
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    urgency = models.CharField(max_length=10, choices=URGENCY_LEVELS, default='Low')
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='Pending')
    accepted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='accepted_requests')# changeed the default to None if no one has accepted the request
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    #accepts = models.ManyToManyField(User, related_name='accepted_requests', blank=True)
    def __str__(self):
        return self.title