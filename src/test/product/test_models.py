import pytest
from django.core.exceptions import ValidationError
from src.product.models import ProductTypeAttribute

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
    def test_str_method(self, product_line_factory, attribute_value_factory):
        att = attribute_value_factory(value="test av")
        obj = product_line_factory.create(sku="hh7", attribute_value=(att,))
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


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        test = attribute_factory(name="test")
        obj = product_type_factory.create(name="test type", attribute=(test,))

        x = ProductTypeAttribute.objects.get(id=1)
        print(x)

        assert obj.__str__() == "test type"


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        obj = attribute_factory(name="test_attribute")
        assert obj.__str__() == "test_attribute"


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory, attribute_factory):
        obj_a = attribute_factory(name="test_attribute")
        obj_b = attribute_value_factory(value="test_value", attribute=obj_a)
        assert obj_b.__str__() == "test_attribute - test_value"
