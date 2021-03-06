# Generated by Django 3.0 on 2022-05-23 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demurage', '0002_auto_20220523_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='demurage',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ranges', to='demurage.DemurageSize'),
        ),
        migrations.AddField(
            model_name='demuragesize',
            name='free_days',
            field=models.IntegerField(default=0),
        ),
    ]
