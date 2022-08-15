from unicodedata import decimal
from django.shortcuts import render
from django.utils.text import slugify

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import (
    Category,
    Product,
    ProductReview
)
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductReviewSerializer
)

# Create your views here.
@api_view(['GET'])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_products(request):
    sort = request.query_params.get('sort')
    query = request.query_params.get('q')
    min_price = request.query_params.get('minPrice')
    max_price = request.query_params.get('maxPrice')

    if query == None or query == '':
        query = ''

    if sort == None or sort == '':
        sort = ''

    if min_price == None or min_price == '':
        min_price = 0

    if max_price == None or max_price == '':
        max_price = 10000000

    products = Product.objects.filter(name__icontains=query, price__gte=int(min_price), price__lte=int(max_price))

    order = ''
    if sort == '1':
        order = '-created_at'
    elif sort == '2':
        order = '-rating'
    elif sort == '3':
        order = '-created_at'
    else:
        order = '-created_at'

    products = products.order_by(order)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_category(request, pk):
    category = Category.objects.filter(pk=pk)

    print(category)

    if category.exists():
        category = category.first()
        
        sort = request.query_params.get('sort')
        min_price = request.query_params.get('minPrice')
        max_price = request.query_params.get('maxPrice')        

        if sort == None:
            sort = ''

        if min_price == None or min_price == '':
            min_price = 0

        if max_price == None or max_price == '':
            max_price = 10000000            

        order = ''
        if sort == '1':
            order = '-created_at'
        elif sort == '2':
            order = '-rating'
        elif sort == '3':
            order = '-created_at'
        else:
            order = '-created_at'

        category_serializer = CategorySerializer(category, many=False)

        products = category.products.all().filter(price__gte=int(min_price), price__lte=int(max_price))        
        products = products.order_by(order)
        product_serializer = ProductSerializer(products, many=True)

        return Response({'category': category_serializer.data, 'products': product_serializer.data})
    else:
        return Response({'detail': 'این دسته بندی وجود ندارد'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_product(request, pk):
    product = Product.objects.filter(pk=pk)

    if product.exists():
        product = product.first()
        serializer = ProductSerializer(product, many=False)

        return Response(serializer.data)
    else:
        return Response({'detail': 'چنین محصولی وجود ندارد.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def comment_on_product(request, pk):
    user = request.user
    data = request.data

    product = Product.objects.filter(id=pk)

    if product.exists():
        product = product.first()

        review = ProductReview.objects.create(
            user = user,
            product = product,
            name = data['name'],
            comment = data['comment'],
            rating = int(data['rating'])
        )

        product.rating = ((product.rating * product.num_ratings) + int(review.rating))/(product.num_ratings + 1)
        product.num_ratings = product.num_ratings + 1
        product.save()

        return Response({'detail': 'دیدگاه شما با موفقیت ثبت شد تا توسط مدیر سایت بررسی شود.'})
    else:
        return Response({'detail': 'چنین محصولی وجود ندارد.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_product_reviews(request, pk):
    product = Product.objects.filter(pk=pk)

    if product.exists():
        product = product.first()
        reviews = product.reviews.all()

        if len(reviews) > 0:
            serializer = ProductReviewSerializer(reviews, many=True)
            return Response({'num_reviews': len(reviews), 'reviews': serializer.data})
        else:
            return Response({'detail': 'تا کنون هیچ دیدگاهی برای این محصول ثبت نشده', 'num_reviews': 0})
    else:
        return Response({'detail': 'چنین محصولی وجود ندارد.'}, status=status.HTTP_404_NOT_FOUND)