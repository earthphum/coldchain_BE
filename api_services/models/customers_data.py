from django.db import models

class CustomersData(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    coordinate = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name