import factory
from ..product.models import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    ProductType,
    Attribute,
    AttributeValue,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.sequence(lambda n: "Category_%d" % n)
    slug = factory.sequence(lambda n: "test_slug_%d" % n)


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = "test_attribute"
    description = "test_attribute_description"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = factory.sequence(lambda n: "type_%d" % n)

    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute.add(*extracted)  # type:ignore


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.sequence(lambda n: "test_product_%d" % n)
    pid = factory.sequence(lambda n: "pid_%d" % n)
    description = "Desc"
    is_digital = False
    is_active = True
    category = factory.SubFactory(CategoryFactory)
    product_type = factory.SubFactory(ProductTypeFactory)


# class AttributeValueFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = AttributeValue

#     value = "attr_value"
#     attribute = factory.SubFactory(AttributeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.00
    sku = "12bd"
    stock_quantity = 5
    is_active = False
    product = factory.SubFactory(ProductFactory)
    weight = 10
    product_type = factory.SubFactory(ProductTypeFactory)

    # @factory.post_generation
    # def attribute_value(self, create, extracted, **kwargs):
    #     if not create or not extracted:
    #         return
    #     self.attribute_value.add(*extracted)  # type:ignore


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = "alt text"
    url = "any.png"
    product_line = factory.SubFactory(ProductLineFactory)
