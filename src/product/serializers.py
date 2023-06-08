from rest_framework import serializers
from .models import Brand, Category, Product, ProductLine


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


class ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLine
        exclude = ["id", "is_active", "product"]
        # fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(
        source="brand.name"
    )  # Note: Check Product Model to Know the Name
    category_name = serializers.CharField(source="category.name")
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
