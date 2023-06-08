from django.contrib import admin
from .models import Category, Brand, Product

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)

# django-admin startproject src .
# ./manage.py startapp product ./src/product
# ./manage.py runserver
# ./manage.py makemigrations
# ./manage.py migrate
# sqlite3 db.sqlite3
# ./manage.py createsuperuser
# ./manage.py spectacular --fileschema.yaml
# export DJANGO_SETTINGS_MODULE=src.local
