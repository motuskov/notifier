from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from django.conf import settings
from django.core.management.base import BaseCommand

from mainapp.models import MailingList, Message


def send_messages():
    '''
    Sends messages to customers according to mailing lists.
    '''
    # Looking for active mailing lists
    active_mailing_lists = MailingList.get_active_mailing_lists()
    # Getting unnotified customers and sending them the message
    for active_mailing_list in active_mailing_lists:
        # Getting unnotified customers
        unnotified_customers = active_mailing_list.get_unnotified_customers()
        # Sending message to every customer if its local time fits
        for unnotified_customer in unnotified_customers:
            if unnotified_customer.is_local_time_in_range(
                active_mailing_list.start,
                active_mailing_list.stop
            ):
                Message.send(
                    active_mailing_list,
                    unnotified_customer
                )

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    '''
    Deletes APScheduler job execution entries older than 'max_age'
    from the database.
    '''
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = 'Runs scheduler.'

    def handle(self, *args, **options):
        # Creating scheduler
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        # Adding jobs
        scheduler.add_job(
            send_messages,
            trigger=CronTrigger(minute='*/1'),
            id='send_messages',
            max_instances=1,
            replace_existing=True
        )
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week='mon', hour='00', minute='00'
            ),
            id='delete_old_job_executions',
            max_instances=1,
            replace_existing=True
        )
        # Starting scheduler
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
