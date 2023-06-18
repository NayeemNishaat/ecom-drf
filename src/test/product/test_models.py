import pytest
from django.core.exceptions import ValidationError
from src.product.models import ProductTypeAttribute
from django.db.utils import IntegrityError
from src.product.models import Category, Product, ProductLine

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
        slug = "x" * 256
        obj = category_factory(slug=slug)
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


class TestProductModel:
    def test_str_method(self, product_factory):
        name = product_factory(name="test_product")
        assert name.__str__() == "test_product"

    def test_slug_max_length(self, product_factory):
        slug = "x" * 256
        obj = product_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_is_digital_false_dflt(self, product_factory):
        obj = product_factory()
        assert obj.is_digital is False

    def test_category_delete_protect(self, product_factory, category_factory):
        obj = category_factory()
        product_factory(category=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_return_active_prods(self, product_factory):
        product_factory(is_active=True)
        product_factory(is_active=False)
        qs = Product.objects.isActive().count()  # type:ignore
        dqs = Product.objects.count()
        assert qs == 1
        assert dqs == 2

    def test_fk_product_type_delete_protect(
        self, product_type_factory, product_factory
    ):
        obj = product_type_factory()
        product_factory(product_type=obj)
        with pytest.raises(IntegrityError):
            obj.delete()


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        obj = product_line_factory.create(sku="hh7")
        assert obj.__str__() == "hh7"

    def test_dupli_order_value(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()

    def test_decimal_places(self, product_line_factory):
        price = "1.223"
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_price_max_digits(self, product_line_factory):
        price = "71.557"
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_sku_max_len(self, product_line_factory):
        sku = "x" * 11
        with pytest.raises(ValidationError):
            product_line_factory(sku=sku)

    def test_fk_product_on_delete_protect(self, product_factory, product_line_factory):
        obj = product_factory()
        product_line_factory(product=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_is_active_false_dflt(self, product_line_factory):
        obj = product_line_factory()
        assert obj.is_active is False

    def test_return_active_prodlines(self, product_line_factory):
        product_line_factory(is_active=True)
        product_line_factory(is_active=False)
        qs = ProductLine.objects.isActive().count()  # type:ignore
        dqs = ProductLine.objects.count()
        assert qs == 1
        assert dqs == 2

    def test_fk_product_type_delete_protect(
        self, product_type_factory, product_line_factory
    ):
        obj = product_type_factory()
        product_line_factory(product_type=obj)
        with pytest.raises(IntegrityError):
            obj.delete()


class TestProductImageModel:
    def test_str_method(self, product_image_factory, product_line_factory):
        obj = product_line_factory(sku="46JGK88")
        obj2 = product_image_factory(order=1, product_line=obj)
        assert obj2.__str__() == "46JGK88_img"

    def test_alt_text_max_len(self, product_image_factory):
        alternative_text = "x" * 256
        with pytest.raises(ValidationError):
            product_image_factory(alternative_text=alternative_text)

    def test_dupli_order_value(self, product_line_factory, product_image_factory):
        obj = product_line_factory()
        product_image_factory(order=1, product_line=obj)
        with pytest.raises(ValidationError):
            product_image_factory(order=1, product_line=obj).clean()


class TestProductTypeModel:
    def test_str_method(self, product_type_factory):
        obj = product_type_factory.create(name="test type")

        assert obj.__str__() == "test type"

    def test_name_max_len(self, product_type_factory):
        name = "x" * 256
        with pytest.raises(ValidationError):
            product_type_factory(name=name).full_clean()


# class TestAttributeModel:
#     def test_str_method(self, attribute_factory):
#         obj = attribute_factory(name="test_attribute")
#         assert obj.__str__() == "test_attribute"


# class TestAttributeValueModel:
#     def test_str_method(self, attribute_value_factory, attribute_factory):
#         obj_a = attribute_factory(name="test_attribute")
#         obj_b = attribute_value_factory(value="test_value", attribute=obj_a)
#         assert obj_b.__str__() == "test_attribute - test_value"
