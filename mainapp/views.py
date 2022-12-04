from rest_framework import viewsets

from django.shortcuts import render

from .models import Customer, MailingList
from .serializers import CustomerSerializer, MailingListSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    '''
    Provides API for Customer entity.
    '''
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class MailingListViewSet(viewsets.ModelViewSet):
    '''
    Provides API for MailingList entity.
    '''
    queryset = MailingList.objects.all()
    serializer_class = MailingListSerializer
