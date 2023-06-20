from rest_framework import serializers
from .models import (
    Category,
    Product,
    ProductImage,
    ProductLine,
    Attribute,
    AttributeValue,
)


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category", "slug"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["id", "product_line"]


class ProductLineCategorySerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ("price", "product_image")


class ProductCategorySerializer(serializers.ModelSerializer):
    product_line = ProductLineCategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ("name", "slug", "pid", "created_at", "product_line")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        x = data.pop("product_line")

        if x:
            price = x[0]["price"]
            image = x[0]["product_image"]
            data.update({"price": price})
            data.update({"image": image})

        return data


class AttributeSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Attribute
        fields = ("name", "id")


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
    category_name = serializers.CharField(source="category.name", allow_null=True)
    product_line = ProductLineSerializer(many=True)
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # exclude = ("id",)
        fields = (
            "name",
            "slug",
            "description",
            "category_name",
            "product_line",
            "attribute",
        )
        # fields = "__all__"

    def get_attribute(self, obj):
        attribute = Attribute.objects.filter(product_type_attribute__product__id=obj.id)
        return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute")
        attr_values = {}

        for key in av_data:  # type:ignore
            attr_values.update({key["id"]: key["name"]})

        data.update({"type_specification": attr_values})
        return data
