from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

"""
# custom user settings
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    url1 = models.CharField(max_length=200, null=True, blank=True)
    url2 = models.CharField(max_length=200, null=True, blank=True)
    url3 = models.CharField(max_length=200, null=True, blank=True)
    url4 = models.CharField(max_length=200, null=True, blank=True)
    url5 = models.CharField(max_length=200, null=True, blank=True)
    url6 = models.CharField(max_length=200, null=True, blank=True)

    
    def create_profile(instance):
        Profile.objects.create(user=instance)
    
    def __str__(self):
        return f'{self.user.username} Profile'
"""


class Profile(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url1 = models.CharField(max_length=200, null=True, blank=True)
    url2 = models.CharField(max_length=200, null=True, blank=True)
    url3 = models.CharField(max_length=200, null=True, blank=True)
    url4 = models.CharField(max_length=200, null=True, blank=True)
    url5 = models.CharField(max_length=200, null=True, blank=True)
    url6 = models.CharField(max_length=200, null=True, blank=True)

    @receiver(post_save, sender=User) #add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    
    @receiver(post_save, sender=User) #add this
    def save_user_profile(sender, instance, **kwargs):
	    instance.profile.save()