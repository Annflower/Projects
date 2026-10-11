"""
load_description.py
Загрузка описания колонок DataCo Supply Chain.
"""

import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESC_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'DescriptionDataCoSupplyChain.csv')


def load_description():
    """Загружает описание колонок."""
    df = pd.read_csv(DESC_DATA, encoding='latin-1')
    print(f"Загружено описание: {df.shape[0]} колонок")
    return df


def show_description(df):
    """Показывает описание колонок."""
    print("=" * 60)
    print("ОПИСАНИЕ КОЛОНОК")
    print("=" * 60)
    for _, row in df.iterrows():
        print(f"\n{row.iloc[0]}")
        print(f"  {row.iloc[1]}")


if __name__ == "__main__":
    df = load_description()
    show_description(df)