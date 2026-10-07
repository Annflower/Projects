# Поля Галуа

Реализация класса `FieldElement` для работы с конечными полями F_p.

## Описание

Класс `FieldElement` представляет элемент конечного поля F_p,с
где p — простое число. Поддерживает все арифметические операции.

## Возможности

- Создание элементов поля
- Сложение, вычитание
- Умножение, деление
- Возведение в степень
- Отрицание
- Сравнение

## Использование

```python
from field_element import FieldElement

# Создание элементов поля F_17
a = FieldElement(8, 17)
b = FieldElement(12, 17)

# Операции
print(a + b)    # FieldElement_17(3)
print(a - b)    # FieldElement_17(13)
print(a * b)    # FieldElement_17(11)
print(a / b)    # FieldElement_17(...)
print(a ** 2)   # FieldElement_17(13)
print(-a)       # FieldElement_17(9)
```


## Тесты

**bash**

```
python -m unittest test_field_element.py
```

## Демонстрация

**bash**

```
python field_element.py
```

## Автор

Анна Германова
