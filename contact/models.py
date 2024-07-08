from django.db import models

# Create your models here.

class ContactUsModel(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=400)
    email   = models.EmailField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'