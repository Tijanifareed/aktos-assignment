from django.db import models

class Consumer(models.Model):
    STATUS_CHOICES = [
        ('INACTIVE', 'Inactive'),
        ('PAID_IN_FULL', 'Paid In Full'),
        ('IN_COLLECTION', 'In Collection'),
    ]
    consumer_name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=12, decimal_places=2)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_COLLECTION')
    client = models.CharField(max_length=255)
    consumer_address = models.CharField(max_length=255, blank=True)  
    ssn = models.CharField(max_length=11, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.consumer_name} - {self.balance} ({self.status})"
