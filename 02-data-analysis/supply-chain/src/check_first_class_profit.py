"""
check_first_class_profit.py
Почему прибыль First Class с опозданием выше?
"""

import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'DataCoSupplyChainDataset.csv')


def load_data():
    df = pd.read_csv(RAW_DATA, encoding='latin-1')
    return df


def check_first_class_profit(df):
    """Сравнение структуры заказов First Class."""
    print("=" * 60)
    print("ПОЧЕМУ ПРИБЫЛЬ FIRST CLASS С ОПОЗДАНИЕМ ВЫШЕ?")
    print("=" * 60)

    # Фильтруем First Class
    fc = df[df['Shipping Mode'] == 'First Class'].copy()

    # Разбиваем на группы
    fc_late = fc[fc['Late_delivery_risk'] == 1]
    fc_on_time = fc[fc['Late_delivery_risk'] == 0]

    print(f"\nFirst Class с опозданием: {len(fc_late)} заказов")
    print(f"First Class без опоздания: {len(fc_on_time)} заказов")

    # Сравниваем средние значения
    print("\n--- Сравнение средних ---")
    compare = pd.DataFrame({
        'с опозданием': fc_late[['Order Profit Per Order', 'Sales', 'Order Item Quantity',
                                  'Order Item Discount Rate', 'Product Price']].mean(),
        'без опоздания': fc_on_time[['Order Profit Per Order', 'Sales', 'Order Item Quantity',
                                      'Order Item Discount Rate', 'Product Price']].mean()
    })
    compare['разница %'] = ((compare['с опозданием'] - compare['без опоздания']) / 
                            compare['без опоздания'] * 100).round(2)
    print(compare.round(2))

    # Сравниваем категории товаров
    print("\n--- Топ-5 категорий с опозданием ---")
    print(fc_late['Category Name'].value_counts().head(5))

    print("\n--- Топ-5 категорий без опоздания ---")
    print(fc_on_time['Category Name'].value_counts().head(5))

    # Сравниваем регионы
    print("\n--- Топ-5 регионов с опозданием ---")
    print(fc_late['Order Region'].value_counts().head(5))

    print("\n--- Топ-5 регионов без опоздания ---")
    print(fc_on_time['Order Region'].value_counts().head(5))

    # Сравниваем сегменты клиентов
    print("\n--- Сегменты клиентов с опозданием ---")
    print(fc_late['Customer Segment'].value_counts())

    print("\n--- Сегменты клиентов без опоздания ---")
    print(fc_on_time['Customer Segment'].value_counts())

    # Сравниваем скидки
    print("\n--- Скидки ---")
    print(f"С опозданием: средняя скидка {fc_late['Order Item Discount Rate'].mean():.4f}")
    print(f"Без опоздания: средняя скидка {fc_on_time['Order Item Discount Rate'].mean():.4f}")


def check_t_test(df):
    """Статистическая проверка: значима ли разница?"""
    from scipy import stats

    print("\n" + "=" * 60)
    print("СТАТИСТИЧЕСКАЯ ПРОВЕРКА (t-test)")
    print("=" * 60)

    fc = df[df['Shipping Mode'] == 'First Class']
    fc_late = fc[fc['Late_delivery_risk'] == 1]['Order Profit Per Order']
    fc_on_time = fc[fc['Late_delivery_risk'] == 0]['Order Profit Per Order']

    t_stat, p_value = stats.ttest_ind(fc_late, fc_on_time)

    print(f"\nt-статистика: {t_stat:.4f}")
    print(f"p-value: {p_value:.6f}")

    if p_value < 0.05:
        print("→ Разница статистически значима (p < 0.05)")
    else:
        print("→ Разница НЕ значима (p >= 0.05)")


if __name__ == "__main__":
    df = load_data()
    check_first_class_profit(df)
    check_t_test(df)

    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН")
    print("=" * 60)