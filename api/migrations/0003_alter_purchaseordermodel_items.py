# Generated by Django 4.2.7 on 2023-12-04 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_po_number_purchaseordermodel_po_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseordermodel',
            name='items',
            field=models.TextField(),
        ),
    ]
