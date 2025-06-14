# Generated by Django 5.2.1 on 2025-05-19 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auths', '0001_initial'),
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Influencer',
            fields=[
                ('influ_id', models.AutoField(primary_key=True, serialize=False)),
                ('channel_name', models.CharField(max_length=225)),
                ('channel_id', models.BigIntegerField(max_length=20)),
                ('channel_niche', models.CharField(choices=[('food', 'Food & Beverage'), ('it', 'Technology / IT'), ('fashion', 'Fashion & Apparel'), ('travel', 'Travel & Tourism'), ('fitness', 'Fitness & Health'), ('beauty', 'Beauty & Skincare'), ('lifestyle', 'Lifestyle'), ('education', 'Education & Learning'), ('finance', 'Finance & Investment'), ('gaming', 'Gaming'), ('sports', 'Sports & Outdoors'), ('automotive', 'Automotive'), ('home_decor', 'Home Decor & Furniture'), ('pets', 'Pet Products'), ('entertainment', 'Entertainment & Media'), ('eco', 'Eco-friendly / Sustainability'), ('parenting', 'Parenting & Family'), ('real_estate', 'Real Estate'), ('books', 'Books & Publishing'), ('luxury', 'Luxury Goods')], max_length=50)),
                ('channel_follower', models.BigIntegerField(blank=True, max_length=225, null=True)),
                ('channel_engagement_rate', models.DecimalField(blank=True, decimal_places=10, max_digits=10, null=True)),
                ('channel_avg_like', models.BigIntegerField(blank=True, max_length=225, null=True)),
                ('channel_avg_comments', models.BigIntegerField(blank=True, max_length=225, null=True)),
                ('wallet', models.IntegerField(blank=True, default=0, null=True)),
                ('influ_acc', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auths.account')),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('appli_id', models.AutoField(primary_key=True, serialize=False)),
                ('efficiency_prob', models.DecimalField(blank=True, decimal_places=10, max_digits=10, null=True)),
                ('ads_file', models.FileField(blank=True, null=True, upload_to='uploads/ads/')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_worked', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_posted', models.BooleanField(default=False)),
                ('is_stoped', models.BooleanField(default=False)),
                ('is_payed', models.BooleanField(default=False)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('summary', models.CharField(blank=True, max_length=225, null=True)),
                ('remarks', models.CharField(blank=True, max_length=225, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_post', to='brand.post')),
                ('influencer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_influencer', to='influencer.influencer')),
            ],
        ),
    ]
