import profile

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def admin_profile_creation_(sender, instance, created, **kwargs):
    '''
    if user is created by createsuperuser then it will create instance of profile
    '''
    if created:
        if instance.is_superuser:
            Profile.objects.create(name='admin', user=instance).save()