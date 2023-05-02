# Generated by Django 4.2 on 2023-05-01 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0003_remove_issuanceaccounting_details_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='costaccountingbalances',
            name='deliver',
        ),
        migrations.AddField(
            model_name='deliverdetail',
            name='cost',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='document.costaccountingbalances', verbose_name='Учет расходов'),
        ),
        migrations.AlterField(
            model_name='costaccountingbalances',
            name='date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата выдачи'),
        ),
        migrations.AlterField(
            model_name='issuanceaccounting',
            name='product_name',
            field=models.CharField(max_length=100, verbose_name='Учета выдачи'),
        ),
    ]
