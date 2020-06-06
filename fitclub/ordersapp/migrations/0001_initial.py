# Generated by Django 2.2.3 on 2020-05-29 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0002_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Календарная дата',
            },
        ),
        migrations.CreateModel(
            name='TimePeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Период времени',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='доступное количество')),
                ('is_active', models.BooleanField(default=True, verbose_name='активен')),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordersapp.CalendarDate')),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.Service')),
                ('time_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordersapp.TimePeriod')),
            ],
        ),
    ]
