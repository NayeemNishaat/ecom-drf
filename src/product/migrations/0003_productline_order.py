# Generated by Django 4.2.1 on 2023-06-10 14:37

from django.db import migrations
import src.product.fields


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_brand_is_active_category_is_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productline",
            name="order",
            field=src.product.fields.OrderField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
