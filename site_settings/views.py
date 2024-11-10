from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import SiteSettings

def static_page(request, page_name):
    site_settings = get_object_or_404(SiteSettings)
    
    if hasattr(site_settings, page_name):
        content = getattr(site_settings, page_name)
        title = page_name.replace('_', ' ').title()
        return render(request, 'site_settings/static_page.html', {
            'title': title,
            'content': content,
        })
    else:
        raise Http404("Page not found")

def about_us(request):
    return static_page(request, 'about_us')

def terms_and_conditions(request):
    return static_page(request, 'terms_and_conditions')

def privacy_policy(request):
    return static_page(request, 'privacy_policy')

def disclaimer(request):
    return static_page(request, 'disclaimer')