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
