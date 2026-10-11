"""
eda_repeat_fixed.py
Исправленный анализ повторных заказов и опозданий.
"""

import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'DataCoSupplyChainDataset.csv')


def load_data():
    df = pd.read_csv(RAW_DATA, encoding='latin-1')
    return df


def analyze_repeat_fixed(df):
    """Исправленный анализ повторных заказов."""
    print("=" * 60)
    print("ИСПРАВЛЕННЫЙ АНАЛИЗ ПОВТОРНЫХ ЗАКАЗОВ")
    print("=" * 60)

    # Шаг 1: Создаём таблицу уникальных заказов
    orders = df.groupby(['Customer Id', 'Order Id']).agg(
        is_late=('Late_delivery_risk', 'max'),  # 1 если хотя бы один товар опоздал
        profit=('Order Profit Per Order', 'mean')
    ).reset_index()

    print(f"\nВсего уникальных заказов: {len(orders)}")
    print(f"Из них с опозданием: {orders['is_late'].sum()} ({orders['is_late'].mean()*100:.2f}%)")

    # Шаг 2: Считаем по клиентам
    customer_stats = orders.groupby('Customer Id').agg(
        total_orders=('Order Id', 'nunique'),
        late_orders=('is_late', 'sum'),
        avg_profit=('profit', 'mean')
    )

    # Шаг 3: Разбиваем на группы по количеству опозданий
    customer_stats['late_group'] = pd.cut(
        customer_stats['late_orders'],
        bins=[-1, 0, 1, 2, 100],
        labels=['0 опозданий', '1 опоздание', '2 опоздания', '3+ опозданий']
    )

    print("\n--- Среднее количество заказов по группам ---")
    repeat_stats = customer_stats.groupby('late_group', observed=True).agg(
        customers=('total_orders', 'count'),
        avg_orders=('total_orders', 'mean'),
        median_orders=('total_orders', 'median'),
        avg_profit=('avg_profit', 'mean')
    ).round(2)
    print(repeat_stats)

    # Шаг 4: Доля клиентов с повторными заказами
    print("\n--- Доля клиентов с повторными заказами (>1 заказа) ---")
    for group in customer_stats['late_group'].cat.categories:
        subset = customer_stats[customer_stats['late_group'] == group]
        if len(subset) > 0:
            repeat_share = (subset['total_orders'] > 1).mean() * 100
            print(f"{group}: {repeat_share:.2f}% (всего клиентов: {len(subset)})")

    # Шаг 5: Кросс-таблица
    print("\n--- Кросс-таблица: заказы vs опоздания ---")
    customer_stats['order_group'] = pd.cut(
        customer_stats['total_orders'],
        bins=[0, 1, 3, 5, 100],
        labels=['1 заказ', '2-3 заказа', '4-5 заказов', '6+ заказов']
    )
    
    cross = pd.crosstab(
        customer_stats['order_group'],
        customer_stats['late_group'],
        margins=True
    )
    print(cross)

    # Шаг 6: Средняя доля опозданий по группам заказов
    print("\n--- Средняя доля опозданий по группам заказов ---")
    for group in customer_stats['order_group'].cat.categories:
        subset = customer_stats[customer_stats['order_group'] == group]
        if len(subset) > 0:
            avg_late_rate = (subset['late_orders'] / subset['total_orders']).mean() * 100
            print(f"{group}: {avg_late_rate:.2f}% (клиентов: {len(subset)})")


def analyze_late_rate_by_orders_fixed(df):
    """Как доля опозданий зависит от количества заказов (исправлено)."""
    print("\n" + "=" * 60)
    print("ДОЛЯ ОПОЗДАНИЙ ПО КОЛИЧЕСТВУ ЗАКАЗОВ (ИСПРАВЛЕНО)")
    print("=" * 60)

    # Уникальные заказы
    orders = df.groupby(['Customer Id', 'Order Id']).agg(
        is_late=('Late_delivery_risk', 'max')
    ).reset_index()

    # По клиентам
    customer_stats = orders.groupby('Customer Id').agg(
        total_orders=('Order Id', 'nunique'),
        late_orders=('is_late', 'sum')
    )
    customer_stats['late_rate'] = customer_stats['late_orders'] / customer_stats['total_orders']

    # Группируем по количеству заказов
    for orders_count in range(1, 11):
        subset = customer_stats[customer_stats['total_orders'] == orders_count]
        if len(subset) > 0:
            print(f"{orders_count} заказов: {len(subset)} клиентов, "
                  f"средняя доля опозданий {subset['late_rate'].mean()*100:.2f}%")


if __name__ == "__main__":
    df = load_data()
    print(f"Загружено: {df.shape[0]} строк")

    analyze_repeat_fixed(df)
    analyze_late_rate_by_orders_fixed(df)

    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН")
    print("=" * 60)