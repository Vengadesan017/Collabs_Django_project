from django.db import models

from auths.models import Account
from django.core.exceptions import ValidationError

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

def validate_file(file):
    # Max size 5MB
    max_size = 5 * 1024 * 1024  # 5 MB in bytes
    if file.size > max_size:
        raise ValidationError("File size must be under 5MB")
    
    # Allowed content types
    valid_mime_types = [
        'image/jpeg',
        'image/png',
        'image/gif',
        'application/pdf'
    ]
    if file.content_type not in valid_mime_types:
        raise ValidationError("Unsupported file type. Only images and PDFs are allowed.")

# Create your models here.
class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_acc = models.OneToOneField(Account, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100)
    brand_niche = models.CharField(max_length=50, choices=NICHE_CHOICES)
    wallet = models.IntegerField(default=1000000,blank=True,null=True)
    upi_qr_code = models.ImageField(upload_to='brand_upi_qr_codes/',validators=[validate_file], blank=True, null=True)  # New field

    def __str__(self):
        return f"{self.brand_name} - {self.get_brand_niche_display()}"
    
    
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="post_brand")
    post_name = models.CharField(max_length=100)
    detail = models.CharField(max_length=225)
    budget = models.IntegerField(max_length=10)
    max_influencer = models.IntegerField()
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.post_name} - {self.brand}"
    