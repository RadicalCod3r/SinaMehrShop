from rest_framework import serializers
from .models import (
    Category,
    Product,
    ProductKeyValFeature,
    ProductReview,
    ProductColor,
    Color,
    ProductFeature
)
from django.utils.text import slugify

class ProductReviewSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductReview
        fields = ['product', 'name', 'comment', 'rating', 'created_at', 'is_validated', 'image']

    def get_image(self, obj):
        user = obj.user
        return user.image.url


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class ProductColorSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    color = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductColor
        fields = '__all__'

    def get_product(self, obj):
        return obj.product.pk

    def get_color(self, obj):
        serializer = ColorSerializer(obj.color, many=False)
        return serializer.data


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = '__all__'


class ProductKeyValFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductKeyValFeature
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    design_colors = serializers.SerializerMethodField(read_only=True)
    features = serializers.SerializerMethodField(read_only=True)
    key_val_features = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ProductReviewSerializer(reviews, many=True)
        return serializer.data

    def get_category(self, obj):
        category = obj.category
        return category.name

    def get_design_colors(self, obj):
        design = obj.design
        product_colors = ProductColor.objects.filter(design=design)
        serializer = ProductColorSerializer(product_colors, many=True)
        return serializer.data

    def get_features(self, obj):
        serializer = ProductFeatureSerializer(obj.features, many=True)
        return serializer.data

    def get_key_val_features(self, obj):
        serializer = ProductKeyValFeatureSerializer(obj.key_val_features, many=True)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    # products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    # def get_products(self, obj):
    #     products = obj.products.all()
    #     serializer = ProductSerializer(products, many=True)
    #     return serializer.data