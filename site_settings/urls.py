from django.urls import path
from . import views

app_name = 'site_settings'

urlpatterns = [
    path('about-us/', views.about_us, name='about_us'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
]