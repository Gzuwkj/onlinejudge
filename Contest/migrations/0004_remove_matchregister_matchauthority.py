# Generated by Django 2.1 on 2019-01-18 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0003_auto_20190112_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchregister',
            name='matchAuthority',
        ),
    ]
