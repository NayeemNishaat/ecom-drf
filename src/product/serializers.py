from rest_framework import serializers
from .models import Brand, Category, Product, ProductImage, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category_name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        # fields = "__all__"
        exclude = ["id"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["id", "product_line"]


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ("price", "sku", "stock_quantity", "order", "product_image")


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(
        source="brand.name"
    )  # Note: Check Product Model to Know the Name
    category_name = serializers.CharField(source="category.name", allow_null=True)
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        # exclude = ("id",)
        fields = (
            "name",
            "slug",
            "description",
            "brand_name",
            "category_name",
            "product_line",
        )
        # fields = "__all__"
