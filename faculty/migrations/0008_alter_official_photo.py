# Generated by Django 5.1.5 on 2025-06-08 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0007_websitesettings_bank1_account_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='official',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='officials_photos/'),
        ),
    ]
