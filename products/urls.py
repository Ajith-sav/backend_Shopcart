from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<slug:slug>", views.product_detail, name="product_detail"),
    path("search/", views.search_product, name="search_product"),
    path("categories/", views.get_category, name="category-list"),
    path("categories/<int:pk>/", views.category_detail, name="category-detail"),
]
