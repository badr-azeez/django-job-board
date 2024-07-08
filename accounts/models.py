from django.db import models
from django.contrib.auth.models import User
import uuid ,os
from django.core.validators import MinValueValidator,MaxValueValidator
from stdimage import StdImageField
from django_countries.fields import CountryField

from datetime import datetime
year = datetime.today().year
month = datetime.today().month

# Create your models here.
def fileUpload(instance,filename):
    uuid_token = uuid.uuid4().hex
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid_token}{ext}"
    return f"media/accounts/cv/{instance.id}-{new_filename}"

def imageUpload(instance, filename):
    uuid_token = uuid.uuid4().hex
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid_token}{ext}"
    return f"accounts/images/{new_filename}"

class ProfileModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    country = CountryField(verbose_name='Country',blank=True,null=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    image = StdImageField(upload_to=imageUpload, blank=True, variations={
        'large': (600, 400),
        'thumbnail': (100, 100, True),
        'medium': (300, 200),
    }, delete_orphans=True)
    birth_day = models.DateField(null=True,blank=True)
    bio      = models.TextField(max_length=250,blank=True,null=True)
    cv_file = models.FileField(upload_to=fileUpload,blank=True,null=True)
    website  = models.CharField(max_length=150,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self,*args, **kwargs):
        print(self.bio)
        super(ProfileModel,self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Profile'

class ExperienceModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='experiences')
    skill = models.CharField(max_length=30)
    level = models.IntegerField(default=1,validators=[
        MinValueValidator(1),
        MaxValueValidator(100)
        ])
    description = models.TextField(max_length=100,blank=True,null=True)
    start_at = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.skill
    class Meta:
        verbose_name = 'Experiences'