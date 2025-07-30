from django.shortcuts import render
from .models import Consumer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.paginator import Paginator
import csv
from io import StringIO

class ConsumerListView(APIView):
     def get(self, request):
          # Get query parameters
          min_balance = request.query_params.get('min_balance')
          max_balance = request.query_params.get('max_balance')
          consumer_name = request.query_params.get('consumer_name')
          status_param = request.query_params.get('status')
          page = request.query_params.get('page', 1)  #default page
          page_size = request.query_params.get('page_size', 10) #page size
          
          # Filter queryset
          consumers = Consumer.objects.all().order_by('id')
          if min_balance:
            consumers = consumers.filter(balance__gte=min_balance)
          if max_balance:
            consumers = consumers.filter(balance__lte=max_balance)
          if consumer_name:
            consumers = consumers.filter(consumer_name__icontains=consumer_name)
          if status_param:
            consumers = consumers.filter(status__iexact=status_param)
            
          # Pagination  
          paginator = Paginator(consumers, page_size)  
          try:
               page_obj = paginator.page(page)
          except:
               return Response({"error": "Invalid page number"}, status=status.HTTP_400_BAD_REQUEST)     
            
          # Serialize data  
          data = [
               {
                    'id': consumer.id,
                    "consumer_name": consumer.consumer_name,
                    "balance": str(consumer.balance), 
                    "status": consumer.status,
                    "client": consumer.client,
                    "consumer_address": consumer.consumer_address,
                    "ssn": consumer.ssn,
                    "created_at": consumer.created_at.isoformat()
               } for consumer in page_obj
          ]  
          return Response({
                    "results": data,
                    "count": paginator.count,
                    "num_pages": paginator.num_pages,
                    "current_page": page_obj.number,
                    "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
                    "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None
               })
          
          
class CSVUploadView(APIView):
     def post(self, request):
          if 'file' not in request.FILES:
               return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
          csv_file = request.FILES['file']
          if not csv_file.name.endswith('.csv'):
            return Response({"error": "File must be a CSV"}, status=status.HTTP_400_BAD_REQUEST)

          try:
               file_data = csv_file.read().decode('utf-8')
               csv_reader = csv.DictReader(StringIO(file_data))
               #validate required fields
               required_fields = ['client reference no', 'balance', 'status', 'consumer name', 'consumer address', 'ssn']
               if not all(field in csv_reader.fieldnames for field in required_fields):
                    return Response({"error": "CSV missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
               
               for row in csv_reader:
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
               return Response({"message": "CSV processed successfully"}, status=status.HTTP_201_CREATED)     
               
          
          except Exception as exception:
               return Response({"error": str(exception)}, status=status.HTTP_400_BAD_REQUEST)
               # Create your views here.
