import pytest
from apps.payments.models import Payment

@pytest.mark.django_db
def test_payment_creation():
    payment = Payment(name="andoh", email="test@mail.com", amount=100.00)
    payment.save()
    assert payment.id is not None

# @pytest.mark.django_db
# class TestServiceModel:
#     def test_service_creation(self):
#         service = Service.objects.create(name="Test Service", is_diagnostics=False)
#         assert service.name == "Test Service"
#         assert service.slug == "test-service"
#         assert not service.is_diagnostics

#     def test_service_str_method(self):
#         service = Service.objects.create(name="Test Service")
#         assert str(service) == "Test Service"

#     def test_service_with_parent(self):
#         parent_service = Service.objects.create(
#             name="Parent Service", is_diagnostics=True
#         )
#         child_service = Service.objects.create(
#             name="Child Service", parent_service=parent_service
#         )
#         assert child_service.parent_service == parent_service

#     def test_service_slug_generation(self):
#         service = Service.objects.create(name="Test Service 123")
#         assert service.slug == "test-service-123"

#     def test_unique_slug_generation(self):
#         Service.objects.create(name="Test Service")
#         service2 = Service.objects.create(name="Test Service")
#         assert service2.slug == "test-service-1"

#     def test_invalid_parent_service(self):
#         service = Service.objects.create(name="Test Service")
#         with pytest.raises(ValidationError):
#             service.parent_service = service
#             service.full_clean()

#     def test_cyclical_parent_relationship(self):
#         service1 = Service.objects.create(name="Service 1")
#         service2 = Service.objects.create(name="Service 2", parent_service=service1)
#         with pytest.raises(ValidationError):
#             service1.parent_service = service2
#             service1.full_clean()

#     def test_bulk_create_with_unique_slugs(self):
#         services = [
#             Service(name="Test Service"),
#             Service(name="Test Service"),
#             Service(name="Another Service"),
#         ]

#         existing_slugs = set()
#         for service in services:
#             service.slug = Service.generate_unique_slug(service.name, existing_slugs)
#             existing_slugs.add(service.slug)

#         Service.objects.bulk_create(services)
#         created_services = Service.objects.all()

#         assert created_services.count() == 3

#         created_slugs = set(service.slug for service in created_services)
#         expected_slugs = {"test-service", "test-service-1", "another-service"}
#         assert created_slugs == expected_slugs

#         for service in created_services:
#             if service.name == "Test Service":
#                 assert service.slug in {"test-service", "test-service-1"}
#             elif service.name == "Another Service":
#                 assert service.slug == "another-service"