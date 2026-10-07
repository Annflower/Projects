"""
Модуль prime_test.py
Реализация алгоритмов проверки чисел на простоту.

Содержит:
- is_prime_trivial: проверка перебором
- eratosthenes_sieve: решето Эратосфена
- is_prime_m_r: тест Миллера-Рабина
"""

import math
import random


def is_prime_trivial(number: int) -> bool:
    """
    Проверяет простоту числа методом последовательного деления.

    Args:
        number: Проверяемое число

    Returns:
        True для простого числа, False для составного

    Examples:
        >>> is_prime_trivial(17)
        True
        >>> is_prime_trivial(15)
        False
    """
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    upper_bound = math.isqrt(number)
    for divisor in range(3, upper_bound + 1, 2):
        if number % divisor == 0:
            return False
    return True


def eratosthenes_sieve(border: int) -> list:
    """
    Генерирует список простых чисел до заданного предела
    с помощью оптимизированного решета Эратосфена.

    Args:
        border: Верхняя граница

    Returns:
        Список простых чисел

    Examples:
        >>> eratosthenes_sieve(10)
        [2, 3, 5, 7]
    """
    if border < 2:
        return []
    if border == 2:
        return [2]

    is_prime = [True] * (border + 1)
    is_prime[0] = is_prime[1] = False
    is_prime[2] = True

    for i in range(4, border + 1, 2):
        is_prime[i] = False

    max_check = math.isqrt(border)
    for current in range(3, max_check + 1, 2):
        if is_prime[current]:
            for multiple in range(current * current, border + 1, 2 * current):
                is_prime[multiple] = False

    primes = [2]
    primes.extend(i for i in range(3, border + 1, 2) if is_prime[i])
    return primes


def is_prime_m_r(number: int, iterations: int = 5) -> bool:
    """
    Определяет простоту числа с помощью вероятностного
    теста Миллера-Рабина.

    Args:
        number: Проверяемое число
        iterations: Количество проверочных итераций

    Returns:
        Вероятностный результат проверки на простоту

    Examples:
        >>> is_prime_m_r(104729)
        True
        >>> is_prime_m_r(104727)
        False
    """
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    if number in {3, 5, 7, 11, 13, 17, 19, 23, 29, 31}:
        return True

    m = number - 1
    k = 0
    while m % 2 == 0:
        m //= 2
        k += 1

    def single_iteration(base: int) -> bool:
        x = pow(base, m, number)
        if x in (1, number - 1):
            return True
        for _ in range(k - 1):
            x = pow(x, 2, number)
            if x == number - 1:
                return True
            if x == 1:
                return False
        return False

    if number < 2**64:
        deterministic_bases = (
            [2] if number < 2047 else
            [2, 3] if number < 1373653 else
            [31, 73] if number < 9080191 else
            [2, 3, 5] if number < 25326001 else
            [2, 3, 5, 7] if number < 3215031751 else
            [2, 7, 61] if number < 4759123141 else
            [2, 13, 23, 1662803] if number < 1122004669633 else
            [2, 3, 5, 7, 11] if number < 2152302898747 else
            [2, 3, 5, 7, 11, 13] if number < 3474749660383 else
            [2, 3, 5, 7, 11, 13, 17] if number < 341550071728321 else
            [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        )
        for base in deterministic_bases:
            if base >= number:
                continue
            if not single_iteration(base):
                return False
        return True

    for _ in range(iterations):
        base = random.randint(2, number - 2)
        if not single_iteration(base):
            return False
    return True


def main():
    """Демонстрация работы алгоритмов."""
    print("=" * 50)
    print("ПРОВЕРКА ЧИСЕЛ НА ПРОСТОТУ")
    print("=" * 50)

    print("\n1. Метод перебора:")
    for n in [2, 3, 17, 25, 97]:
        print(f"   is_prime_trivial({n}) = {is_prime_trivial(n)}")

    print("\n2. Решето Эратосфена:")
    for limit in [10, 20, 50]:
        print(f"   eratosthenes_sieve({limit}) = {eratosthenes_sieve(limit)}")

    print("\n3. Тест Миллера-Рабина:")
    for n in [2, 15, 104729, 104727]:
        print(f"   is_prime_m_r({n}) = {is_prime_m_r(n)}")

    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()