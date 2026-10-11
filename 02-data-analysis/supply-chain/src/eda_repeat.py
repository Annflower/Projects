"""
eda_repeat.py
Анализ повторных заказов и влияния опозданий на лояльность.
"""

import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'DataCoSupplyChainDataset.csv')


def load_data():
    """Загружает данные."""
    df = pd.read_csv(RAW_DATA, encoding='latin-1')
    return df


def analyze_repeat_orders(df):
    """Общая статистика по повторным заказам."""
    print("=" * 60)
    print("ПОВТОРНЫЕ ЗАКАЗЫ: ОБЩАЯ СТАТИСТИКА")
    print("=" * 60)

    unique_customers = df['Customer Id'].nunique()
    total_orders = df['Order Id'].nunique()

    print(f"\nУникальных клиентов: {unique_customers}")
    print(f"Всего заказов: {total_orders}")
    print(f"Среднее заказов на клиента: {total_orders / unique_customers:.2f}")

    # Клиенты с опозданиями
    late_customers = df[df['Late_delivery_risk'] == 1]['Customer Id'].nunique()
    on_time_customers = df[df['Late_delivery_risk'] == 0]['Customer Id'].nunique()

    print(f"\nКлиентов с хотя бы одним опозданием: {late_customers}")
    print(f"  Доля: {late_customers / unique_customers * 100:.2f}%")
    print(f"Клиентов без опозданий: {on_time_customers}")
    print(f"  Доля: {on_time_customers / unique_customers * 100:.2f}%")


def analyze_orders_per_customer(df):
    """Распределение количества заказов на клиента."""
    print("\n" + "=" * 60)
    print("РАСПРЕДЕЛЕНИЕ ЗАКАЗОВ НА КЛИЕНТА")
    print("=" * 60)

    orders_per_customer = df.groupby('Customer Id')['Order Id'].nunique()

    print(f"\nСреднее: {orders_per_customer.mean():.2f}")
    print(f"Медиана: {orders_per_customer.median():.2f}")
    print(f"Максимум: {orders_per_customer.max()}")
    print(f"Минимум: {orders_per_customer.min()}")

    print("\n--- Распределение (топ-10) ---")
    print(orders_per_customer.value_counts().sort_index().head(10))


def analyze_late_impact_on_repeat(df):
    """Влияние опозданий на повторные заказы."""
    print("\n" + "=" * 60)
    print("ВЛИЯНИЕ ОПОЗДАНИЙ НА ПОВТОРНЫЕ ЗАКАЗЫ")
    print("=" * 60)

    # Для каждого клиента: сколько заказов и сколько опозданий
    customer_stats = df.groupby('Customer Id').agg(
        total_orders=('Order Id', 'nunique'),
        late_orders=('Late_delivery_risk', 'sum'),
        avg_profit=('Order Profit Per Order', 'mean')
    )

    # Разбиваем на группы по количеству опозданий
    customer_stats['late_group'] = pd.cut(
        customer_stats['late_orders'],
        bins=[-1, 0, 1, 2, 100],
        labels=['0 опозданий', '1 опоздание', '2 опоздания', '3+ опозданий']
    )

    print("\n--- Среднее количество заказов по группам ---")
    repeat_stats = customer_stats.groupby('late_group', observed=True).agg(
        customers=('total_orders', 'count'),
        avg_orders=('total_orders', 'mean'),
        avg_profit=('avg_profit', 'mean')
    ).round(2)
    print(repeat_stats)

    # Доля клиентов, которые сделали >1 заказа
    print("\n--- Доля клиентов с повторными заказами (>1 заказа) ---")
    for group in customer_stats['late_group'].cat.categories:
        subset = customer_stats[customer_stats['late_group'] == group]
        if len(subset) > 0:
            repeat_share = (subset['total_orders'] > 1).mean() * 100
            print(f"{group}: {repeat_share:.2f}% (всего клиентов: {len(subset)})")


def analyze_late_by_segment(df):
    """Анализ опозданий по сегментам клиентов."""
    print("\n" + "=" * 60)
    print("ОПОЗДАНИЯ ПО СЕГМЕНТАМ КЛИЕНТОВ")
    print("=" * 60)

    segment_stats = df.groupby('Customer Segment').agg(
        total_orders=('Order Id', 'count'),
        late_orders=('Late_delivery_risk', 'sum'),
        late_rate=('Late_delivery_risk', 'mean'),
        avg_profit=('Order Profit Per Order', 'mean')
    )
    segment_stats['late_rate'] = (segment_stats['late_rate'] * 100).round(2)
    segment_stats = segment_stats.round(2)
    print(segment_stats)


if __name__ == "__main__":
    df = load_data()
    print(f"Загружено: {df.shape[0]} строк")

    analyze_repeat_orders(df)
    analyze_orders_per_customer(df)
    analyze_late_impact_on_repeat(df)
    analyze_late_by_segment(df)

    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН")
    print("=" * 60)