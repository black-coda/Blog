# Generated by Django 3.2.7 on 2021-10-21 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='authorpost',
            name='image_cover',
            field=models.ImageField(null=True, upload_to='images_cover/'),
        ),
    ]