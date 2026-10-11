"""
data_loader.py
Загрузка данных для API (с кэшированием).
"""

import pandas as pd
import os
from functools import lru_cache

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'DataCoSupplyChainDataset.csv')


@lru_cache(maxsize=1)
def load_data():
    """
    Загружает данные один раз и кэширует.
    
    Returns:
        DataFrame с данными
    """
    df = pd.read_csv(RAW_DATA, encoding='latin-1')
    
    # Создаём вычисляемые колонки
    df['delay'] = df['Days for shipping (real)'] - df['Days for shipment (scheduled)']
    
    return df


def get_stats():
    """Общая статистика."""
    df = load_data()
    
    total_orders = df['Order Id'].nunique()
    total_rows = len(df)
    late_orders = df[df['Late_delivery_risk'] == 1]['Order Id'].nunique()
    late_rate = late_orders / total_orders * 100
    
    return {
        'total_orders': int(total_orders),
        'total_rows': int(total_rows),
        'late_orders': int(late_orders),
        'late_rate': round(late_rate, 2),
        'avg_profit': round(df['Order Profit Per Order'].mean(), 2),
        'avg_sales': round(df['Sales'].mean(), 2),
    }


def get_shipping_modes():
    """Статистика по способам доставки."""
    df = load_data()
    
    # Уникальные заказы
    orders = df.groupby(['Shipping Mode', 'Order Id']).agg(
        is_late=('Late_delivery_risk', 'max'),
        profit=('Order Profit Per Order', 'mean')
    ).reset_index()
    
    stats = orders.groupby('Shipping Mode').agg(
        total_orders=('Order Id', 'nunique'),
        late_orders=('is_late', 'sum'),
        late_rate=('is_late', 'mean'),
        avg_profit=('profit', 'mean')
    )
    
    # Округляем ПОСЛЕ умножения
    stats['late_rate'] = (stats['late_rate'] * 100).round(2)
    stats['avg_profit'] = stats['avg_profit'].round(2)
    stats = stats.sort_values('late_rate', ascending=False)
    
    return stats.reset_index().to_dict(orient='records')


def get_regions():
    """Статистика по регионам."""
    df = load_data()
    
    orders = df.groupby(['Order Region', 'Order Id']).agg(
        is_late=('Late_delivery_risk', 'max')
    ).reset_index()
    
    stats = orders.groupby('Order Region').agg(
        total_orders=('Order Id', 'nunique'),
        late_orders=('is_late', 'sum'),
        late_rate=('is_late', 'mean')
    )
    
    # Округляем ПОСЛЕ умножения
    stats['late_rate'] = (stats['late_rate'] * 100).round(2)
    stats = stats.sort_values('late_rate', ascending=False).head(20)
    
    return stats.reset_index().to_dict(orient='records')


def get_categories():
    """Статистика по категориям."""
    df = load_data()
    
    orders = df.groupby(['Category Name', 'Order Id']).agg(
        is_late=('Late_delivery_risk', 'max')
    ).reset_index()
    
    stats = orders.groupby('Category Name').agg(
        total_orders=('Order Id', 'nunique'),
        late_orders=('is_late', 'sum'),
        late_rate=('is_late', 'mean')
    )
    
    # Фильтр: минимум 100 заказов
    stats = stats[stats['total_orders'] >= 100]
    
    # Округляем ПОСЛЕ умножения
    stats['late_rate'] = (stats['late_rate'] * 100).round(2)
    stats = stats.sort_values('late_rate', ascending=False).head(20)
    
    return stats.reset_index().to_dict(orient='records')


def get_order(order_id):
    """Информация о конкретном заказе."""
    df = load_data()
    
    order = df[df['Order Id'] == order_id]
    
    if order.empty:
        return None
    
    first = order.iloc[0]
    
    return {
        'order_id': int(order_id),
        'customer_id': int(first['Customer Id']),
        'order_date': str(first['order date (DateOrders)']),
        'shipping_date': str(first['shipping date (DateOrders)']),
        'shipping_mode': first['Shipping Mode'],
        'delivery_status': first['Delivery Status'],
        'late_delivery_risk': int(first['Late_delivery_risk']),
        'days_scheduled': int(first['Days for shipment (scheduled)']),
        'days_real': int(first['Days for shipping (real)']),
        'delay': int(first['delay']),
        'order_region': first['Order Region'],
        'order_country': first['Order Country'],
        'category': first['Category Name'],
        'sales': round(float(first['Sales']), 2),
        'profit': round(float(first['Order Profit Per Order']), 2),
        'quantity': int(first['Order Item Quantity']),
    }


def get_late_risk(order_id):
    """Риск опоздания для заказа."""
    df = load_data()
    
    order = df[df['Order Id'] == order_id]
    
    if order.empty:
        return None
    
    first = order.iloc[0]
    
    # Простая модель: риск зависит от способа доставки
    risk_by_mode = {
        'First Class': 95.32,
        'Second Class': 76.63,
        'Same Day': 45.74,
        'Standard Class': 38.07,
    }
    
    risk = risk_by_mode.get(first['Shipping Mode'], 50.0)
    
    return {
        'order_id': int(order_id),
        'shipping_mode': first['Shipping Mode'],
        'late_risk_percent': risk,
        'actual_late': int(first['Late_delivery_risk']),
        'days_scheduled': int(first['Days for shipment (scheduled)']),
        'days_real': int(first['Days for shipping (real)']),
    }


def get_recommendations():
    """Рекомендации по улучшению."""
    return {
        'problem': 'Высокая доля опозданий (54.82%)',
        'root_cause': 'Нереалистичные сроки доставки для First Class и Second Class',
        'details': [
            'First Class: запланировано 1 день, реально 2 дня → 95.32% опозданий',
            'Second Class: запланировано 2 дня, реально 4 дня → 76.63% опозданий',
            'Standard Class: запланировано 4 дня, реально 4 дня → 38.07% опозданий',
        ],
        'solution': [
            'First Class: установить 2 дня вместо 1',
            'Second Class: установить 4 дня вместо 2',
            'Standard Class: оставить 4 дня',
        ],
        'expected_effect': {
            'late_rate_before': 54.82,
            'late_rate_after': 20.0,
            'improvement': 34.82,
        },
    }
