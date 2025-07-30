from django.shortcuts import render
from .models import Consumer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

class ConsumerListView(APIView):
     def get(self, request):
          min_balance = request.query_params.get('min_balance')
          max_balance = request.query_params.get('max_balance')
          consumer_name = request.query_params.get('consumer_name')
          status_param = request.query_params.get('status')
          
          
          consumers = Consumer.objects.all()
          if min_balance:
            consumers = consumers.filter(balance__gte=min_balance)
          if max_balance:
            consumers = consumers.filter(balance__lte=max_balance)
          if consumer_name:
            consumers = consumers.filter(consumer_name__icontains=consumer_name)
          if status_param:
            consumers = consumers.filter(status__iexact=status_param)
            
            
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
               } for consumer in consumers
          ]  
          return Response(data)


# Create your views here.
