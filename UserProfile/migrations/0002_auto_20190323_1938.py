# Generated by Django 2.1 on 2019-03-23 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='headImage',
            field=models.ImageField(default='medie/headimage/1.jpg', upload_to='headImage'),
        ),
    ]
