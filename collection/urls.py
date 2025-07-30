from django.urls import path
from .views import CSVUploadView, ConsumerListView

urlpatterns = [
    path('consumers/', ConsumerListView.as_view(), name='consumer_list'),
    path('upload-csv/', CSVUploadView.as_view(), name='upload-csv'),
    
]