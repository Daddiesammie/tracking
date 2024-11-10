import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)

def send_status_update_email(tracking_status):
    logger.debug(f"Attempting to send email for TrackingStatus {tracking_status.pk}")
    
    if not tracking_status.product:
        logger.error(f"No product associated with TrackingStatus {tracking_status.pk}")
        return
    
    if not tracking_status.product.user:
        logger.warning(f"No user associated with product {tracking_status.product.tracking_number}")
        return
    
    if not tracking_status.product.user.email:
        logger.warning(f"No email associated with user {tracking_status.product.user.username}")
        return

    subject = f'Package Update - {tracking_status.product.tracking_number}'
    context = {
        'tracking_number': tracking_status.product.tracking_number,
        'status': tracking_status.get_status_display(),
        'location': tracking_status.location,
        'description': tracking_status.description,
        'timestamp': tracking_status.timestamp,
        'recipient_name': tracking_status.product.recipient_name
    }
    
    html_message = render_to_string('tracking/emails/status_update.html', context)
    
    try:
        send_mail(
            subject=subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[tracking_status.product.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email sent successfully for TrackingStatus {tracking_status.pk}")
    except Exception as e:
        logger.exception(f"Failed to send email for TrackingStatus {tracking_status.pk}: {str(e)}")