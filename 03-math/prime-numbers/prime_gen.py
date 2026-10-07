"""
Модуль prime_gen.py
Генерация больших простых чисел.

Гибридный алгоритм: предварительная проверка + тест Миллера-Рабина.
"""

import random
import time
import math
from typing import Tuple, List
from prime_test import eratosthenes_sieve, is_prime_m_r

LOW_PRIMES: List[int] = eratosthenes_sieve(1000)


def is_prime(number: int) -> bool:
    """
    Проверяет, является ли число простым (гибридный алгоритм).

    Args:
        number: Проверяемое число

    Returns:
        True если простое, иначе False
    """
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    if number <= 1000:
        return number in LOW_PRIMES

    for prime in LOW_PRIMES:
        if number % prime == 0:
            return False

    if number < 10**6:
        iterations = 20
    elif number < 10**12:
        iterations = 30
    else:
        iterations = 40

    return is_prime_m_r(number, iterations)


def is_prime_pure_mr(number: int) -> bool:
    """Проверка простоты чистым тестом Миллера-Рабина."""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    return is_prime_m_r(number, 40)


def gen_large_prime(keysize: int = 1024, pure_mr: bool = False) -> Tuple[int, int]:
    """
    Генерирует большое простое число заданного размера в битах.

    Args:
        keysize: Размер числа в битах (минимум 2)
        pure_mr: Если True, использует чистый тест Миллера-Рабина

    Returns:
        Кортеж (простое_число, количество_попыток)
    """
    if keysize < 2:
        raise ValueError("Размер ключа должен быть >= 2 бит")

    min_value = 2**(keysize - 1)
    max_value = 2**keysize - 1

    attempts = 0
    max_attempts = 10000

    while attempts < max_attempts:
        attempts += 1

        num = random.randint(min_value, max_value)
        if num % 2 == 0:
            num += 1 if num < max_value else -1

        if pure_mr:
            if is_prime_pure_mr(num):
                return num, attempts
        else:
            if is_prime(num):
                return num, attempts

    raise RuntimeError(f"Не удалось найти простое число за {max_attempts} попыток")


def benchmark(size_bits: int, trials: int = 50) -> dict:
    """Проводит бенчмарк для заданного размера ключа."""
    hybrid_attempts = []
    hybrid_times = []
    pure_attempts = []
    pure_times = []

    for _ in range(trials):
        start = time.perf_counter()
        _, attempts = gen_large_prime(size_bits, pure_mr=False)
        end = time.perf_counter()
        hybrid_attempts.append(attempts)
        hybrid_times.append(end - start)

        start = time.perf_counter()
        _, attempts = gen_large_prime(size_bits, pure_mr=True)
        end = time.perf_counter()
        pure_attempts.append(attempts)
        pure_times.append(end - start)

    def avg(lst):
        return sum(lst) / len(lst) if lst else 0

    return {
        'size': size_bits,
        'hybrid_avg_attempts': avg(hybrid_attempts),
        'hybrid_avg_time': avg(hybrid_times),
        'pure_avg_attempts': avg(pure_attempts),
        'pure_avg_time': avg(pure_times),
        'speedup': avg(pure_times) / avg(hybrid_times) if avg(hybrid_times) > 0 else 0
    }


def main():
    """Демонстрация генерации простых чисел."""
    print("=" * 60)
    print("ГЕНЕРАЦИЯ БОЛЬШИХ ПРОСТЫХ ЧИСЕЛ")
    print("=" * 60)

    print("\n1. Проверка на известных простых числах:")
    for n in [2, 3, 17, 1009, 7919, 10007]:
        print(f"   is_prime({n:6}) = {is_prime(n)}")

    print("\n2. Генерация простых чисел:")
    for size in [64, 128, 256]:
        prime, attempts = gen_large_prime(size)
        print(f"   {size}-битное: найдено за {attempts} попыток")

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()