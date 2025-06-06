# Generated by Django 5.1.5 on 2025-06-06 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='websiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook_link', models.CharField(max_length=200)),
                ('instagram_link', models.CharField(max_length=200)),
                ('x_link', models.CharField(max_length=200)),
                ('linked_in_link', models.CharField(max_length=200)),
                ('arcdo_email', models.CharField(max_length=200)),
                ('phone_number_1', models.CharField(max_length=200)),
                ('phone_number_2', models.CharField(max_length=200)),
                ('arcdo_address', models.CharField(max_length=200)),
            ],
        ),
    ]
