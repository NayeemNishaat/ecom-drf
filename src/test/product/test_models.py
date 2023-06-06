import pytest

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        name = category_factory(name="abc")
        assert name.__str__() == "abc"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        name = brand_factory(name="test")
        assert name.__str__() == "test"


class TestProductModel:
    pass
