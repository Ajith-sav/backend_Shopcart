from django.db.models import Q
from django.shortcuts import render
from django.utils.text import slugify
from rest_framework import permissions, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Category, Products
from .serializers import CategorySerializer, ProductSerializer


@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def product_list(request):
    if request.method == "GET":
        if request.user.is_vendor:
            products = Products.objects.filter(vendor_id=request.user.id)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            products = Products.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if request.user.is_vendor:
            serializer = ProductSerializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )


@api_view(["GET", "POST", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def product_detail(request, slug):

    try:
        product = Products.objects.get(slug=slug)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == "PUT":
        if request.user.is_vendor and product.vendor == request.user.id:
            serializer = ProductSerializer(
                product, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

    elif request.method == "DELETE":
        if request.user.is_vendor and product.vendor == request.user.id:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def search_product(request):
    if request.method == "GET":
        query = request.query_params.get("query", None)
        query_slug = slugify(query)
        if query:
            products = Products.objects.filter(
                Q(slug__icontains=query_slug)
                | Q(brand_name__icontains=query)
                | Q(categories__name__icontains=query)
            ).distinct()
            if request.user.is_vendor:
                product = products.filter(vendor_id=request.user.id)
                serializer = ProductSerializer(product, many=True)
                return Response(serializer.data)

            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
