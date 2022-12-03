from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=False,blank=True)
    first_name = models.CharField(max_length=200,blank=True,null=False)
    last_name=models.CharField(max_length=200,blank=True,null=False)
    username = models.CharField(max_length=200,blank=True,null=False)
    email=models.EmailField(null=False,blank=True,max_length=500)
    head_line=models.CharField(max_length=500,blank=True,null=False)
    bio=models.TextField(max_length=500,blank=True,null=False)
    location = models.CharField(max_length=200,null=True,blank=True)
    personal_signature = models.ImageField(upload_to='signatures/',blank=True,null=True,editable=True,default="signatures/default.png")
    picture = models.ImageField(upload_to='profiles/',blank=True,null=True,editable=True,default="profiles/avatar.png")
    national_id = models.CharField(blank=True,null=False,unique=True,max_length=100)
    github = models.CharField(max_length=500,null=True,blank=True)
    stackoverflow = models.CharField(max_length=500,null=True,blank=True)
    twitter = models.CharField(max_length=500,null=True,blank=True)
    linkedin = models.CharField(max_length=500,null=True,blank=True)
    personalwebsite = models.CharField(max_length=500,null=True,blank=True)

    id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,blank=False,editable=False,null=False)
    def __str__(self):
        return str(self.user.username)

class Skill(models.Model):
    name = models.CharField(null=False, blank=False, max_length=250)
    body = models.TextField(blank=True,null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    def __str__(self):
        return self.name[0:50]

class Message(models.Model):
    body = models.TextField(max_length=500)
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="sender")
    reciever = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="reciever")
    title = models.CharField(max_length=250,null=True,blank= True)
    is_read = models.BooleanField(default=False,null=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body[0:50]