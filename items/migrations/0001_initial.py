# Generated by Django 3.2.20 on 2023-10-18 10:49

from django.db import migrations, models
import django.db.models.deletion
import items.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=items.models.upload_image)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('actual_price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('currency', models.CharField(choices=[('UAH', 'UAH'), ('USD', 'USD'), ('EUR', 'EUR')], default='USD', max_length=3)),
                ('sku', models.CharField(blank=True, max_length=32, null=True)),
                ('image', models.ImageField(default='static/images/products/no_image.jpg', upload_to=items.models.upload_image)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.category')),
                ('items', models.ManyToManyField(blank=True, to='items.Item')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
