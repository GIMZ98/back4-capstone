# Generated by Django 4.0.5 on 2024-01-27 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_sale_sale_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='vin',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
