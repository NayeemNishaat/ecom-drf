from pytest_factoryboy import register
from .factories import (
    CategoryFactory,
    ProductFactory,
    ProductLineFactory,
    ProductImageFactory,
    AttributeFactory,
    AttributeValueFactory,
    ProductTypeFactory,
    ProductLineAttributeValueFactory,
)
from rest_framework.test import APIClient
import pytest

register(CategoryFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)
register(AttributeFactory)
register(AttributeValueFactory)
register(ProductLineAttributeValueFactory)
register(ProductTypeFactory)


@pytest.fixture
def api_client():
    return APIClient
