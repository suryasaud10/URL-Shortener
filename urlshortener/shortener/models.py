from django.db import models
from django.conf import settings
from django.utils import timezone
import string
import secrets

class ShortURL(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    original_url = models.URLField()
    short_key = models.CharField(
        max_length=10,
        unique=True,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)
    expiration_date = models.DateTimeField(null=True, blank=True)
    custom_key = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.short_key} -> {self.original_url}"

    @staticmethod
    def generate_short_key(length=6):
        chars = string.ascii_letters + string.digits  # Base62
        while True:
            key = ''.join(secrets.choice(chars) for _ in range(length))
            if not ShortURL.objects.filter(short_key=key).exists():
                return key

    def is_expired(self):
        if not self.expiration_date:
            return False
        return timezone.now() > self.expiration_date
