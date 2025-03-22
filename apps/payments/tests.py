import pytest
from apps.payments.models import Payment

@pytest.mark.django_db
def test_payment_creation():
    payment = Payment(name="andoh", email="test@mail.com", amount=100.00)
    payment.save()
    assert payment.id is not None