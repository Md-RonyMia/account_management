from django.contrib import admin
from .models import SalesRecord, DemandForecast, AIRecommendation


@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'date', 'quantity_sold', 'unit_price')
    list_filter = ('product', 'date')


@admin.register(DemandForecast)
class DemandForecastAdmin(admin.ModelAdmin):
    list_display = ('product', 'horizon_days', 'forecast_quantity', 'generated_at', 'method')
    list_filter = ('product', 'horizon_days', 'method')


@admin.register(AIRecommendation)
class AIRecommendationAdmin(admin.ModelAdmin):
    list_display = ('product', 'created_at', 'status', 'recommended_quantity', 'priority', 'confidence')
    list_filter = ('status', 'recommendation_type', 'priority')
