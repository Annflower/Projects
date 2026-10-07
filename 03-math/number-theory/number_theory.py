"""
Модуль number_theory.py
Реализация алгоритмов теории чисел.

Содержит:
- mod: остаток от деления
- gcd_mr, gcd_m, gcd_er, gcd_e: НОД (4 метода)
- is_coprime_pairs: проверка взаимной простоты
- least_residue_system: система наименьших неотрицательных вычетов
- absolutely_least_residue_system: система абсолютно наименьших вычетов
- reduced_residue_system: приведенная система вычетов
- gcd_ext_r, gcd_ext: расширенный алгоритм Евклида
- factorization: факторизация числа
- phi_function_r, phi_function_t: функция Эйлера
- inverse: обратный элемент по модулю
"""


def mod(a, m):
    """
    1.1: Остаток от деления a на m (mod(a, m) >= 0).

    Args:
        a: Число
        m: Модуль

    Returns:
        Остаток от деления, или None если m = 0

    Examples:
        >>> mod(23, 7)
        2
        >>> mod(-23, 7)
        5
        >>> mod(23, 0)
        None
    """
    if m == 0:
        return None
    return a % abs(m)


def gcd_mr(num1, num2):
    """
    1.2: НОД методом вычитания (рекурсия).

    Args:
        num1: Первое число
        num2: Второе число

    Returns:
        НОД двух чисел

    Examples:
        >>> gcd_mr(48, 18)
        6
    """
    a, b = abs(num1), abs(num2)

    if a == 0:
        return b
    if b == 0:
        return a

    if a > b:
        return gcd_mr(a - b, b)
    return gcd_mr(a, b - a)


def gcd_m(num1, num2):
    """
    1.3: НОД методом вычитания (цикл).

    Args:
        num1: Первое число
        num2: Второе число

    Returns:
        НОД двух чисел

    Examples:
        >>> gcd_m(48, 18)
        6
    """
    a, b = abs(num1), abs(num2)

    if a == 0 and b == 0:
        return 0
    if a == 0:
        return b
    if b == 0:
        return a

    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a

    return a


def gcd_er(num1, num2):
    """
    1.4: НОД алгоритмом Евклида (рекурсия).

    Args:
        num1: Первое число
        num2: Второе число

    Returns:
        НОД двух чисел

    Examples:
        >>> gcd_er(48, 18)
        6
    """
    a, b = abs(num1), abs(num2)

    if a == 0 and b == 0:
        return 0
    if b == 0:
        return a
    return gcd_er(b, a % b)


def gcd_e(num1, num2):
    """
    1.5: НОД алгоритмом Евклида (цикл).

    Args:
        num1: Первое число
        num2: Второе число

    Returns:
        НОД двух чисел

    Examples:
        >>> gcd_e(48, 18)
        6
    """
    a, b = abs(num1), abs(num2)

    if a == 0 and b == 0:
        return 0
    if a == 0:
        return b
    if b == 0:
        return a

    while b != 0:
        a, b = b, a % b
    return a


def is_coprime_pairs(pairs_list):
    """
    1.6: Проверка взаимной простоты чисел в списке.

    Args:
        pairs_list: Список чисел

    Returns:
        True если все числа взаимно просты, иначе False

    Examples:
        >>> is_coprime_pairs([2, 3, 5])
        True
        >>> is_coprime_pairs([2, 4, 6])
        False
    """
    if len(pairs_list) < 2:
        return False

    for i in range(len(pairs_list)):
        for j in range(i + 1, len(pairs_list)):
            a, b = abs(pairs_list[i]), abs(pairs_list[j])
            if a == 0 or b == 0:
                return False
            if gcd_e(a, b) != 1:
                return False
    return True


def least_residue_system(mod_val):
    """
    2.1: Система наименьших неотрицательных вычетов.

    Args:
        mod_val: Модуль

    Returns:
        Список вычетов [0, 1, ..., mod_val-1]

    Examples:
        >>> least_residue_system(5)
        [0, 1, 2, 3, 4]
    """
    if mod_val <= 0:
        return []
    return list(range(mod_val))


def absolutely_least_residue_system(mod_val):
    """
    2.2: Система абсолютно наименьших вычетов.

    Args:
        mod_val: Модуль

    Returns:
        Список вычетов

    Examples:
        >>> absolutely_least_residue_system(5)
        [-2, -1, 0, 1, 2]
        >>> absolutely_least_residue_system(4)
        [-2, -1, 0, 1]
    """
    if mod_val <= 0:
        return []

    result = []
    if mod_val % 2 == 1:  # нечетный модуль
        start = -(mod_val // 2)
        end = mod_val // 2
    else:  # четный модуль
        start = -(mod_val // 2 - 1)
        end = mod_val // 2

    for i in range(start, end + 1):
        result.append(i)
    return result


def reduced_residue_system(mod_val):
    """
    2.3: Приведенная система вычетов.

    Args:
        mod_val: Модуль

    Returns:
        Список вычетов, взаимно простых с mod_val

    Examples:
        >>> reduced_residue_system(12)
        [1, 5, 7, 11]
    """
    if mod_val <= 0:
        return []

    result = []
    for i in range(1, mod_val):
        if gcd_e(i, mod_val) == 1:
            result.append(i)
    return result


def gcd_ext_r(num1, num2):
    """
    2.4: Расширенный алгоритм Евклида (рекурсия).

    Args:
        num1: Первое число
        num2: Второе число

    Returns:
        Кортеж (d, x, y), где d = НОД, x, y — коэффициенты Безу

    Examples:
        >>> gcd_ext_r(48, 18)
        (6, -1, 3)
    """
    a, b = abs(num1), abs(num2)

    if a == 0 and b == 0:
        return (0, 0, 0)

    def extended_recursive(a, b):
        if b == 0:
            return (a, 1, 0)
        d, x1, y1 = extended_recursive(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (d, x, y)

    d, x, y = extended_recursive(a, b)

    if num1 < 0:
        x = -x
    if num2 < 0:
        y = -y

    return (d, x, y)


def gcd_ext(num1, num2):
    """
    2.5: Расширенный алгоритм Евклида (цикл).

    Args:
        num1: Первое число
        num2: Второе число

    Returns:
        Кортеж (d, u, v), где d = НОД, u, v — коэффициенты Безу

    Examples:
        >>> gcd_ext(48, 18)
        (6, -1, 3)
    """
    if num1 == 0 and num2 == 0:
        return (0, 0, 0)

    a_abs, b_abs = abs(num1), abs(num2)

    u = 1
    d = a_abs

    if b_abs == 0:
        v = 0
    else:
        v1 = 0
        v3 = b_abs

        while v3 != 0:
            q = d // v3
            t3 = d % v3
            t1 = u - q * v1
            u = v1
            d = v3
            v1 = t1
            v3 = t3

        v = (d - u * a_abs) // b_abs

    if num1 < 0:
        u = -u
    if num2 < 0:
        v = -v

    return (d, u, v)


def factorization(num):
    """
    2.6: Факторизация числа.

    Args:
        num: Число

    Returns:
        Список простых множителей

    Examples:
        >>> factorization(60)
        [2, 2, 3, 5]
        >>> factorization(17)
        [17]
    """
    if num == 0 or num == 1:
        return []

    n = abs(num)
    factors = []

    while n % 2 == 0:
        factors.append(2)
        n //= 2

    f = 3
    while f * f <= n:
        if n % f == 0:
            factors.append(f)
            n //= f
        else:
            f += 2

    if n > 1:
        factors.append(n)

    return factors


def phi_function_r(num):
    """
    2.7: Функция Эйлера через приведенную систему вычетов.

    Args:
        num: Число

    Returns:
        Значение функции Эйлера

    Examples:
        >>> phi_function_r(12)
        4
    """
    if num <= 0:
        return None
    if num == 1:
        return 1
    return len(reduced_residue_system(num))


def phi_function_t(num):
    """
    2.8: Функция Эйлера через факторизацию.

    Args:
        num: Число

    Returns:
        Значение функции Эйлера

    Examples:
        >>> phi_function_t(12)
        4
    """
    if num <= 0:
        return None
    if num == 1:
        return 1

    result = num
    factors = set(factorization(num))

    for p in factors:
        result = result * (p - 1) // p

    return result


def inverse(num, mod_val):
    """
    2.9: Обратный элемент по модулю.

    Args:
        num: Число
        mod_val: Модуль

    Returns:
        Обратный элемент, или None если не существует

    Examples:
        >>> inverse(3, 11)
        4
        >>> inverse(3, 6)
        None
    """
    if mod_val <= 1 or gcd_e(num, mod_val) != 1:
        return None

    num_pos = num % mod_val
    if num_pos < 0:
        num_pos += mod_val

    d, x, y = gcd_ext(num_pos, mod_val)
    if d != 1:
        return None

    result = x % mod_val
    if result < 0:
        result += mod_val

    return result


if __name__ == "__main__":
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ ВСЕХ РЕАЛИЗОВАННЫХ ФУНКЦИЙ")
    print("=" * 50)

    print("\n1. Функция mod(a, m):")
    print(f"mod(23, 7) = {mod(23, 7)}")
    print(f"mod(-23, 7) = {mod(-23, 7)}")

    print("\n2. Функции НОД:")
    a, b = 48, 18
    print(f"gcd_e({a}, {b}) = {gcd_e(a, b)}")

    print("\n3. Расширенный алгоритм Евклида:")
    d, x, y = gcd_ext(48, 18)
    print(f"gcd_ext(48, 18) = ({d}, {x}, {y})")
    print(f"Проверка: 48*{x} + 18*{y} = {48*x + 18*y}")

    print("\n4. Факторизация:")
    print(f"factorization(60) = {factorization(60)}")

    print("\n5. Функция Эйлера:")
    for n in [1, 2, 5, 10, 12, 30]:
        print(f"φ({n}) = {phi_function_t(n)}")

    print("\n6. Обратный элемент:")
    print(f"inverse(3, 11) = {inverse(3, 11)}")