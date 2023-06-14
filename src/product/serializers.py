from rest_framework import serializers
from .models import (
    Brand,
    Category,
    Product,
    ProductImage,
    ProductLine,
    Attribute,
    AttributeValue,
)


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


class AttributeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="name")

    class Meta:
        model = Attribute
        fields = ("name",)


class AttributeValueSerializer(serializers.ModelSerializer):
    # attribute = AttributeSerializer(many=False)
    name = serializers.CharField(source="attribute.name")
    id = serializers.IntegerField(source="attribute.id")

    class Meta:
        model = AttributeValue
        fields = ("name", "value", "id")


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute = AttributeValueSerializer(many=True, source="attribute_value")

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_quantity",
            "order",
            "product_image",
            "attribute",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.get("attribute")
        attr_values = {}

        for key in av_data:  # type:ignore
            attr_values.update({key["id"]: key["value"]})

        data.update({"specification": attr_values})
        return data


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
