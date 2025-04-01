from django.db import models
from django.core.exceptions import ValidationError

class OriginData(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latlng = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and OriginData.objects.exists():
            raise ValidationError("Accept only one Origin")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
