# Generated by Django 3.2.7 on 2021-10-30 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_authorpost_image_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=234, null=True, unique=True),
        ),
    ]
