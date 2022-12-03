# Generated by Django 4.1.3 on 2022-11-27 21:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('signatures', '0010_alter_note_owner_alter_note_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
