# Generated by Django 2.2.3 on 2020-05-22 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='цена услуги')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='доступное количество')),
                ('is_active', models.BooleanField(default=True, verbose_name='активен')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.ServiceCategory')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
    ]
