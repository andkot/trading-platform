# Generated by Django 3.1.2 on 2020-10-27 07:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0003_auto_20201027_0715'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10, validators=[django.core.validators.MinValueValidator(0.1)]),
        ),
    ]
