from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Product, ProductLine, ProductImage
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductCategorySerializer,
)
from drf_spectacular.utils import extend_schema
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer
from sqlparse import format
from django.db import connection
from django.db.models import Prefetch


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all().isActive()  # type:ignore

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(
    viewsets.ViewSet
):  # ModelViewSet will create all CRUD APIs and ViewSet will only create the get API
    queryset = Product.objects.all().isActive()  # type:ignore
    # queryset = Product.isActive.all()
    # queryset = Product.objects.isActive()
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug)
            .prefetch_related(Prefetch("attribute_value__attribute"))
            .prefetch_related(Prefetch("product_line__product_image"))
            .prefetch_related(
                Prefetch("product_line__attribute_value__attribute")
            ),  # Important: Select related won't work for reverse fk relationship ("product_line") to avoid N + 1 problem we can use prefetch_related()
            many=True,
        )

        # Note: Formatting SQL
        # formattedSql = format(str(self.queryset.filter(slug=slug).query), reindent=True)
        # print(highlight(formattedSql, SqlLexer(), TerminalFormatter()))

        data = Response(
            serializer.data
        )  # Remark: Storing response to data so that we can measure how many queries ran.

        # q = list(connection.queries)
        # print(len(q))
        # for q in q:
        #     print(
        #         highlight(
        #             format(str(q["sql"]), reindent=True),
        #             SqlLexer(),
        #             TerminalFormatter(),
        #         )
        #     )

        return data

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        """ViewSet for viewing all products"""

        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<cat_slug>[\w-]+)",
    )
    def list_by_category_slug(self, request, cat_slug=None):
        """ViewSet for getting products by category"""

        serializer = ProductCategorySerializer(
            self.queryset.filter(category__slug=cat_slug)
            .prefetch_related(
                Prefetch("product_line", queryset=ProductLine.objects.order_by("order"))
            )
            .prefetch_related(
                Prefetch(
                    "product_line__product_image",
                    queryset=ProductImage.objects.filter(order=1),
                )
            ),
            many=True,
        )

        return Response(serializer.data)
