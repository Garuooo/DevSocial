# Generated by Django 4.1.3 on 2022-11-22 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signatures', '0003_verify'),
    ]

    operations = [
        migrations.AddField(
            model_name='verify',
            name='prediction',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
