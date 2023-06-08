from pytest_factoryboy import register
from .factories import CategoryFactory, BrandFactory, ProductFactory
from rest_framework.test import APIClient
import pytest

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)


@pytest.fixture
def api_client():
    return APIClient
