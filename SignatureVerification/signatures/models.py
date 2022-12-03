from django.db import models
import uuid
from users.models import Profile


class Signature(models.Model):
    owner = models.ForeignKey(Profile, blank=False,
                              null=True, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=False,
                              default='signatures/signature.png')
    title = models.CharField(blank=False, null=False, max_length=300)
    description = models.TextField(blank=True, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False, unique=True)

    def __str__(self):
        return self.title[0:50]


class Verify(models.Model):
    owner = models.ForeignKey(Profile, blank=False,
                              null=True, on_delete=models.CASCADE)
    first_signature = models.ImageField(
        null=False, blank=False, upload_to="signatures/")
    second_signature = models.ImageField(
        null=False, blank=False, upload_to="signatures/")
    created = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=10, blank=True, null=False)

    def __str__(self):
        return str(self.owner.username)


class Note(models.Model):
    vote_type = (
        ('valid', 'Valid'),
        ('Invalid', 'Invalid')
    )
    signature = models.OneToOneField(
        Signature, on_delete=models.CASCADE, null=True)
    body = models.TextField(null=False, blank=True)
    value = models.TextField(null=False, choices=vote_type, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False, unique=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.body[0:50]


class Tag(models.Model):
    name = models.CharField(null=False, blank=False, max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name[0:50]
