from django.db import models

class ChatScript(models.Model):
    name = models.CharField(max_length=100)
    script_tag = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Chat Script'
        verbose_name_plural = 'Chat Scripts'

    def __str__(self):
        return self.name
