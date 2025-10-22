from django.db import models

from django.contrib.auth.models import User

import random
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
    is_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)

    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.save()
        return self.otp_code
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

