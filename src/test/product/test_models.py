import pytest
from django.core.exceptions import ValidationError

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
    def test_str_method(self, product_factory):
        name = product_factory(name="test_product")
        assert name.__str__() == "test_product"


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        obj = product_line_factory(sku="hh7")
        assert obj.__str__() == "hh7"

    def test_dupli_order_value(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        obj = product_image_factory(order=1)
        assert obj.__str__() == "1"
