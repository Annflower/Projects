# Простые числа

Модуль с алгоритмами проверки и генерации простых чисел.

## Описание

Реализация классических алгоритмов:

- Проверка перебором
- Решето Эратосфена
- Тест Миллера-Рабина
- Генерация больших простых чисел

## Функции

| Функция                  | Описание                               |
| ------------------------------- | ---------------------------------------------- |
| `is_prime_trivial(n)`         | Проверка перебором            |
| `eratosthenes_sieve(border)`  | Решето Эратосфена              |
| `is_prime_m_r(n, iterations)` | Тест Миллера-Рабина           |
| `is_prime(n)`                 | Гибридная проверка            |
| `gen_large_prime(keysize)`    | Генерация простого числа |

## Использование

```python
from prime_test import is_prime_trivial, eratosthenes_sieve
from prime_gen import gen_large_prime

# Проверка
print(is_prime_trivial(17))          # True

# Решето
print(eratosthenes_sieve(10))        # [2, 3, 5, 7]

# Генерация
prime, attempts = gen_large_prime(64)
print(f"Найдено за {attempts} попыток")
```

## Тесты

**bash**

```
python -m unittest test_prime.py
```

## Автор

Анна Германова
