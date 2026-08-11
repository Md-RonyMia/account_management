from django.contrib import admin
from .models import Supplier, PurchaseRequest, PurchaseRequestItem


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'contact_phone', 'average_lead_time_days')


class PurchaseRequestItemInline(admin.TabularInline):
    model = PurchaseRequestItem
    extra = 1


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'created_at', 'status')
    inlines = [PurchaseRequestItemInline]
