import pytz

from django.core.exceptions import ValidationError


def validate_time_zone(value):
    '''
    Checks if value is a valid time zone name.

    Parameters:
        value (str): Time zone name
    '''
    if value not in pytz.all_timezones_set:
        raise ValidationError(
            f'{value} is not a valid time zone name.'
        )
