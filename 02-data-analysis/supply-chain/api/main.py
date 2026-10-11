"""
main.py
REST API для анализа цепочки поставок DataCo.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from api.models import (
    HealthResponse,
    StatsResponse,
    ShippingModeStats,
    RegionStats,
    CategoryStats,
    OrderResponse,
    LateRiskResponse,
    RecommendationResponse,
    ErrorResponse,
)
from api import data_loader

app = FastAPI(
    title="DataCo Supply Chain API",
    description="API для анализа цепочки поставок DataCo Global",
    version="1.0.0",
)


@app.get("/", tags=["Root"])
def root():
    """Корневой эндпоинт."""
    return {
        "message": "DataCo Supply Chain API",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
def health():
    """Проверка работоспособности API."""
    return HealthResponse(status="ok", version="1.0.0")


@app.get("/api/stats", response_model=StatsResponse, tags=["Stats"])
def stats():
    """Общая статистика."""
    return data_loader.get_stats()


@app.get("/api/shipping-modes", tags=["Stats"])
def shipping_modes():
    """Статистика по способам доставки."""
    return data_loader.get_shipping_modes()


@app.get("/api/regions", tags=["Stats"])
def regions():
    """Статистика по регионам."""
    return data_loader.get_regions()


@app.get("/api/categories", tags=["Stats"])
def categories():
    """Статистика по категориям."""
    return data_loader.get_categories()


@app.get(
    "/api/orders/{order_id}",
    response_model=OrderResponse,
    responses={404: {"model": ErrorResponse}},
    tags=["Orders"],
)
def get_order(order_id: int):
    """
    Информация о конкретном заказе.
    
    - **order_id**: ID заказа (целое число)
    """
    if order_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="order_id должен быть положительным числом",
        )
    
    order = data_loader.get_order(order_id)
    
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заказ с ID {order_id} не найден",
        )
    
    return order


@app.get(
    "/api/late-risk/{order_id}",
    response_model=LateRiskResponse,
    responses={404: {"model": ErrorResponse}},
    tags=["Orders"],
)
def get_late_risk(order_id: int):
    """
    Риск опоздания для заказа.
    
    - **order_id**: ID заказа (целое число)
    """
    if order_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="order_id должен быть положительным числом",
        )
    
    risk = data_loader.get_late_risk(order_id)
    
    if risk is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заказ с ID {order_id} не найден",
        )
    
    return risk


@app.get(
    "/api/recommendations",
    response_model=RecommendationResponse,
    tags=["Analytics"],
)
def recommendations():
    """Рекомендации по улучшению."""
    return data_loader.get_recommendations()