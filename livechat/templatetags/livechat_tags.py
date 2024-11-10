from django import template
from django.utils.safestring import mark_safe
from livechat.models import ChatScript

register = template.Library()

@register.simple_tag
def render_chat_script():
    active_script = ChatScript.objects.filter(is_active=True).first()
    if active_script:
        return mark_safe(active_script.script_tag)
    return ''
