from django.contrib import admin

from .models import *


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'start',
        'stop',
        'filter_phone_code',
        'filter_tag',
        'message',
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'phone_number',
        'phone_code',
        'tag',
        'time_zone',
    )
    exclude = (
        'phone_code',
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'sent',
        'status',
        'mailing_list',
        'customer',
    )
    readonly_fields = (
        'status',
        'mailing_list',
        'customer',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
