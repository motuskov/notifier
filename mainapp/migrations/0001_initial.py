# Generated by Django 3.2.16 on 2022-12-04 10:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(help_text='Phone number of the customer in format: 7XXXXXXXXXX.', max_length=11, validators=[django.core.validators.RegexValidator(message='Format should be "7XXXXXXXXXX" where X is digit.', regex='^7\\d{10}$')])),
                ('phone_code', models.CharField(help_text='Mobile operator phone code, 3 digits.', max_length=3, validators=[django.core.validators.RegexValidator(message='Format should be "XXX" where X is digit.', regex='^\\d{3}$')])),
                ('tag', models.CharField(help_text='Tag, not more then 100 characters.', max_length=100)),
                ('time_zone', models.CharField(help_text='Customer time zone.', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(help_text='Start date and time of the sending process.')),
                ('stop', models.DateTimeField(help_text='End date and time of the sending process.')),
                ('message', models.TextField(help_text='Message to send.')),
                ('filter_phone_code', models.CharField(help_text='Mobile operator phone code for filtering customers, 3 digits.', max_length=3, validators=[django.core.validators.RegexValidator(message='Format should be "XXX" where X is digit.', regex='^\\d{3}$')])),
                ('filter_tag', models.CharField(help_text='Tag for filtering customers, not more then 100 characters.', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent', models.DateTimeField(auto_now_add=True, help_text='Date and time the message was sent.')),
                ('status', models.CharField(choices=[('sent', 'Successfully sent'), ('error', 'An error has occurred')], help_text='Message sending status.', max_length=20)),
                ('customer', models.ForeignKey(help_text='Customer the message was sent to.', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mainapp.customer')),
                ('mailing_list', models.ForeignKey(help_text='Mailing list the message was sent for.', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mainapp.mailinglist')),
            ],
        ),
    ]