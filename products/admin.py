from django.contrib import admin

from .models import Category, Products


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand_name","price", "stock", "available", "created_at", "updated_at")
    list_filter = (
        "name",
        "brand_name",
        "available",
        "price",
        "vendor_id",
        "categories",
        "created_at",
        "updated_at",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "categories")
    raw_id_fields = ("categories",)
    ordering = ("-created_at",)
