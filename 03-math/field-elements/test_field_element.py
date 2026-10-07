"""
Тесты для модуля field_element.
Проверяют корректность операций в полях Галуа.
"""

import unittest
from field_element import FieldElement


class TestFieldElement(unittest.TestCase):
    """Тесты для класса FieldElement."""

    def test_creation(self):
        """Тест создания элемента поля."""
        a = FieldElement(7, 13)
        self.assertEqual(a.num, 7)
        self.assertEqual(a.prime, 13)

    def test_creation_errors(self):
        """Тест ошибок при создании."""
        with self.assertRaises(ValueError):
            FieldElement(13, 13)  # num >= prime
        with self.assertRaises(ValueError):
            FieldElement(-1, 13)  # num < 0
        with self.assertRaises(ValueError):
            FieldElement(7, 1)    # prime <= 1

    def test_equality(self):
        """Тест сравнения."""
        a = FieldElement(7, 13)
        b = FieldElement(7, 13)
        c = FieldElement(6, 13)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_addition(self):
        """Тест сложения."""
        a = FieldElement(7, 13)
        b = FieldElement(12, 13)
        self.assertEqual(a + b, FieldElement(6, 13))

    def test_subtraction(self):
        """Тест вычитания."""
        a = FieldElement(7, 13)
        b = FieldElement(12, 13)
        self.assertEqual(a - b, FieldElement(8, 13))

    def test_multiplication(self):
        """Тест умножения."""
        a = FieldElement(3, 13)
        b = FieldElement(12, 13)
        self.assertEqual(a * b, FieldElement(10, 13))

    def test_pow(self):
        """Тест возведения в степень."""
        a = FieldElement(3, 13)
        self.assertEqual(a ** 3, FieldElement(1, 13))
        self.assertEqual(a ** 0, FieldElement(1, 13))

    def test_division(self):
        """Тест деления."""
        a = FieldElement(7, 13)
        b = FieldElement(12, 13)
        self.assertEqual(a / b, FieldElement(6, 13))

    def test_negation(self):
        """Тест отрицания."""
        a = FieldElement(7, 13)
        self.assertEqual(-a, FieldElement(6, 13))

    def test_different_fields_error(self):
        """Тест ошибки при операциях с разными полями."""
        a = FieldElement(7, 13)
        b = FieldElement(7, 17)
        with self.assertRaises(TypeError):
            a + b
        with self.assertRaises(TypeError):
            a - b
        with self.assertRaises(TypeError):
            a * b
        with self.assertRaises(TypeError):
            a / b

    def test_division_by_zero(self):
        """Тест деления на ноль."""
        a = FieldElement(7, 13)
        b = FieldElement(0, 13)
        with self.assertRaises(ZeroDivisionError):
            a / b

    def test_inverse_property(self):
        """Тест свойства обратного элемента."""
        for x in [2, 3, 5, 7, 11]:
            a = FieldElement(x, 13)
            inverse = a ** (13 - 2)
            self.assertEqual(a * inverse, FieldElement(1, 13))


if __name__ == "__main__":
    unittest.main(verbosity=2)