from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer
from drf_spectacular.utils import extend_schema
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer
from sqlparse import format
from django.db import connection


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(
    viewsets.ViewSet
):  # ModelViewSet will create all CRUD APIs and ViewSet will only create the get API
    queryset = Product.objects.isActive()
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug).select_related(
                "category", "brand"
            ),  # Important: Select related won't work for reverse fk relationship ("product_line") to avoid N + 1 problem we can use prefetch_related()
            many=True,
        )

        # Note: Formatting SQL
        # formattedSql = format(str(self.queryset.filter(slug=slug).query), reindent=True)
        # print(highlight(formattedSql, SqlLexer(), TerminalFormatter()))

        data = Response(
            serializer.data
        )  # Remark: Storing response to data so that we can measure how many queries ran.

        q = list(connection.queries)
        print(len(q))
        for q in q:
            print(
                highlight(
                    format(str(q["sql"]), reindent=True),
                    SqlLexer(),
                    TerminalFormatter(),
                )
            )

        return data

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        """ViewSet for viewing all products"""

        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"(?P<category>\w+)/all",
    )
    def list_by_category(self, request, category=None):
        """ViewSet for getting products by category"""

        serializer = ProductSerializer(
            self.queryset.filter(category__name=category), many=True
        )
        return Response(serializer.data)
