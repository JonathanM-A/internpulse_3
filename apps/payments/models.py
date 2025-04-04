from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from apps.common.models import BaseModel


class Payment(BaseModel):

    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    amount = models.DecimalField(
        decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal("0.01"))]
    )
    ref = models.CharField(max_length=250, null=True, unique=True, editable=False)
    status = models.CharField(max_length=10, default="pending")
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
