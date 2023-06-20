from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class IsActiveQuerySet(models.QuerySet):
    def isActive(self):
        return self.filter(is_active=True)


# class ActiveManager(models.Manager):
#     # def get_queryset(self):
#     # return super().get_queryset().filter(is_active=True)
#     def isActive(self):
#         return self.get_queryset().filter(is_active=True)


# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    objects = IsActiveQuerySet.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    pid = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey(
        "Category", null=True, blank=True, on_delete=models.PROTECT
    )
    is_active = models.BooleanField(default=False)
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product_type"
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    attribute_value = models.ManyToManyField(
        "AttributeValue",
        through="ProductAttributeValue",
        related_name="product_attribute_value",
    )

    # objects = models.Manager()
    objects = IsActiveQuerySet.as_manager()
    # isActive = ActiveManager()

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_value"
    )

    def __str__(self):
        return f"{self.attribute.name} - {self.value}"


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    sku = models.CharField(max_length=10)
    stock_quantity = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True)  # type: ignore
    weight = models.FloatField()
    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_value",
    )
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product_line_type"
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    objects = IsActiveQuerySet.as_manager()

    def clean(self):
        try:
            qs = ProductLine.objects.filter(product=self.product)
            for obj in qs:
                if self.id != obj.id and self.order == obj.order:  # type:ignore
                    raise ValidationError("Dupli Error")
        except ObjectDoesNotExist:
            raise ValidationError("Product is required")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)


class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_line_attribute_value_av",
    )
    product_line = models.ForeignKey(
        ProductLine,
        on_delete=models.CASCADE,
        related_name="product_line_attribute_value_pl",
    )

    class Meta:
        unique_together = ("attribute_value", "product_line")

    # Important: Preventing duplicate attribute insert
    def clean(self):
        qs = (
            ProductLineAttributeValue.objects.filter(
                attribute_value=self.attribute_value
            )
            .filter(product_line=self.product_line)
            .exists()
        )

        if not qs:
            iqs = Attribute.objects.filter(
                attribute_value__product_line_attribute_value=self.product_line
            ).values_list("pk", flat=True)

            if self.attribute_value.attribute.id in list(iqs):  # type:ignore
                raise ValidationError("Dupli Error")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLineAttributeValue, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.attribute_value)


class ProductAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_av",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_pl",
    )

    class Meta:
        unique_together = ("attribute_value", "product")

    def __str__(self):
        return f"{self.product} - {self.attribute_value}"


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=255)
    url = models.ImageField(upload_to=None, default="test.jpg")  # type:ignore
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="product_line", blank=True)  # type:ignore

    def clean(self):
        qs = ProductImage.objects.filter(product_line=self.product_line)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:  # type:ignore
                raise ValidationError("Dupli Error")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_line.sku}_img"


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    attribute = models.ManyToManyField(
        Attribute, through="ProductTypeAttribute", related_name="product_type_attribute"
    )

    def __str__(self):
        return str(self.name)


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="product_type_attribute_pt"
    )  # Note: M2M to ProductType
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="product_type_attribute_a"
    )  # Note: One2Many to Attribute

    class Meta:
        unique_together = ("product_type", "attribute")

    def __str__(self):
        return str(self.attribute)
