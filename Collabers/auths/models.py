from django.db import models

from django.contrib.auth.models import User
# Create your models here.

USER_TYPE_CHOICES = [
    ('brand', 'Brand'),
    ('influencer', 'Influencer'),
    ('admin', 'Admin'),
]

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

