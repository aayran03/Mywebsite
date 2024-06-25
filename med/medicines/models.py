# medicines/models.py
from django.db import models
from django.utils import timezone

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    identification_number = models.CharField(max_length=255, unique=True)
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

    def is_near_expiry(self):
        return self.expiry_date <= timezone.now().date() + timezone.timedelta(days=30)
    
    def expiry_days_left(self):
        today = timezone.now().date()
        days_left = (self.expiry_date - today).days
        return days_left
