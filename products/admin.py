from django.contrib import admin
from .models import (
    Product,
    Category,
    ProductReview,
    Color,
    ProductColor,
    ProductDesign,
    ProductFamily,
    ProductFeature,
    ProductKeyValFeature
)

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductReview)
admin.site.register(Color)
admin.site.register(ProductColor)
admin.site.register(ProductFamily)
admin.site.register(ProductDesign)
admin.site.register(ProductFeature)
admin.site.register(ProductKeyValFeature)