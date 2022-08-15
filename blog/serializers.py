from rest_framework import serializers
from .models import BlogPost, PostReview, Tag

class PostReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReview
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'

    def get_author(self, obj):
        name = obj.author.name

        if name == '':
            name = 'ادمین'

        return name

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = PostReviewSerializer(reviews, many=True)
        return serializer.data

    def get_tags(self, obj):
        tags = obj.tags.all()
        serializer = TagSerializer(tags, many=True)
        return serializer.data