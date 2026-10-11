"""
check_first_class.py
Проверка: почему First Class опаздывает в 95% случаев.
"""

import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'DataCoSupplyChainDataset.csv')


def load_data():
    df = pd.read_csv(RAW_DATA, encoding='latin-1')
    return df


def check_first_class(df):
    """Детальная проверка First Class."""
    print("=" * 60)
    print("ПРОВЕРКА FIRST CLASS")
    print("=" * 60)

    # Фильтруем только First Class
    fc = df[df['Shipping Mode'] == 'First Class'].copy()

    print(f"\nВсего заказов First Class: {len(fc)}")

    # Смотрим на сроки
    print("\n--- Запланированный срок (Days for shipment (scheduled)) ---")
    print(fc['Days for shipment (scheduled)'].value_counts().sort_index())

    print("\n--- Реальный срок (Days for shipping (real)) ---")
    print(fc['Days for shipping (real)'].value_counts().sort_index())

    # Считаем задержку
    fc['delay'] = fc['Days for shipping (real)'] - fc['Days for shipment (scheduled)']

    print("\n--- Задержка (real - scheduled) ---")
    print(fc['delay'].value_counts().sort_index())

    # Проверяем Late_delivery_risk
    print("\n--- Late_delivery_risk ---")
    print(fc['Late_delivery_risk'].value_counts())

    # Смотрим на примеры
    print("\n--- Примеры заказов First Class ---")
    print(fc[['Days for shipment (scheduled)', 'Days for shipping (real)', 
              'delay', 'Late_delivery_risk', 'Delivery Status']].head(20))

    # Проверяем Delivery Status
    print("\n--- Delivery Status для First Class ---")
    print(fc['Delivery Status'].value_counts())


def check_all_modes(df):
    """Проверка всех способов доставки."""
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ ВСЕХ СПОСОБОВ ДОСТАВКИ")
    print("=" * 60)

    for mode in df['Shipping Mode'].unique():
        subset = df[df['Shipping Mode'] == mode]
        print(f"\n--- {mode} ---")
        print(f"Запланировано (среднее): {subset['Days for shipment (scheduled)'].mean():.2f}")
        print(f"Реально (среднее): {subset['Days for shipping (real)'].mean():.2f}")
        print(f"Late_delivery_risk = 1: {subset['Late_delivery_risk'].sum()} "
              f"({subset['Late_delivery_risk'].mean()*100:.2f}%)")
        print(f"Delivery Status:")
        print(subset['Delivery Status'].value_counts())


if __name__ == "__main__":
    df = load_data()
    check_first_class(df)
    check_all_modes(df)