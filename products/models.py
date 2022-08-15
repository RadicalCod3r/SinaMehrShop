from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    image = models.ImageField(upload_to='images/categories', default='images/categories/sample_category.png')
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    color_code = models.CharField(max_length=6, null=True, blank=True)
    is_complex = models.BooleanField(default=False)
    color_code1 = models.CharField(max_length=6, null=True, blank=True)
    color_code2 = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductFamily(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ProductDesign(models.Model):
    family = models.ForeignKey(ProductFamily, on_delete=models.CASCADE, related_name='family_designs')
    use = models.CharField(max_length=100)

    class Meta:
        unique_together = ('family', 'use')

    def __str__(self):
        return f'{self.family} {self.use}'


class ProductColor(models.Model):
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='product_color')
    design = models.ForeignKey(ProductDesign, on_delete=models.CASCADE, related_name='product_colors')

    def __str__(self):
        return f'{self.design} | {self.color}'


class ProductFeature(models.Model):
    feature = models.CharField(max_length=200, null=False, blank=False, unique=True)

    def __str__(self):
        return self.feature


class ProductKeyValFeature(models.Model):
    key = models.CharField(max_length=50, null=False, blank=False)
    value = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        unique_together = ('key', 'value')

    def __str__(self):
        return f'{self.key} : {self.value}'


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    code = models.CharField(max_length=7, blank=True, null=True, unique=True)
    image = models.ImageField(upload_to='images/products', default='images/products/sample_product.png')
    price = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000000)], null=False, blank=False)
    description = models.TextField()
    count_in_stock = models.IntegerField(default=0)
    num_sold = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    num_ratings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True, allow_unicode=True)
    design = models.ForeignKey(ProductDesign, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    product_color = models.OneToOneField(ProductColor, on_delete=models.CASCADE, related_name='product', null=True, blank=True)
    features = models.ManyToManyField(ProductFeature);
    key_val_features = models.ManyToManyField(ProductKeyValFeature)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')
    name = models.CharField(max_length=50, default='کاربر جدید')
    comment = models.TextField(max_length=400)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at',]

    def __str__(self):
        return f'User {self.user.full_name}, Product {self.product}, Rating {self.rating}'
