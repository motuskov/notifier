from rest_framework import serializers

from .models import Customer, MailingList, Message


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

class MailingListsStatisticsSerializer(serializers.BaseSerializer):
    '''
    Serialize mailing lists statistics.
    '''
    def to_representation(self, instance):
        return {
            'mailing_list_id': instance['pk'],
            'message_status': instance['messages__status'],
            'message_count': instance['messages_count'],
        }

class MessageSerializer(serializers.ModelSerializer):
    '''
    Serialize and deserialize Message model instances.
    '''
    class Meta:
        model = Message
        fields = [
            'customer',
            'sent',
            'status',
        ]

class SendMessageSerializer(serializers.ModelSerializer):
    '''
    Serialize and deserialize Message model instances for sending
    message.
    '''
    class Meta:
        model = Message
        fields = [
            'customer',
        ]
