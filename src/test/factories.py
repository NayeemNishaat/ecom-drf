import factory
from ..product.models import Category, Brand, Product, ProductLine


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.sequence(lambda n: "Category_%d" % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.sequence(lambda n: "Brand_%d" % n)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = "test_product"
    description = "Desc"
    is_digital = False
    is_active = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.00
    sku = "12bd"
    stock_quantity = 5
    is_active = True
    product = factory.SubFactory(ProductFactory)
