from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="product-list"),
    path("<slug:slug>", views.product_detail, name="product_detail"),
    path("search/", views.search_product, name="search_product"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
