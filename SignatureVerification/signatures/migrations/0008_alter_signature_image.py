# Generated by Django 4.1.3 on 2022-11-26 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signatures', '0007_alter_signature_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='image',
            field=models.ImageField(blank=True, default='signatures/signature.png', upload_to=''),
        ),
    ]
