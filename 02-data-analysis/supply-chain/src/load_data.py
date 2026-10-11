"""
load_data.py
Загрузка данных DataCo Supply Chain.
"""

import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'DataCoSupplyChainDataset.csv')


def load_raw_data():
    """Загружает сырые данные."""
    df = pd.read_csv(RAW_DATA, encoding='latin-1')
    print(f"Загружено: {df.shape[0]} строк, {df.shape[1]} колонок")
    return df


def show_basic_info(df):
    """Показывает базовую информацию о данных."""
    print("=" * 60)
    print("ИНФОРМАЦИЯ О ДАТАСЕТЕ")
    print("=" * 60)
    print(f"\nРазмер: {df.shape}")
    print("\nКолонки:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    print("\nТипы данных:")
    print(df.dtypes.value_counts())
    print("\nПропуски (топ-10):")
    missing = df.isnull().sum().sort_values(ascending=False).head(10)
    print(missing[missing > 0])
    print("\nПервые 3 строки:")
    print(df.head(3))


if __name__ == "__main__":
    df = load_raw_data()
    show_basic_info(df)