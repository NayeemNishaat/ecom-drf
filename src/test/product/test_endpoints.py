import pytest
import json

pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    endpoint = "/api/category/"  # Lame

    def test_category_get(self, category_factory, api_client):
        category_factory.create_batch(4, is_active=True)
        response = api_client().get(self.endpoint)

        # print(json.loads(response.content))  # Remark: To print use pytest -s

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4


class TestProductEndpoints:
    endpoint = "/api/product/"  # Lame

    def test_product_get(self, product_factory, api_client):
        product_factory.create_batch(4)
        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_product_get_by_slug(self, product_factory, api_client):
        obj = product_factory(slug="my-slug")
        response = api_client().get(f"{self.endpoint}{obj.slug}/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_product_get_by_category_slug(
        self, product_factory, category_factory, api_client
    ):
        obj = category_factory(slug="my-cat")
        product_factory(category=obj)

        response = api_client().get(f"{self.endpoint}category/{obj.slug}/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1
