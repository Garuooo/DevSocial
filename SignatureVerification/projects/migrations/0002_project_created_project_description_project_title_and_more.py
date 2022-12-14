# Generated by Django 4.1.3 on 2022-11-25 22:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='title',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AddField(
            model_name='project',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
