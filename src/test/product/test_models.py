import pytest
from django.core.exceptions import ValidationError
from src.product.models import ProductTypeAttribute
from django.db.utils import IntegrityError
from src.product.models import Category

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        name = category_factory(name="abc")
        assert name.__str__() == "abc"

    def test_name_max_length(self, category_factory):
        name = "x" * 236
        obj = category_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, category_factory):
        name = "x" * 256
        obj = category_factory(slug=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_name_unique(self, category_factory):
        category_factory(name="test")
        with pytest.raises(IntegrityError):
            category_factory(name="test")

    def test_slug_unique(self, category_factory):
        category_factory(slug="test")
        with pytest.raises(IntegrityError):
            category_factory(slug="test")

    def test_is_active_false_dflt(self, category_factory):
        obj = category_factory()
        assert obj.is_active is False  # ==

    def test_parent_cat_delete_protect(self, category_factory):
        obj = category_factory()
        category_factory(parent=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_parent_field_null(self, category_factory):
        obj = category_factory()
        assert obj.parent is None

    def test_return_active_cats(self, category_factory):
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.isActive().count()  # type:ignore
        assert qs == 1

    def test_dflt_manager(self, category_factory):
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.count()
        assert qs == 2


# class TestBrandModel:
#     def test_str_method(self, brand_factory):
#         name = brand_factory(name="test")
#         assert name.__str__() == "test"


# class TestProductModel:
#     def test_str_method(self, product_factory):
#         name = product_factory(name="test_product")
#         assert name.__str__() == "test_product"


# class TestProductLineModel:
#     def test_str_method(self, product_line_factory, attribute_value_factory):
#         att = attribute_value_factory(value="test av")
#         obj = product_line_factory.create(sku="hh7", attribute_value=(att,))
#         assert obj.__str__() == "hh7"

#     def test_dupli_order_value(self, product_line_factory, product_factory):
#         obj = product_factory()
#         product_line_factory(order=1, product=obj)
#         with pytest.raises(ValidationError):
#             product_line_factory(order=1, product=obj).clean()


# class TestProductImageModel:
#     def test_str_method(self, product_image_factory):
#         obj = product_image_factory(order=1)
#         assert obj.__str__() == "1"


# class TestProductTypeModel:
#     def test_str_method(self, product_type_factory, attribute_factory):
#         test = attribute_factory(name="test")
#         obj = product_type_factory.create(name="test type", attribute=(test,))

#         x = ProductTypeAttribute.objects.get(id=1)
#         print(x)

#         assert obj.__str__() == "test type"


# class TestAttributeModel:
#     def test_str_method(self, attribute_factory):
#         obj = attribute_factory(name="test_attribute")
#         assert obj.__str__() == "test_attribute"


# class TestAttributeValueModel:
#     def test_str_method(self, attribute_value_factory, attribute_factory):
#         obj_a = attribute_factory(name="test_attribute")
#         obj_b = attribute_value_factory(value="test_value", attribute=obj_a)
#         assert obj_b.__str__() == "test_attribute - test_value"
