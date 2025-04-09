import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_products_list():
    username = "user"
    password = "user@123"
    email = "user@gmail.com"
    role = "customer"
    client = APIClient()
    User = get_user_model()

    user = User.objects.create_user(
        username=username, password=password, email=email, role=role
    )
    login_response = client.post(
        reverse("signin"), {"email": email, "password": password}
    )
    print("🧪 Login Response:", login_response.content.decode())
    access_token = login_response.json()["access"]
    assert access_token is not None, "Access token should not be None"

    if access_token:
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = client.get(reverse("product_list"))
        print("🧪 Product Response:", response.json())
        assert response.status_code == 200
