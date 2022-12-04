from rest_framework import serializers

from .models import Customer, MailingList


class CustomerSerializer(serializers.ModelSerializer):
    '''
    Serialize and deserialize Customer model instances.
    '''
    class Meta:
        model = Customer
        fields = [
            'phone_number',
            'tag',
            'time_zone',
        ]

class MailingListSerializer(serializers.ModelSerializer):
    '''
    Serialize and deserialize MailingList model instances.
    '''
    class Meta:
        model = MailingList
        fields = [
            'start',
            'stop',
            'message',
            'filter_phone_code',
            'filter_tag',
        ]
