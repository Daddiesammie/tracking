from django.db import models
from ckeditor.fields import RichTextField

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='site_settings/', null=True, blank=True)
    favicon = models.ImageField(upload_to='site_settings/', null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    # Social Links
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    
    # SEO Fields
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.TextField(max_length=255, blank=True)
    
    # Rich Text Content
    about_us = RichTextField()
    terms_and_conditions = RichTextField()
    privacy_policy = RichTextField()
    disclaimer = RichTextField()
    
    # Additional fields
    maintenance_mode = models.BooleanField(default=False)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    custom_css = models.TextField(blank=True)
    custom_js = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            # If you're trying to create a new settings instance,
            # and one already exists, update the existing one.
            raise ValueError("There can only be one SiteSettings instance")
        return super(SiteSettings, self).save(*args, **kwargs)