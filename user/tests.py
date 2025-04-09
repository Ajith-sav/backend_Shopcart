import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_user_login(client, django_user_model):
    email = "user@gmail.com"
    password = "user@123"
    username = "user"
    user = django_user_model.objects.create_user(
        email=email, password=password, username=username
    )
    response = client.post(reverse("signin"), {"email": email, "password": password})

    # print("📨 Response status:", response.status_code)
    # print("📄 Response content:", response.content.decode())

    assert response.status_code == 200
