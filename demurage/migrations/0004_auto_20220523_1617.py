# Generated by Django 3.0 on 2022-05-23 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demurage', '0003_auto_20220523_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demuragesize',
            name='size',
            field=models.CharField(choices=[('Dry 20 ft', 'Dry 20 ft'), ('Reefer 20 ft', 'Reefer 20 ft'), ('Special 20 ft', 'Special 20 ft'), ('Dry 40 ft', 'Dry 40 ft'), ('Reefer 40 ft', 'Reefer 40 ft'), ('Special 40 ft', 'Special 40 ft'), ('Dry 45 ft', 'Dry 45 ft'), ('Reefer 45 ft', 'Reefer 45 ft')], max_length=255, unique=True),
        ),
    ]
