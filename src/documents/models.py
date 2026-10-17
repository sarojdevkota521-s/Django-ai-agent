from django.db import models
from django.conf import settings
from django.utils import timezone


User = settings.AUTH_USER_MODEL


class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Title()")
    content = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    active_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} (Owner: {self.owner.username})"

    def save(self, *args, **kwargs):
        if self.active and self.active_at is None:
            self.active_at = timezone.now()
        elif not self.active:
            self.active_at = None

        super().save(*args, **kwargs)