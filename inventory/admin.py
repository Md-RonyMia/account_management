from django.contrib import admin
from .models import Category, Product, InventorySnapshot, StockTransaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'reorder_threshold', 'safety_stock', 'max_stock')
    list_filter = ('category',)


@admin.register(InventorySnapshot)
class InventorySnapshotAdmin(admin.ModelAdmin):
    list_display = ('product', 'recorded_at', 'quantity')
    list_filter = ('product',)


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'created_at', 'quantity_change', 'source')
    list_filter = ('product',)
