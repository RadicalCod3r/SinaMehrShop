from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import BlogPost
from .serializers import BlogPostSerializer

# Create your views here.
@api_view(['GET'])
def list_blog_posts(request):
    posts = BlogPost.objects.all()
    serializer = BlogPostSerializer(posts, many=True)
    return Response(serializer.data)