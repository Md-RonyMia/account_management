from django.db import models
from django.conf import settings
from inventory.models import Product


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    average_lead_time_days = models.PositiveIntegerField(default=7)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class PurchaseRequest(models.Model):
    STATUS_NEW = 'new'
    STATUS_SUBMITTED = 'submitted'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_CANCELED, 'Canceled'),
    ]

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='purchase_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'PR-{self.id} ({self.status})'


class PurchaseRequestItem(models.Model):
    purchase_request = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity_requested = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField(blank=True)

    def __str__(self):
        return f'{self.product.name}: {self.quantity_requested}'
