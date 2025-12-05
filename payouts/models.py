import uuid
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator
from django.db import models


class Currency(models.TextChoices):
    RUB = 'RUB', 'Ruble'
    USD = 'USD', 'Dollar'
    EUR = 'EUR', 'Euro'


class PayoutStatus(models.TextChoices):
    NEW = 'new', 'New'
    PROCESSING = 'processing', 'Processing'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'


class User(AbstractUser):
    def __str__(self):
        return self.username


class Payout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    currency = models.CharField(max_length=3, choices=Currency.choices)
    beneficiary_name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(3)],
    )
    beneficiary_account = models.CharField(
        max_length=34,
        validators=[
            MinLengthValidator(16),
            RegexValidator(regex=r'^[0-9A-Z]+$', message='Неверно указан счёт получателя!'),
        ],
    )
    description = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=16, choices=PayoutStatus.choices, default=PayoutStatus.NEW)

    class Meta:
        ordering = ['-created_at']
        default_related_name = 'created_payouts'
        verbose_name = 'выплата'
        verbose_name_plural = 'Выплаты'

    def __str__(self):
        return f'Payout {self.id} {self.amount} {self.currency} ({self.status})'
