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
class Influencer(models.Model):
    influ_id = models.AutoField(primary_key=True)
    influ_acc = models.OneToOneField(Account, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=225)
    channel_id = models.BigIntegerField(max_length=20)
    channel_niche = models.CharField(max_length=50, choices=NICHE_CHOICES)
    channel_follower = models.BigIntegerField(max_length=225,blank=True, null=True)
    channel_engagement_rate = models.DecimalField(max_digits=20, decimal_places=10,blank=True, null=True)
    channel_avg_like = models.BigIntegerField(max_length=225,blank=True, null=True)
    channel_avg_comments = models.BigIntegerField(max_length=225,blank=True, null=True)
    wallet = models.IntegerField(default=0,blank=True,null=True)
    
    def __str__(self):
        return f"{self.channel_name} - {self.channel_niche}"

class Applicant(models.Model):
    appli_id = models.AutoField(primary_key=True)
    post = models.ForeignKey('brand.Post',related_name="applicant_post",on_delete=models.CASCADE)
    influencer = models.ForeignKey(Influencer,related_name="applicant_influencer",on_delete=models.CASCADE)
    efficiency_prob = models.DecimalField(max_digits=20, decimal_places=10,blank=True,null=True)
    ads_file = models.FileField(upload_to='uploads/ads/', blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    is_worked = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_posted = models.BooleanField(default=False)
    is_stoped = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)
    url = models.URLField(max_length=200, blank=True, null=True) 
    amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    summary = models.CharField(max_length=225, blank=True, null= True)
    remarks = models.CharField(max_length=225, blank=True, null= True)

    def __str__(self):
        return f"Application by {self.influencer} for {self.post}"
