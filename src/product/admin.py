from django.contrib import admin
from .models import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    AttributeValue,
    Attribute,
    ProductType,
    ProductAttributeValue,
    ProductLineAttributeValue,
    ProductTypeAttribute,
)
from django.urls import reverse
from django.utils.safestring import mark_safe


class EditLinkInline(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=[instance.pk],
        )
        if instance.pk:
            link = mark_safe('<a href="{url}">edit</a>'.format(url=url))
            return link
        else:
            return ""


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductLineInline(EditLinkInline, admin.TabularInline):
    model = ProductLine
    readonly_fields = ("edit",)


# @admin.register(Product)


class AttributeValueProductLineInline(admin.TabularInline):
    model = AttributeValue.product_line_attribute_value.through  # type:ignore


class AttributeValueProductInline(admin.TabularInline):
    model = AttributeValue.product_attribute_value.through  # type:ignore

    # def formfield_for_choice_field(self, db_field, request, **kwargs):
    #     print(67777)
    #     print(db_field)
    #     return super().formfield_for_choice_field(db_field, request, **kwargs)
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        print(db_field)
        kwargs["queryset"] = AttributeValue.objects.filter(id=1)
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline, AttributeValueProductInline]

    # def formfield_for_choice_field(self, db_field, request, **kwargs):
    #     print(67777)
    #     print(db_field)
    #     return super().formfield_for_choice_field(db_field, request, **kwargs)

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "attribute_value":
    #         # kwargs["queryset"] = self.get_queryset(request).filter(id=100)
    #         kwargs["queryset"] = AttributeValue.objects.filter(id=1)
    #         # qs = self.get_queryset(request).filter(id=1)
    #         # print(kwargs)
    #         print(db_field)
    #         # print(super().formfield_for_choice_field())
    #         # return super().formfield_for_choice_field(db_field, request, **kwargs)


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, AttributeValueProductLineInline]


class AttributeInline(admin.TabularInline):
    model = Attribute.product_type_attribute.through  # type:ignore


class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [AttributeInline]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Attribute)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(AttributeValue)


# django-admin startproject src .
# ./manage.py startapp product ./src/product
# ./manage.py runserver
# ./manage.py makemigrations
# ./manage.py migrate
# sqlite3 db.sqlite3
# ./manage.py createsuperuser
# ./manage.py spectacular --fileschema.yaml
# export DJANGO_SETTINGS_MODULE=src.local
# pytest -k test_category_get
# pytest -x
