# Generated by Django 4.2.1 on 2023-06-10 17:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0003_productline_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.SlugField(default="sdf", max_length=255),
            preserve_default=False,
        ),
    ]
