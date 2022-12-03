from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User
from .models import Profile
from django.dispatch import receiver
import random

def CreateProfile(sender,instance,created,**kwargs):
    if created == True:
        user = instance
        profile = Profile.objects.create(user=user,
                                        email=user.email,
                                        national_id=random.randint(10000,10000000000),
                                        username=user.username,
  
                                      first_name=user.first_name)
@receiver(post_delete,sender=Profile)
def DeleteProfile(sender,instance,**kwargs):
    user = instance.user
    user.delete()

post_save.connect(CreateProfile,sender=User)
    