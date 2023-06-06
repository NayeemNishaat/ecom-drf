from pytest_factoryboy import register
from .factories import CategoryFactory, BrandFactory

register(CategoryFactory)
register(BrandFactory)
