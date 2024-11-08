# Generated by Django 5.1.2 on 2024-11-03 03:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests_app', '0004_request_location'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='accepted_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accepted_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
