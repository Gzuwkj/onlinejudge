# Generated by Django 2.1.3 on 2018-12-03 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchName', models.CharField(max_length=30, unique=True)),
                ('startTime', models.DateTimeField()),
                ('howLong', models.IntegerField(blank=True, default=120)),
                ('attribute', models.CharField(choices=[('私有', '私有'), ('公开', '公开')], default='公开', max_length=2)),
                ('matchAuthority', models.CharField(blank=True, choices=[('允许', '允许'), ('禁止', '禁止')], default='允许', max_length=2)),
                ('matchInclude', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MatchRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchName', models.CharField(blank=True, max_length=30)),
                ('userName', models.CharField(blank=True, max_length=30)),
                ('acTime', models.IntegerField(blank=True, default=0)),
                ('wrongTimes', models.IntegerField(blank=True, default=0)),
                ('score', models.IntegerField(blank=True, default=0)),
                ('ranking', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MatchRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchName', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=10)),
                ('registerTime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MatchSubmit',
            fields=[
                ('matchName', models.CharField(blank=True, max_length=30)),
                ('userName', models.CharField(blank=True, max_length=30)),
                ('probID', models.IntegerField()),
                ('content', models.TextField(blank=True)),
                ('runID', models.AutoField(primary_key=True, serialize=False)),
                ('result', models.CharField(blank=True, default='0', max_length=2)),
                ('time', models.IntegerField(blank=True, default=0)),
                ('memory', models.IntegerField(blank=True, default=0)),
                ('language', models.CharField(blank=True, choices=[('C', 'C'), ('C++', 'C++'), ('Java', 'Java'), ('Python', 'Python')], default='C++', max_length=9)),
                ('subTime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]