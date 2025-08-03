from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from rest_framework import permissions, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from modules.products.models import *
from modules.products.serializers import *


def is_owner(request, product):
    return request.user.role == "vendor" and product.vendor_id == request.user.id


# Category Views
@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_category(request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        if request.user.role == "vendor":
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == "PUT":
        if request.user.role == "vendor":
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if request.user.role == "vendor" or request.user.role == "admin":
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


# Product Views
@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def product_list(request):
    if request.method == "GET":
        if request.user.role == "vendor":
            products = Products.objects.filter(vendor_id=request.user.id)
            serializer = ProductSerializer(
                products, context={"request": request}, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            products = Products.objects.all()
            serializer = ProductSerializer(
                products, context={"request": request}, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if request.user.role == "vendor":
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


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def product_detail(request, slug):

    product = get_object_or_404(Products, slug=slug)

    if request.method == "GET":
        serializer = ProductSerializer(
            product,
            context={"request": request},
        )
        return Response(serializer.data)

    elif request.method == "PUT":
        if is_owner(request, product):
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
        if is_owner(request, product) or (request.user.role == "admin"):
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )


# Search
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
            if request.user.role == "vendor":
                product = products.filter(vendor_id=request.user.id)
                serializer = ProductSerializer(
                    product, context={"request": request}, many=True
                )
                return Response(serializer.data)

            serializer = ProductSerializer(
                products, context={"request": request}, many=True
            )
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
