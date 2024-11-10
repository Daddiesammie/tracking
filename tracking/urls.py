from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.home, name='home'),
    path('track/<str:tracking_number>/', views.tracking_detail, name='tracking_detail'),
    path('track/<str:tracking_number>/pdf/', views.download_pdf, name='download_pdf'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracking/auth/login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('add-product/', views.add_product, name='add_product'),
    path('mark-notification-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
]
