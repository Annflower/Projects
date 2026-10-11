"""
models.py
Pydantic-модели для API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class HealthResponse(BaseModel):
    """Ответ для проверки работоспособности."""
    status: str = Field(..., description="Статус: ok")
    version: str = Field(..., description="Версия API")


class StatsResponse(BaseModel):
    """Общая статистика."""
    total_orders: int = Field(..., description="Всего заказов")
    total_rows: int = Field(..., description="Всего строк")
    late_orders: int = Field(..., description="Заказов с опозданием")
    late_rate: float = Field(..., description="Доля опозданий (%)")
    avg_profit: float = Field(..., description="Средняя прибыль")
    avg_sales: float = Field(..., description="Средняя выручка")


class ShippingModeStats(BaseModel):
    """Статистика по способу доставки."""
    Shipping_Mode: str
    total_orders: int
    late_orders: int
    late_rate: float
    avg_profit: float


class RegionStats(BaseModel):
    """Статистика по региону."""
    Order_Region: str
    total_orders: int
    late_orders: int
    late_rate: float


class CategoryStats(BaseModel):
    """Статистика по категории."""
    Category_Name: str
    total_orders: int
    late_orders: int
    late_rate: float


class OrderResponse(BaseModel):
    """Информация о заказе."""
    order_id: int
    customer_id: int
    order_date: str
    shipping_date: str
    shipping_mode: str
    delivery_status: str
    late_delivery_risk: int
    days_scheduled: int
    days_real: int
    delay: int
    order_region: str
    order_country: str
    category: str
    sales: float
    profit: float
    quantity: int


class LateRiskResponse(BaseModel):
    """Риск опоздания."""
    order_id: int
    shipping_mode: str
    late_risk_percent: float
    actual_late: int
    days_scheduled: int
    days_real: int


class RecommendationResponse(BaseModel):
    """Рекомендации."""
    problem: str
    root_cause: str
    details: List[str]
    solution: List[str]
    expected_effect: dict


class ErrorResponse(BaseModel):
    """Ответ об ошибке."""
    detail: str = Field(..., description="Описание ошибки")