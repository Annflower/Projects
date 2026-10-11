"""
clean_data.py
Очистка данных DataCo Supply Chain.

Что делает:
- Удаляет мусорные колонки (Product Description, Order Zipcode).
- Переименовывает колонки (на английский без пробелов).
- Сохраняет очищенные данные в data/processed/.
"""

import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'DataCoSupplyChainDataset.csv')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
PROCESSED_DATA = os.path.join(PROCESSED_DIR, 'supply_chain_clean.csv')


# Колонки, которые удаляем (мусор)
DROP_COLUMNS = [
    'Product Description',   # 100% пусто
    'Order Zipcode',         # 86% пусто
    'Product Image',         # ссылки, не нужны
    'Customer Password',     # замаскировано
    'Customer Email',        # PII
    'Customer Fname',        # PII
    'Customer Lname',        # PII
    'Customer Street',       # PII
]


# Переименование колонок (для удобства)
RENAME_COLUMNS = {
    'Type': 'type',
    'Days for shipping (real)': 'days_real',
    'Days for shipment (scheduled)': 'days_scheduled',
    'Benefit per order': 'benefit_per_order',
    'Sales per customer': 'sales_per_customer',
    'Delivery Status': 'delivery_status',
    'Late_delivery_risk': 'late_risk',
    'Category Id': 'category_id',
    'Category Name': 'category_name',
    'Customer City': 'customer_city',
    'Customer Country': 'customer_country',
    'Customer Id': 'customer_id',
    'Customer Segment': 'customer_segment',
    'Customer State': 'customer_state',
    'Customer Zipcode': 'customer_zipcode',
    'Department Id': 'department_id',
    'Department Name': 'department_name',
    'Latitude': 'latitude',
    'Longitude': 'longitude',
    'Market': 'market',
    'Order City': 'order_city',
    'Order Country': 'order_country',
    'Order Customer Id': 'order_customer_id',
    'order date (DateOrders)': 'order_date',
    'Order Id': 'order_id',
    'Order Item Cardprod Id': 'item_cardprod_id',
    'Order Item Discount': 'item_discount',
    'Order Item Discount Rate': 'item_discount_rate',
    'Order Item Id': 'item_id',
    'Order Item Product Price': 'item_product_price',
    'Order Item Profit Ratio': 'item_profit_ratio',
    'Order Item Quantity': 'item_quantity',
    'Sales': 'sales',
    'Order Item Total': 'item_total',
    'Order Profit Per Order': 'profit_per_order',
    'Order Region': 'order_region',
    'Order State': 'order_state',
    'Order Status': 'order_status',
    'Product Card Id': 'product_card_id',
    'Product Category Id': 'product_category_id',
    'Product Name': 'product_name',
    'Product Price': 'product_price',
    'Product Status': 'product_status',
    'shipping date (DateOrders)': 'shipping_date',
    'Shipping Mode': 'shipping_mode',
}


def clean_data():
    """Очищает данные и сохраняет в data/processed/."""
    print("Загружаем сырые данные...")
    df = pd.read_csv(RAW_DATA, encoding='latin-1')
    print(f"  Загружено: {df.shape}")

    # Удаляем мусорные колонки
    print("\nУдаляем мусорные колонки...")
    df = df.drop(columns=DROP_COLUMNS, errors='ignore')
    print(f"  Осталось колонок: {df.shape[1]}")

    # Переименовываем колонки
    print("\nПереименовываем колонки...")
    df = df.rename(columns=RENAME_COLUMNS)

    # Преобразуем даты
    print("\nПреобразуем даты...")
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['shipping_date'] = pd.to_datetime(df['shipping_date'])

    # Сохраняем
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df.to_csv(PROCESSED_DATA, index=False, encoding='utf-8')
    print(f"\nСохранено: {PROCESSED_DATA}")
    print(f"  Размер: {df.shape}")

    return df


if __name__ == "__main__":
    clean_data()