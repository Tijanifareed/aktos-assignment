from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Consumer
import csv
from io import StringIO

class ConsumerTests(TestCase):
     def setUp(self):
        self.client = APIClient()
        
        # Create dummy data for testing
        Consumer.objects.create(
            consumer_name="John Doe",
            balance=5000.00,
            status="IN_COLLECTION",
            client="client reference no",
            consumer_address="123 Test Street",
            ssn="123-45-6789"
        )
        Consumer.objects.create(
            consumer_name="Jane Smith",
            balance=10000.00,
            status="PAID_IN_FULL",
            client="client reference no",
            consumer_address="456 Test Avenue",
            ssn="987-65-4321"
        )
        
     # Test filtering by min_balance and status
     def test_consumer_list_filter(self):
          response = self.client.get('/consumers/?min_balance=6000&status=IN_COLLECTION')
          self.assertEqual(response.status_code, status.HTTP_200_OK)
          self.assertEqual(len(response.json()['results']), 0)  

          response = self.client.get('/consumers/?min_balance=4000&status=IN_COLLECTION')
          self.assertEqual(response.status_code, status.HTTP_200_OK)
          self.assertEqual(len(response.json()['results']), 1)
          self.assertEqual(response.json()['results'][0]['consumer_name'], "John Doe")


     # Test pagination with page_size=1
     def test_consumer_list_pagination(self):
        response = self.client.get('/consumers/?page=1&page_size=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['num_pages'], 2)
        self.assertEqual(response.json()['current_page'], 1)
        self.assertEqual(response.json()['next_page'], 2)

        response = self.client.get('/consumers/?page=2&page_size=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['consumer_name'], "Jane Smith")

     # Test CSV upload endpoint
     def test_csv_upload(self):
        csv_content = "client reference no,balance,status,consumer name,consumer address,ssn\nclient reference no,3000.00,INACTIVE,Test User,789 Test Lane,111-22-3333"
        csv_file = StringIO(csv_content)
        csv_file.name = "test.csv"
        response = self.client.post('/upload-csv/', {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"message": "CSV processed successfully"})
        self.assertTrue(Consumer.objects.filter(consumer_name="Test User").exists())
# Create your tests here.
