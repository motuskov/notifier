# Generated by Django 3.2.16 on 2022-12-05 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20221204_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='error_description',
            field=models.TextField(blank=True, help_text='Response error description.'),
        ),
    ]
