# Generated by Django 5.2.2 on 2025-06-16 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0004_classsession_start_date_classsession_weekday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classsession',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='classsession',
            name='weekday',
            field=models.IntegerField(),
        ),
    ]
