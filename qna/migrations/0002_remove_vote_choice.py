# Generated by Django 2.2.3 on 2019-07-13 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='choice',
        ),
    ]
