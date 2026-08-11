from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    unit = models.CharField(max_length=50, default='unit')
    reorder_threshold = models.PositiveIntegerField(default=0)
    safety_stock = models.PositiveIntegerField(default=0)
    max_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.sku})'


class InventorySnapshot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='snapshots')
    recorded_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-recorded_at']


class StockTransaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    quantity_change = models.IntegerField()
    source = models.CharField(max_length=120)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
