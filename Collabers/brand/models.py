from django.db import models

from auths.models import Account
NICHE_CHOICES = [
    ('food', 'Food & Beverage'),
    ('it', 'Technology / IT'),
    ('fashion', 'Fashion & Apparel'),
    ('travel', 'Travel & Tourism'),
    ('fitness', 'Fitness & Health'),
    ('beauty', 'Beauty & Skincare'),
    ('lifestyle', 'Lifestyle'),
    ('education', 'Education & Learning'),
    ('finance', 'Finance & Investment'),
    ('gaming', 'Gaming'),
    ('sports', 'Sports & Outdoors'),
    ('automotive', 'Automotive'),
    ('home_decor', 'Home Decor & Furniture'),
    ('pets', 'Pet Products'),
    ('entertainment', 'Entertainment & Media'),
    ('eco', 'Eco-friendly / Sustainability'),
    ('parenting', 'Parenting & Family'),
    ('real_estate', 'Real Estate'),
    ('books', 'Books & Publishing'),
    ('luxury', 'Luxury Goods'),
]


# Create your models here.
class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_acc = models.OneToOneField(Account, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100)
    brand_niche = models.CharField(max_length=50, choices=NICHE_CHOICES)
    wallet = models.IntegerField(default=0,blank=True,null=True)
    
    def __str__(self):
        return self.brand_name
    
    
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="post_brand")
    post_name = models.CharField(max_length=100)
    detail = models.CharField(max_length=225)
    budget = models.IntegerField(max_length=10)
    max_influencer = models.IntegerField()
    is_open = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.post_name} - {self.brand}"
    