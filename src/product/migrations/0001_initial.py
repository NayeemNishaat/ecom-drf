# Generated by Django 4.2.1 on 2023-06-17 11:58

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import src.product.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Attribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="AttributeValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=100)),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attribute_value",
                        to="product.attribute",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=235, unique=True)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("is_active", models.BooleanField(default=False)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="product.category",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=255)),
                ("pid", models.CharField(max_length=10, unique=True)),
                ("description", models.TextField(blank=True)),
                ("is_digital", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "category",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="product.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductLine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("sku", models.CharField(max_length=100)),
                ("stock_quantity", models.IntegerField()),
                ("is_active", models.BooleanField(default=False)),
                ("order", src.product.fields.OrderField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProductType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="ProductTypeAttribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_type_attribute_a",
                        to="product.attribute",
                    ),
                ),
                (
                    "product_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_type_attribute_pt",
                        to="product.producttype",
                    ),
                ),
            ],
            options={
                "unique_together": {("product_type", "attribute")},
            },
        ),
        migrations.AddField(
            model_name="producttype",
            name="attribute",
            field=models.ManyToManyField(
                related_name="product_type_attribute",
                through="product.ProductTypeAttribute",
                to="product.attribute",
            ),
        ),
        migrations.CreateModel(
            name="ProductLineAttributeValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attribute_value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_line_attribute_value_av",
                        to="product.attributevalue",
                    ),
                ),
                (
                    "product_line",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_line_attribute_value_pl",
                        to="product.productline",
                    ),
                ),
            ],
            options={
                "unique_together": {("attribute_value", "product_line")},
            },
        ),
        migrations.AddField(
            model_name="productline",
            name="attribute_value",
            field=models.ManyToManyField(
                related_name="product_line_attribute_value",
                through="product.ProductLineAttributeValue",
                to="product.attributevalue",
            ),
        ),
        migrations.AddField(
            model_name="productline",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_line",
                to="product.product",
            ),
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("alternative_text", models.CharField(max_length=255)),
                ("url", models.ImageField(default="test.jpg", upload_to=None)),
                ("order", src.product.fields.OrderField(blank=True)),
                (
                    "product_line",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_image",
                        to="product.productline",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="product_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="product",
                to="product.producttype",
            ),
        ),
    ]
