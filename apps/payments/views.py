from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Payment
from .serializers import PaymentSerializer
from .paystack import Paystack
import secrets


class PaymentViewset(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Payment.objects.all()
    http_method_names = [
        m for m in ModelViewSet.http_method_names if m not in ["delete", "put", "patch"]
    ]
    serializer_class = PaymentSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        if request.version == "v1":

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            ref = secrets.token_urlsafe(50)
            name = serializer.validated_data.get("name")
            email = serializer.validated_data.get("email")
            amount = serializer.validated_data.get("amount")

            amount_in_sub_unit = int(float(amount) * 100)

            paystack = Paystack()
            response_data = paystack.initialize_payment(ref, email, amount_in_sub_unit)

            status = response_data["status"]
            message = response_data["message"]
            data = response_data["data"]

            if not status:
                return Response(
                    {
                        "error": _(
                            f"Failed to initialize payment with Paystack, {message}"
                        ),
                        "details": _(data),
                    },
                    status=500,
                )

            payment_url = data["authorization_url"]

            payment_instance = serializer.save()
            payment_instance.ref = ref
            payment_instance.save()
            payment_instance.refresh_from_db()

            return Response(
                {
                    "payment_url": payment_url,
                    "message": "Payment created successfully",
                    "details": PaymentSerializer(payment_instance).data,
                },
                status=201,
            )

        else:
            return Response({"error": _("Unknown version")})

    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):
        if request.version == "v1":
            instance = self.get_object()

            if instance.status == "pending":
                is_verified, message, status, paid_at = Paystack.verify_payment(
                    instance.ref
                )

                if is_verified:
                    instance.status = status
                    instance.paid_at = paid_at
                    instance.save()
                    instance.refresh_from_db()
                else:
                    raise Exception(message)

            serializer = self.get_serializer(instance)
            return Response(
                {
                    "details": serializer.data,
                    "message": "Payment details retrieved successfully",
                },
                status=200,
            )
        else:
            return Response({"error": _("Unknown version")})
