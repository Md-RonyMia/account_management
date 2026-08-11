import pandas as pd
from datetime import timedelta
from analytics.models import DemandForecast, AIRecommendation
from inventory.models import Product


class ForecastService:
    @staticmethod
    def compute_moving_average(product: Product, horizon_days: int = 14):
        records = product.sales_records.order_by('date').values('date', 'quantity_sold')
        if not records.exists():
            return None

        df = pd.DataFrame(records)
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date').resample('D').sum().fillna(0)
        df['ma7'] = df['quantity_sold'].rolling(window=7, min_periods=1).mean()
        forecast_qty = float(df['ma7'].iloc[-1] * horizon_days)
        confidence = ForecastService.estimate_confidence(df)

        DemandForecast.objects.create(
            product=product,
            horizon_days=horizon_days,
            forecast_quantity=forecast_qty,
            method='moving_average',
            confidence=confidence,
            note='7-day moving average forecast',
        )
        return forecast_qty, confidence

    @staticmethod
    def estimate_confidence(df):
        if len(df) < 14:
            return 45.0
        seasonal_strength = df['quantity_sold'].std() / (df['quantity_sold'].mean() + 1)
        confidence = max(30.0, min(95.0, 100.0 - seasonal_strength * 20.0))
        return round(confidence, 2)


class RecommendationService:
    @staticmethod
    def generate_purchase_recommendation(product: Product, horizon_days: int = 14):
        forecast = ForecastService.compute_moving_average(product, horizon_days=horizon_days)
        if forecast is None:
            return None

        forecast_quantity, confidence = forecast
        current_stock = product.snapshots.first().quantity if product.snapshots.exists() else 0
        incoming_stock = 0
        recommended_qty = max(0, int(round(forecast_quantity + product.safety_stock - current_stock - incoming_stock)))
        priority = RecommendationService.compute_priority(product, recommended_qty)
        explanation = (
            f'Current stock: {current_stock}\n'
            f'Forecast demand for next {horizon_days} days: {forecast_quantity:.1f}\n'
            f'Safety stock: {product.safety_stock}\n'
            f'Incoming stock: {incoming_stock}\n'
            f'Recommended purchase quantity: {recommended_qty}\n'
        )

        recommendation = AIRecommendation.objects.create(
            product=product,
            recommended_quantity=recommended_qty,
            priority=priority,
            confidence=confidence,
            reason='Forecasted demand and safety stock gap.',
            explanation=explanation,
            input_data_period_start=product.sales_records.order_by('date').first().date,
            input_data_period_end=product.sales_records.order_by('-date').first().date,
            model_name='moving_average',
        )
        return recommendation

    @staticmethod
    def compute_priority(product: Product, recommended_qty: int):
        if recommended_qty <= 0:
            return 'Normal'
        if recommended_qty > product.reorder_threshold:
            return 'High'
        return 'Medium'
