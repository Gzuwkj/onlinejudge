# Generated by Django 2.1 on 2019-03-24 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0002_auto_20190323_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='headImage',
            field=models.ImageField(default='user.jpg', upload_to='headImage'),
        ),
    ]
