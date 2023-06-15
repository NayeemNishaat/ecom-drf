from pytest_factoryboy import register
from .factories import (
    CategoryFactory,
    BrandFactory,
    ProductFactory,
    ProductLineFactory,
    ProductImageFactory,
    AttributeFactory,
    AttributeValueFactory,
    ProductTypeFactory,
)
from rest_framework.test import APIClient
import pytest

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)
register(AttributeFactory)
register(AttributeValueFactory)
register(ProductTypeFactory)


@pytest.fixture
def api_client():
    return APIClient
