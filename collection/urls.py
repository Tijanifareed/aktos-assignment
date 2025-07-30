from django.urls import path
from .views import ConsumerListView

urlpatterns = [
    path('consumers/', ConsumerListView.as_view(), name='consumer_list'),
]