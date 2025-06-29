from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Profile
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance, role='SHEPHERD', phone='')

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance, role='SHEPHERD', phone='')