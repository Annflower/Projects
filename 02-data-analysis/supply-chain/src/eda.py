"""
eda.py
Первичный анализ данных DataCo Supply Chain.
"""

import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'DataCoSupplyChainDataset.csv')


def load_data():
    """Загружает данные."""
    df = pd.read_csv(RAW_DATA, encoding='latin-1')
    return df


def analyze_late_delivery(df):
    """Анализ опозданий."""
    print("=" * 60)
    print("АНАЛИЗ ОПОЗДАНИЙ")
    print("=" * 60)

    # Общая доля опозданий
    late_share = df['Late_delivery_risk'].mean() * 100
    print(f"\nОбщая доля опозданий: {late_share:.2f}%")

    # По способу доставки
    print("\n--- По способу доставки ---")
    shipping_stats = df.groupby('Shipping Mode').agg(
        total=('Late_delivery_risk', 'count'),
        late=('Late_delivery_risk', 'sum'),
        late_rate=('Late_delivery_risk', 'mean')
    )
    shipping_stats['late_rate'] = (shipping_stats['late_rate'] * 100).round(2)
    shipping_stats = shipping_stats.sort_values('late_rate', ascending=False)
    print(shipping_stats)

    # По региону
    print("\n--- По региону (топ-10) ---")
    region_stats = df.groupby('Order Region').agg(
        total=('Late_delivery_risk', 'count'),
        late=('Late_delivery_risk', 'sum'),
        late_rate=('Late_delivery_risk', 'mean')
    )
    region_stats['late_rate'] = (region_stats['late_rate'] * 100).round(2)
    region_stats = region_stats.sort_values('late_rate', ascending=False).head(10)
    print(region_stats)

    # По категории
    print("\n--- По категории (топ-10) ---")
    category_stats = df.groupby('Category Name').agg(
        total=('Late_delivery_risk', 'count'),
        late=('Late_delivery_risk', 'sum'),
        late_rate=('Late_delivery_risk', 'mean')
    )
    category_stats['late_rate'] = (category_stats['late_rate'] * 100).round(2)
    category_stats = category_stats.sort_values('late_rate', ascending=False).head(10)
    print(category_stats)


def analyze_profit(df):
    """Анализ влияния опозданий на прибыль."""
    print("\n" + "=" * 60)
    print("ВЛИЯНИЕ ОПОЗДАНИЙ НА ПРИБЫЛЬ")
    print("=" * 60)

    # Средняя прибыль при опоздании и без
    profit_stats = df.groupby('Late_delivery_risk').agg(
        avg_profit=('Order Profit Per Order', 'mean'),
        avg_sales=('Sales', 'mean'),
        count=('Order Profit Per Order', 'count')
    )
    print("\n--- Средняя прибыль ---")
    print(profit_stats)

    # Разница
    profit_late = profit_stats.loc[1, 'avg_profit']
    profit_on_time = profit_stats.loc[0, 'avg_profit']
    diff = ((profit_late - profit_on_time) / profit_on_time) * 100
    print(f"\nРазница в прибыли: {diff:.2f}%")

    # По сегментам клиентов
    print("\n--- По сегментам клиентов ---")
    segment_stats = df.groupby('Customer Segment').agg(
        total=('Late_delivery_risk', 'count'),
        late_rate=('Late_delivery_risk', 'mean'),
        avg_profit=('Order Profit Per Order', 'mean')
    )
    segment_stats['late_rate'] = (segment_stats['late_rate'] * 100).round(2)
    print(segment_stats)


def analyze_cross(df):
    """Кросс-анализ: способ доставки + регион."""
    print("\n" + "=" * 60)
    print("КРОСС-АНАЛИЗ: СПОСОБ ДОСТАВКИ + РЕГИОН")
    print("=" * 60)

    # Топ-5 комбинаций с максимальным процентом опозданий
    cross = df.groupby(['Shipping Mode', 'Order Region']).agg(
        total=('Late_delivery_risk', 'count'),
        late_rate=('Late_delivery_risk', 'mean')
    )
    cross['late_rate'] = (cross['late_rate'] * 100).round(2)
    cross = cross[cross['total'] > 100]  # фильтр по количеству
    cross = cross.sort_values('late_rate', ascending=False).head(10)
    print(cross)


if __name__ == "__main__":
    df = load_data()
    print(f"Загружено: {df.shape[0]} строк, {df.shape[1]} колонок")

    analyze_late_delivery(df)
    analyze_profit(df)
    analyze_cross(df)

    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН")
    print("=" * 60)