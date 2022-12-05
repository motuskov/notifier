from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import render
from django.db.models import Count

from .models import Customer, MailingList
from .serializers import CustomerSerializer
from .serializers import MailingListSerializer
from .serializers import MailingListsStatisticsSerializer
from .serializers import MessageSerializer


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

    @action(detail=True)
    def messages(self, request, pk=None):
        mailing_list = self.get_object()
        queryset = mailing_list.messages.all()
        serializer = MessageSerializer(
            queryset,
            many=True
        )
        return Response(serializer.data)

class MailingListsStatisticsViewSet(viewsets.ViewSet):
    '''
    Provides API for mailing lists statistics.
    '''
    def list(self, request):
        queryset = MailingList.objects.values(
            'pk',
            'messages__status'
        ).annotate(
            messages_count=Count('messages__status')
        ).filter(
            messages_count__gt=0
        )
        serializer = MailingListsStatisticsSerializer(
            queryset,
            many=True
        )
        return Response(serializer.data)

class ActiveMailingListsViewSet(viewsets.ModelViewSet):
    '''
    Provides API for active mailing lists.
    '''
    queryset = MailingList.get_active_mailing_lists()
    serializer_class = MailingListSerializer

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        '''
        Sends message to selected customer.
        '''
        mailing_list = self.get_object()
        serializer = SendMessageSerializer(data=request.data)
        if serializer.is_valid():
            message = Message.send(
                mailing_list,
                serializer.validated_data['customer']
            )
            return Response({'status': message.status})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
