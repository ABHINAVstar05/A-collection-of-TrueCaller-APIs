# Generated by Django 5.0.3 on 2024-03-24 04:33

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(10)])),
                ('spam_reported_count', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(10)])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='registered_user_permissions', related_query_name='registered_user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(10)])),
                ('users', models.ManyToManyField(blank=True, related_name='contacts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
