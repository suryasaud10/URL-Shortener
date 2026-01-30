from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField()
    short_key = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    click_count = models.PositiveIntegerField(default=0)
    expiration_date = models.DateTimeField(null=True, blank=True)
    custom_key = models.BooleanField(default=False)  # For custom URLs

    def __str__(self):
        return f"{self.short_key} -> {self.original_url}"

    @staticmethod
    def generate_short_key(length=6):
        """Generate a unique Base62 short key."""
        chars = string.ascii_letters + string.digits  # Base62: a-z, A-Z, 0-9
        while True:
            key = ''.join(random.choice(chars) for _ in range(length))
            if not ShortURL.objects.filter(short_key=key).exists():
                return key

    def is_expired(self):
        """Check if the URL has expired."""
        return self.expiration_date and timezone.now() > self.expiration_date