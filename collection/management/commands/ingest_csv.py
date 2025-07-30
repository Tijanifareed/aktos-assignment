import csv
from django.core.management.base import BaseCommand
from ...models import Consumer
import os


class Command(BaseCommand):
     help = 'Ingests consumer data from a CSV file into the database'
     
     def add_arguments(self, parser):
          parser.add_argument('csv_file', type=str, help='Path to the CSV file')
          
     def handle(self, *args, **options):
          csv_file_path = options['csv_file']
          if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file_path}"))
            return   
       
          with open(csv_file_path, 'r', encoding='utf-8') as file:
               reader = csv.DictReader(file)
               self.stdout.write(self.style.WARNING(f"CSV headers: {reader.fieldnames}"))
               for row in reader:
                    balance = float(row['balance'])
                    Consumer.objects.update_or_create(
                         consumer_name=row['consumer name'],
                         client=row['client reference no'],
                         defaults={
                              'balance': balance,
                              'status': row['status'],
                              'consumer_address': row['consumer address'],
                              'ssn': row['ssn']
                         }
                    )
          self.stdout.write(self.style.SUCCESS(f"Successfully ingested data from {csv_file_path}"))
          
# consumers_balances headers = client reference no,balance,status,consumer name,consumer address,ssn
          