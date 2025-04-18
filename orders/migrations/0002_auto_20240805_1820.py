# Generated by Django 3.2.20 on 2024-08-05 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_auto_20240805_1820'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitemrelation',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='items.size'),
        ),
        migrations.AlterUniqueTogether(
            name='orderitemrelation',
            unique_together={('order', 'item', 'size')},
        ),
    ]
