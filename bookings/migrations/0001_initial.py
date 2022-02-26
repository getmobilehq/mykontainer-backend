# Generated by Django 3.0 on 2022-02-26 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateField()),
                ('laden_number', models.CharField(max_length=350)),
                ('container_number', models.CharField(max_length=350)),
                ('container_size', models.CharField(max_length=350)),
                ('drop_off', models.CharField(max_length=6)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('bay_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='main.BayArea')),
                ('shipping_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='main.ShippingCompany')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
