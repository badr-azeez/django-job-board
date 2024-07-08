from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import ContactUsForm

# Create your views here.
def send_message(request):
    contact_us_form = ContactUsForm()

    context= {
        'contact_us_form':contact_us_form
    }
    
    if request.method == 'POST':
        
        contact_us_form = ContactUsForm(request.POST)
        if contact_us_form.is_valid():
            contact_us_form.save()
            # send message to sender
            if settings.EMAIL_HOST_USER:
                subject = contact_us_form.cleaned_data.get('subject')
                message = "Hello,\n\nThank you for reaching out. We've received your message and will get back to you promptly. Please expect a response from us soon.\nBest regards,"
                email_from =  settings.EMAIL_HOST_USER
                recipient_list = [contact_us_form.cleaned_data.get('email')]
                send_mail( subject, message, email_from, recipient_list )

                # send message to admin
                subject = contact_us_form.cleaned_data.get('subject')
                message = f"Email From {contact_us_form.cleaned_data.get('email')} \n {contact_us_form.cleaned_data.get('message')}"
                email_from =  settings.EMAIL_HOST_USER
                recipient_list = [settings.ADMIN_EMAIL]
                send_mail( subject, message, email_from, recipient_list )
                return redirect(reverse('contact_us:send_message'))
            
            context.update({'msg':'Your Message Is Sent'})

    return render(request,'contact/send_message.html',context)