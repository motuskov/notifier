import requests
from rest_framework.renderers import JSONRenderer
from datetime import datetime, timezone, timedelta
import pytz

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from .validators import validate_time_zone


class MailingList(models.Model):
    '''
    Represents parameters for controlling the process of sending
    messages to customers.
    '''
    start = models.DateTimeField(
        help_text='Start date and time of the sending process.'
    )
    stop = models.DateTimeField(
        help_text='End date and time of the sending process.'
    )
    message = models.TextField(
        help_text='Message to send.'
    )
    filter_phone_code = models.CharField(
        max_length=3,
        help_text='Mobile operator phone code for filtering '
        + 'customers, 3 digits.',
        validators=[
            RegexValidator(
                regex='^\d{3}$',
                message='Format should be "XXX" where X is digit.'
            )
        ]
    )
    filter_tag = models.CharField(
        max_length=100,
        help_text='Tag for filtering customers, not more then 100 '
        + 'characters.'
    )

    def clean(self, *args, **kwargs):
        # Checking that stop more than start
        if self.stop <= self.start:
            raise ValidationError(
                'Stop date and time should be more than start date '
                + 'and time.'
            )

        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Cleaning the model
        self.full_clean()

        super().save(*args, **kwargs)

    @classmethod
    def get_active_mailing_lists(cls):
        '''
        Finds mailing lists notification period of witch intersects
        with range of current world local times.

        Return (QuerySet): Active mailing lists
        '''
        # Getting the range of current world local time
        now_utc = datetime.now(timezone.utc)
        now_minimal_world_time = now_utc - timedelta(hours=12)
        now_maximum_world_time = now_utc + timedelta(hours=12)
        # Looking for active mailing lists
        active_mailing_lists = MailingList.objects.exclude(
            stop__lt=now_minimal_world_time
        ).exclude(
            start__gt=now_maximum_world_time
        )

        return active_mailing_lists

    def get_unnotified_customers(self):
        '''
        Finds customers witch have not recieved notification
        according current mailing list.

        Return (QuerySet): Unnotified customers query set
        '''
        notified_customer_pks = Message.objects.filter(
            status='sent',
            mailing_list=self
        ).values_list('customer__pk')
        unnotified_customers = Customer.objects.filter(
            phone_code=self.filter_phone_code,
            tag=self.filter_tag
        ).exclude(
            pk__in=notified_customer_pks
        )
        return unnotified_customers

class Customer(models.Model):
    '''
    Represents a customer.
    '''
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        help_text='Phone number of the customer in format: '
        + '7XXXXXXXXXX.',
        validators=[
            RegexValidator(
                regex=r'^7\d{10}$',
                message='Format should be "7XXXXXXXXXX" where X is '
                + 'digit.'
            )
        ]
    )
    phone_code = models.CharField(
        max_length=3,
        help_text='Mobile operator phone code, 3 digits.',
    )
    tag = models.CharField(
        max_length=100,
        help_text='Tag, not more then 100 characters.'
    )
    time_zone = models.CharField(
        max_length=50,
        help_text='Customer time zone.',
        validators=[
            validate_time_zone,
        ]
    )

    def save(self, *args, **kwargs):
        # Detecting phone code by phone number
        self.phone_code = self.phone_number[1:4]

        super().save(*args, **kwargs)

    def is_local_time_in_range(self, begin, end):
        '''
        Checks if customer local time is in specified range.

        Parameters:
            begin (DateTime): Range begin time
            end (DateTime): Range end time

        Return (bool): If customer local time is in specified range
        '''
        local_time = datetime.now(pytz.timezone(
            self.time_zone
        ))
        return begin < local_time < end

class Message(models.Model):
    '''
    Represents a message sent to a customer.
    '''
    STATUS_CHOICES = [
        ('sent', 'Successfully sent'),
        ('error', 'An error has occurred'),
    ]
    sent = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time the message was sent.'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        help_text='Message sending status.'
    )
    error_description = models.TextField(
        blank=True,
        help_text='Response error description.'
    )
    mailing_list = models.ForeignKey(
        MailingList,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text='Mailing list the message was sent for.'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text='Customer the message was sent to.'
    )

    @classmethod
    def send(cls, mailing_list, customer):
        '''
        Sends message to customer and create DB record.

        Parameters:
            mailing_list (MailingList): Mailing list the message will 
            be send for
            customer (Customer): Customer the message will be send to

        Return (Message): Sent message
        '''
        # Defining constants
        ENDPOINT = 'https://probe.fbrq.cloud/v1/send/1'
        TOKEN = (
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MD'
            'E0Mzc1MTgsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Im1vdHVza'
            '292In0.0hSdfJ69kLfn4aN1HxJXEyR2ZlGValzItYWGoYehHiw'
        )
        # Preparing headers and data
        data = JSONRenderer().render({
            'id': 1,
            'phone': int(customer.phone_number),
            'text': mailing_list.message
        })
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + TOKEN,
            'Content-Type': 'application/json'
        }
        # Sending message
        try:
            response = requests.post(
                ENDPOINT,
                data=data,
                headers=headers
            )
            if response.status_code == 200:
                status = 'sent'
                error_description = ''
            else:
                status = 'error'
                error_description = (
                    f'Response status code: {response.status_code}'
                    '\n\n'
                    f'Response text:\n{response.text}'
                    '\n\n'
                    f'Response headers:\n{response.headers}'
                )
        except Exception as e:
            status = 'error'
            error_description = (f'Exception:\n{e}')
        finally:
            # Creating message instance
            message = cls.objects.create(
                mailing_list=mailing_list,
                customer=customer,
                status=status,
                error_description=error_description
            )

        return message
