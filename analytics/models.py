from django.db import models
from inventory.models import Product


class SalesRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales_records')
    date = models.DateField()
    quantity_sold = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.product.name} sold {self.quantity_sold} on {self.date}'


class DemandForecast(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='forecasts')
    generated_at = models.DateTimeField(auto_now_add=True)
    horizon_days = models.PositiveIntegerField()
    forecast_quantity = models.FloatField()
    method = models.CharField(max_length=120)
    confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f'{self.product.name} forecast {self.horizon_days}d = {self.forecast_quantity}'


class AIRecommendation(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_REVIEWED = 'reviewed'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_DISMISSED = 'dismissed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_REVIEWED, 'Reviewed'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_DISMISSED, 'Dismissed'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ai_recommendations')
    created_at = models.DateTimeField(auto_now_add=True)
    recommendation_type = models.CharField(max_length=120, default='purchase')
    recommended_quantity = models.PositiveIntegerField()
    recommended_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=50, blank=True)
    confidence = models.DecimalField(max_digits=5, decimal_places=2)
    reason = models.TextField(blank=True)
    explanation = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    input_data_period_start = models.DateField(null=True, blank=True)
    input_data_period_end = models.DateField(null=True, blank=True)
    model_name = models.CharField(max_length=120, default='moving_average')

    def __str__(self):
        return f'AI Recommendation for {self.product.name} ({self.status})'
