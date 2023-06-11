from django.contrib import admin
from .models import Category, Brand, Product, ProductLine


class ProductLineInline(admin.TabularInline):
    model = ProductLine


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductLine)

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
