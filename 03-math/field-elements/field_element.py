"""
Модуль field_element.py
Реализация класса FieldElement для работы с полями Галуа.

Класс FieldElement представляет элемент конечного поля F_p,
где p — простое число.

Поддерживает операции:
- Сложение, вычитание
- Умножение, деление
- Возведение в степень
- Отрицание
- Сравнение
"""


class FieldElement:
    """
    Элемент конечного поля F_p.

    Атрибуты:
        num: Число (0 <= num < prime)
        prime: Модуль (простое число)

    Examples:
        >>> a = FieldElement(7, 13)
        >>> b = FieldElement(12, 13)
        >>> a + b
        FieldElement_13(6)
        >>> a * b
        FieldElement_13(6)
    """

    def __init__(self, num, prime):
        """
        Создаёт элемент поля.

        Args:
            num: Число
            prime: Модуль (простое число)

        Raises:
            ValueError: Если num или prime некорректны
        """
        if not isinstance(num, int) or not isinstance(prime, int):
            raise ValueError(f'Числа {num} и {prime} должны быть целыми')
        if prime <= 1:
            raise ValueError(f'Модуль {prime} должен быть простым числом > 1')
        if num >= prime or num < 0:
            raise ValueError(f'Число {num} не из промежутка от 0 до {prime - 1}')

        self.num = num
        self.prime = prime

    def __repr__(self):
        """Строковое представление."""
        return f'FieldElement_{self.prime}({self.num})'

    def __eq__(self, other):
        """Сравнение на равенство."""
        if not isinstance(other, FieldElement):
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        """Сравнение на неравенство."""
        return not self == other

    def __add__(self, other):
        """
        Сложение двух элементов.

        Examples:
            >>> FieldElement(7, 13) + FieldElement(12, 13)
            FieldElement_13(6)
        """
        if self.prime != other.prime:
            raise TypeError('Нельзя складывать элементы из разных полей')
        num = (self.num + other.num) % self.prime
        return FieldElement(num, self.prime)

    def __sub__(self, other):
        """
        Вычитание двух элементов.

        Examples:
            >>> FieldElement(7, 13) - FieldElement(12, 13)
            FieldElement_13(8)
        """
        if self.prime != other.prime:
            raise TypeError('Нельзя вычитать элементы из разных полей')
        num = (self.num - other.num) % self.prime
        return FieldElement(num, self.prime)

    def __mul__(self, other):
        """
        Умножение двух элементов.

        Examples:
            >>> FieldElement(7, 13) * FieldElement(12, 13)
            FieldElement_13(6)
        """
        if self.prime != other.prime:
            raise TypeError('Нельзя перемножать элементы из разных полей')
        num = (self.num * other.num) % self.prime
        return FieldElement(num, self.prime)

    def __pow__(self, exponent):
        """
        Возведение в степень.

        Examples:
            >>> FieldElement(7, 13) ** 2
            FieldElement_13(10)
        """
        if not isinstance(exponent, int):
            raise ValueError(f'Показатель степени {exponent} должен быть целым')

        if self.num == 0 and exponent > 0:
            return FieldElement(0, self.prime)

        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return FieldElement(num, self.prime)

    def __truediv__(self, other):
        """
        Деление двух элементов.

        Examples:
            >>> FieldElement(7, 13) / FieldElement(12, 13)
            FieldElement_13(8)
        """
        if self.prime != other.prime:
            raise TypeError('Нельзя делить элементы из разных полей')
        if other.num == 0:
            raise ZeroDivisionError('Деление на ноль в конечном поле')

        inverse = pow(other.num, self.prime - 2, self.prime)
        num = (self.num * inverse) % self.prime
        return FieldElement(num, self.prime)

    def __neg__(self):
        """
        Отрицание элемента.

        Examples:
            >>> -FieldElement(7, 13)
            FieldElement_13(6)
        """
        num = (-self.num) % self.prime
        return FieldElement(num, self.prime)


def main():
    """Демонстрация работы с полями Галуа."""
    print("=" * 50)
    print("ПОЛЯ ГАЛУА F_p")
    print("=" * 50)

    print("\n1. Создание элементов поля F_17:")
    a = FieldElement(8, 17)
    b = FieldElement(12, 17)
    c = FieldElement(3, 17)
    print(f"   a = {a}")
    print(f"   b = {b}")
    print(f"   c = {c}")

    print("\n2. Арифметические операции:")
    print(f"   a + b = {a + b}")
    print(f"   a - b = {a - b}")
    print(f"   a * b = {a * b}")
    print(f"   a / b = {a / b}")
    print(f"   -a = {-a}")

    print("\n3. Возведение в степень:")
    print(f"   a^2 = {a ** 2}")
    print(f"   a^3 = {a ** 3}")

    print("\n4. Обратный элемент в F_31:")
    for x in [7, 15, 30]:
        elem = FieldElement(x, 31)
        inverse = FieldElement(pow(x, 31 - 2, 31), 31)
        print(f"   {x}^(-1) = {inverse}")
        print(f"   Проверка: {x} * {inverse.num} mod 31 = {(x * inverse.num) % 31}")

    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()