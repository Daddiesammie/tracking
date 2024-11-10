from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .email_utils import send_status_update_email
import logging

logger = logging.getLogger(__name__)

class Product(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipments', null=True)
    tracking_number = models.CharField(max_length=12, unique=True, editable=False)
    sender_name = models.CharField(max_length=100)
    sender_address = models.TextField()
    recipient_name = models.CharField(max_length=100)
    recipient_address = models.TextField()
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = str(uuid.uuid4().hex[:12].upper())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_number} - {self.recipient_name}"

class TrackingStatus(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=20, choices=Product.STATUS_CHOICES)
    location = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.tracking_number} - {self.status}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Tracking statuses'

    def save(self, *args, **kwargs):
        logger.debug(f"Saving TrackingStatus {self.pk}")
        is_new = self._state.adding
        old_status = None
        if not is_new:
            try:
                old_status = TrackingStatus.objects.get(pk=self.pk).status
            except TrackingStatus.DoesNotExist:
                logger.warning(f"TrackingStatus with pk {self.pk} does not exist.")

        super().save(*args, **kwargs)

        if is_new or (old_status and old_status != self.status):
            logger.info(f"Status changed for TrackingStatus {self.pk}. Sending email and creating notification.")
            try:
                send_status_update_email(self)
                self.create_notification()
                self.update_product_status()
            except Exception as e:
                logger.exception(f"Error updating status for TrackingStatus {self.pk}: {str(e)}")

    def send_status_update_email(self):
        subject = f'Package Update - {self.product.tracking_number}'
        context = {
            'tracking_number': self.product.tracking_number,
            'status': self.get_status_display(),
            'location': self.location,
            'description': self.description,
            'timestamp': self.timestamp,
            'recipient_name': self.product.recipient_name
        }
        
        html_message = render_to_string('tracking/emails/status_update.html', context)
        
        if self.product.user and self.product.user.email:
            send_mail(
                subject=subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.product.user.email],
                html_message=html_message
            )

    def create_notification(self):
        if self.product.user:
            Notification.objects.create(
                user=self.product.user,
                message=f"Your shipment {self.product.tracking_number} is now {self.get_status_display()} at {self.location}."
            )

    def update_product_status(self):
        self.product.current_status = self.status
        self.product.save()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"
    
class BitcoinWallet(models.Model):
    address = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.address

class BitcoinPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    payment_proof = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.product.tracking_number}"