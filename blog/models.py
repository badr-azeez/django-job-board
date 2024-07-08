from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from stdimage import StdImageField
import uuid ,os
from django.utils.crypto import get_random_string
# Create your models here.

def imageUpload(instance, filename):
    uuid_token = uuid.uuid4().hex
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid_token}{ext}"
    return f"media/blog/{new_filename}"



class BlogModel(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,editable=False)
    slug = AutoSlugField(populate_from='title',unique=True,allow_unicode=True )
    title = models.CharField(max_length=120)
    summary_text = models.CharField(max_length=168)
    full_text = RichTextUploadingField(max_length=15000,null=True,blank=True)
    category = models.ForeignKey('CategoryModel', on_delete=models.CASCADE , related_name='blog_posts',null=True,blank=True)
    tags = models.ManyToManyField('TagModel', related_name='blog_posts',null=True,blank=True)
    comments_enable = models.BooleanField(default=True)
    image = StdImageField(upload_to=imageUpload, blank=True, variations={
        'large': (600, 400),
        'thumbnail': (80, 80, True),
        'medium': (300, 200),
    }, delete_orphans=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    updated_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Blog'

class CategoryModel(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'


class TagModel(models.Model): 
    name = models.CharField(max_length=50)
    
    def __str__(self):
            return self.name

    class Meta:
        verbose_name = 'Tag'

class CommentModel(models.Model):
    def random_id(self):
        return get_random_string(length=15) 
        
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(BlogModel,related_name='comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField( populate_from='random_id',unique=True,allow_unicode=True ,primary_key=True)
    
    def __str__(self):
        return self.comment
    
    class Meta:
        verbose_name ='Comment'
        ordering = ['-created_at']

