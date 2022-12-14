# Generated by Django 4.1.3 on 2022-12-02 23:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_personal_signature_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('name', models.CharField(max_length=250)),
                ('body', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
