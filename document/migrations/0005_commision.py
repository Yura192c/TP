# Generated by Django 4.2 on 2023-05-17 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0004_remove_costaccountingbalances_deliver_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100, verbose_name='Должность')),
                ('full_name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('cost', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='document.costaccountingbalances', verbose_name='Учет расходов')),
            ],
            options={
                'verbose_name': 'Комиссия выдачи',
                'verbose_name_plural': 'Комиссия выдачи',
            },
        ),
    ]
