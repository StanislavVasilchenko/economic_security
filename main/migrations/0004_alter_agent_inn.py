# Generated by Django 4.2.7 on 2024-05-08 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_filereport_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='inn',
            field=models.CharField(max_length=12, verbose_name='ИНН'),
        ),
    ]