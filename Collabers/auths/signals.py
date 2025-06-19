from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from influencer.models import Influencer # Replace with your actual influencer model
from .views import fetch_and_store_channel_data  # Replace with correct import path

import threading

@receiver(post_save, sender=Influencer)
def fetch_youtube_data_on_signup(sender, instance, created, **kwargs):
    """
    Automatically fetch YouTube channel data when a new Influencer is created.
    Uses a background thread to avoid blocking user signup flow.
    """
    if created and instance.channel_id:
        threading.Thread(
            target=fetch_and_store_channel_data,
            args=(instance.channel_id, instance),
            daemon=True
        ).start()
