# Generated by Django 2.2.3 on 2019-07-13 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0003_auto_20190713_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
