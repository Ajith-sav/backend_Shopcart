from django.urls import path

from modules.orders.views import *


urlpatterns = [
    path("", OrderListCreateView.as_view(), name="order-list-create"),
    path(
        "<int:pk>/",
        OrderRetrieveUpdateDestroyView.as_view(),
        name="order-retrieve-update-destroy",
    ),
    path(
        "<int:order_id>/items/",
        OrderItemListCreateView.as_view(),
        name="orderitem-list-create",
    ),
    path(
        "items/<int:pk>/",
        OrderItemRetrieveUpdateDestroyView.as_view(),
        name="orderitem-retrieve-update-destroy",
    ),
]
