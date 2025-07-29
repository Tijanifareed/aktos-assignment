from django.db import models

class Consumer(models.Model):
     STATUS_CHOICES = [
          ('in_collection', 'In Collection'),
          ('collected', 'Collected'),
          ('disputed', 'Disputed'),
     ]
     consumer_name = models.CharField(max_length=255)
     balance = models.DecimalField(max_digits=10, decimal_places=2)
     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_collection')
     client = models.CharField(max_length=255)  
     created_at = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
        return f"{self.consumer_name} - {self.balance} ({self.status})"


