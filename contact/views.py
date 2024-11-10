from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email to admin
            subject = f"New Contact Form Submission: {contact.subject}"
            message = f"""
            Name: {contact.name}
            Email: {contact.email}
            Subject: {contact.subject}
            Message: {contact.message}
            """
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # Admin email address
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact:contact')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})
