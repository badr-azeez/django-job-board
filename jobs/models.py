from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
import uuid ,os
from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField

from datetime import datetime
year = datetime.today().year
month = datetime.today().month

def imageUpload(instance, filename):
    uuid_token = uuid.uuid4().hex
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid_token}{ext}"
    return f"media/jobs/{new_filename}"

def fileUpload(instance,filename):
    uuid_token = uuid.uuid4().hex
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid_token}{ext}"
    return f"media/apply/{new_filename}"



class JobsModel(models.Model): 
    JOB_TYPES = (
        ('full time','full time'),
        ('part time','part time')
    )
    user = models.ForeignKey(User,related_name='user_job',on_delete=models.CASCADE) 
    title = models.CharField(max_length=205,verbose_name='Title') 
    slug = AutoSlugField(populate_from='title',unique=True,default='')
    country = CountryField(verbose_name='Country',null=True)
    job_type = models.CharField(verbose_name='Job Type',max_length=20,choices=JOB_TYPES)
    description = RichTextUploadingField(verbose_name='Description',max_length=8000,null=True,blank=True)
    vacancy =  models.IntegerField(verbose_name='Vacancy',default=1)
    salary = models.IntegerField(verbose_name='Salary($/M)',default=0)
    experience = models.IntegerField(verbose_name='Experience(Y)',default=1)
    category = models.ForeignKey('CategoryJobModel',on_delete=models.CASCADE,verbose_name='Category')
    published_at =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'job'
    
class CategoryJobModel(models.Model):
    name = models.CharField(max_length=50,unique=True,)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class ApplyModel(models.Model):
    job = models.ForeignKey(JobsModel,related_name='apply_not_users',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    website = models.URLField(blank=True,null=True)
    cv_file = models.FileField(upload_to=fileUpload)
    cover_latter = models.TextField(max_length=500,blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Applies Non User'

class ApplyUsersModel(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    job = models.ForeignKey(JobsModel,on_delete=models.CASCADE,related_name='apply_users')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name 
    
    class Meta:
        unique_together = ('user','job')
        verbose_name = 'Applies User'
