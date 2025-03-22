import pytest
import requests_mock
from django.urls import reverse
from rest_framework.test import APIClient
from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer


@pytest.fixture
def payment_instance():
    """
    Fixture to create a Payment instance for testing.
    """
    payment = Payment.objects.create(
        name="John Doe",
        email="test@mail.com",
        amount=100.50,
        ref="test_ref"
    )
    return payment


@pytest.mark.django_db
def test_payment_creation(requests_mock):
    # Mock the Paystack API response
    paystack_response = {
        "status": True,
        "message": "Authorization URL created",
        "data": {"authorization_url": "https://paystack.com/authorize/12345"},
    }

    requests_mock.post(
        "https://api.paystack.co/transaction/initialize",
        json=paystack_response,
        status_code=200,
    )

    client = APIClient()
    url = reverse("api:payment-list", kwargs={"version": "v1"})
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "amount": 100.50,
    }

    # Make the POST request
    response = client.post(
        url, data, format="json", HTTP_ACCEPT="application/json; version=v1"
    )

    # Assert the response
    assert response.status_code == 201
    assert "payment_url" in response.data
    assert response.data["payment_url"] == "https://paystack.com/authorize/12345"
    assert "details" in response.data
    assert response.data["details"]["name"] == "John Doe"
    assert response.data["details"]["email"] == "john@example.com"
    assert response.data["details"]["amount"] == "100.50"

@pytest.mark.django_db
def test_payment_retrieve(requests_mock, payment_instance):
    paystack_response = {
        "status": True,
        "message": "Verification successful",
        "data": {
            "status": "success",
            "paid_at": "2023-10-01T12:00:00Z",
        },
    }

    requests_mock.get(
        f"https://api.paystack.co/transaction/verify/{payment_instance.ref}",
        json=paystack_response,
        status_code=200,
    )

    client = APIClient()
    url = reverse("api:payment-detail", kwargs={"pk": payment_instance.id, "version": "v1"})

    # Make the GET request
    response = client.get(url, HTTP_ACCEPT="application/json; version=v1")

    # Assert the response
    assert response.status_code == 200
    assert "details" in response.data
    assert response.data["details"]["status"] == "success"
    assert response.data["details"]["paid_at"] == "2023-10-01T12:00:00Z"