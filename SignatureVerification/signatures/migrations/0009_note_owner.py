# Generated by Django 4.1.3 on 2022-11-27 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_personal_signature_and_more'),
        ('signatures', '0008_alter_signature_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
