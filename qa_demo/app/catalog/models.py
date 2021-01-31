from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=500, verbose_name="Producto")
    link = models.URLField(max_length=2000, verbose_name="Link de Producto")
    classification = models.CharField(max_length=500, verbose_name="Clasificación")
    product_type = models.CharField(max_length=500, verbose_name="Tipo")
    brand = models.CharField(
        max_length=500, verbose_name="Marca", blank=True, null=True
    )
    vendor_link = models.URLField(
        max_length=2000, blank=True, null=True, verbose_name="Enlace Vendedor"
    )
    vendor_name = models.CharField(
        max_length=500, verbose_name="Vendedor", blank=True, null=True
    )
    vendor_sales = models.CharField(
        max_length=500, verbose_name="Ventas", blank=True, null=True
    )
    vendor_location = models.CharField(
        max_length=500, verbose_name="Ubicación", blank=True, null=True
    )

    class Meta:
        db_table = "product_catalog"
        ordering = ("name",)
