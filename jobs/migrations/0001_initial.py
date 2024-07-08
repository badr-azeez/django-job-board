# Generated by Django 5.0.4 on 2024-07-06 15:31

import autoslug.fields
import ckeditor_uploader.fields
import django.db.models.deletion
import django_countries.fields
import jobs.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryJobModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='JobsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=205, verbose_name='Title')),
                ('slug', autoslug.fields.AutoSlugField(default='', editable=False, populate_from='title', unique=True)),
                ('country', django_countries.fields.CountryField(max_length=2, null=True, verbose_name='Country')),
                ('job_type', models.CharField(choices=[('full time', 'full time'), ('part time', 'part time')], max_length=20, verbose_name='Job Type')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=8000, null=True, verbose_name='Description')),
                ('vacancy', models.IntegerField(default=1, verbose_name='Vacancy')),
                ('salary', models.IntegerField(default=0, verbose_name='Salary($/M)')),
                ('experience', models.IntegerField(default=1, verbose_name='Experience(Y)')),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.categoryjobmodel', verbose_name='Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_job', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'job',
            },
        ),
        migrations.CreateModel(
            name='ApplyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('cv_file', models.FileField(upload_to=jobs.models.fileUpload)),
                ('cover_latter', models.TextField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apply_not_users', to='jobs.jobsmodel')),
            ],
            options={
                'verbose_name': 'Applies Non User',
            },
        ),
        migrations.CreateModel(
            name='ApplyUsersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apply_users', to='jobs.jobsmodel')),
            ],
            options={
                'verbose_name': 'Applies User',
                'unique_together': {('user', 'job')},
            },
        ),
    ]
