"""
eda_profit_deep.py
Анализ прибыли по способам доставки с учетом опозданий.
"""

import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'DataCoSupplyChainDataset.csv')


def load_data():
    df = pd.read_csv(RAW_DATA, encoding='latin-1')
    return df


def analyze_profit_by_mode(df):
    """Прибыль по способу доставки с учетом опозданий."""
    print("=" * 60)
    print("ПРИБЫЛЬ ПО СПОСОБУ ДОСТАВКИ")
    print("=" * 60)

    # Группируем по способу доставки и статусу опоздания
    profit_stats = df.groupby(['Shipping Mode', 'Late_delivery_risk']).agg(
        count=('Order Profit Per Order', 'count'),
        avg_profit=('Order Profit Per Order', 'mean'),
        avg_sales=('Sales', 'mean'),
        total_profit=('Order Profit Per Order', 'sum')
    ).round(2)

    print(profit_stats)

    # Сравнение: опоздание vs без опоздания по каждому способу
    print("\n--- Разница в прибыли (опоздание vs без) ---")
    for mode in df['Shipping Mode'].unique():
        subset = df[df['Shipping Mode'] == mode]
        profit_late = subset[subset['Late_delivery_risk'] == 1]['Order Profit Per Order'].mean()
        profit_on_time = subset[subset['Late_delivery_risk'] == 0]['Order Profit Per Order'].mean()
        
        if profit_on_time > 0:
            diff = ((profit_late - profit_on_time) / profit_on_time) * 100
            print(f"{mode}: {diff:.2f}%")


def analyze_cancellations(df):
    """Анализ отменённых заказов."""
    print("\n" + "=" * 60)
    print("ОТМЕНЁННЫЕ ЗАКАЗЫ")
    print("=" * 60)

    canceled = df[df['Delivery Status'] == 'Shipping canceled']
    print(f"Всего отменённых: {len(canceled)}")
    print(f"Доля от всех заказов: {len(canceled) / len(df) * 100:.2f}%")

    print("\n--- По способу доставки ---")
    print(canceled['Shipping Mode'].value_counts())

    print("\n--- Прибыль от отменённых ---")
    print(f"Средняя прибыль: {canceled['Order Profit Per Order'].mean():.2f}")
    print(f"Суммарная прибыль: {canceled['Order Profit Per Order'].sum():.2f}")


def analyze_customer_segments(df):
    """Анализ по сегментам клиентов."""
    print("\n" + "=" * 60)
    print("СЕГМЕНТЫ КЛИЕНТОВ И ОПОЗДАНИЯ")
    print("=" * 60)

    segment_stats = df.groupby('Customer Segment').agg(
        total=('Late_delivery_risk', 'count'),
        late=('Late_delivery_risk', 'sum'),
        late_rate=('Late_delivery_risk', 'mean'),
        avg_profit=('Order Profit Per Order', 'mean')
    )
    segment_stats['late_rate'] = (segment_stats['late_rate'] * 100).round(2)
    print(segment_stats)


if __name__ == "__main__":
    df = load_data()
    print(f"Загружено: {df.shape[0]} строк")

    analyze_profit_by_mode(df)
    analyze_cancellations(df)
    analyze_customer_segments(df)

    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН")
    print("=" * 60)