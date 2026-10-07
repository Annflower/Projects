"""
Тесты для модуля number_theory.
Проверяют корректность всех функций.
"""

import unittest
import math
import number_theory as nt


class TestNumberTheory(unittest.TestCase):
    """Тесты для функций теории чисел."""

    def test_mod(self):
        """Тест функции mod."""
        self.assertEqual(nt.mod(23, 7), 2)
        self.assertEqual(nt.mod(-23, 7), 5)
        self.assertEqual(nt.mod(23, -7), 2)
        self.assertEqual(nt.mod(-23, -7), 5)
        self.assertEqual(nt.mod(7, 23), 7)
        self.assertEqual(nt.mod(0, 5), 0)
        self.assertEqual(nt.mod(5, 1), 0)
        self.assertEqual(nt.mod(5, 5), 0)
        self.assertIsNone(nt.mod(7, 0))

    def test_gcd_functions(self):
        """Тест всех функций НОД."""
        test_cases = [
            (48, 18), (-12, 18), (17, 19), (100, 25),
            (0, 5), (5, 0), (1, 1), (1, 100),
        ]
        for a, b in test_cases:
            expected = math.gcd(abs(a), abs(b))
            self.assertEqual(nt.gcd_mr(a, b), expected, f"gcd_mr({a}, {b})")
            self.assertEqual(nt.gcd_m(a, b), expected, f"gcd_m({a}, {b})")
            self.assertEqual(nt.gcd_er(a, b), expected, f"gcd_er({a}, {b})")
            self.assertEqual(nt.gcd_e(a, b), expected, f"gcd_e({a}, {b})")

    def test_is_coprime_pairs(self):
        """Тест функции is_coprime_pairs."""
        self.assertTrue(nt.is_coprime_pairs([2, 3, 5]))
        self.assertTrue(nt.is_coprime_pairs([7, 11, 13]))
        self.assertFalse(nt.is_coprime_pairs([2, 4, 6]))
        self.assertFalse(nt.is_coprime_pairs([3, 6, 9]))
        self.assertFalse(nt.is_coprime_pairs([0, 1]))

    def test_residue_systems(self):
        """Тест систем вычетов."""
        self.assertEqual(nt.least_residue_system(5), [0, 1, 2, 3, 4])
        self.assertEqual(nt.absolutely_least_residue_system(5), [-2, -1, 0, 1, 2])
        self.assertEqual(nt.reduced_residue_system(12), [1, 5, 7, 11])

    def test_factorization(self):
        """Тест факторизации."""
        self.assertEqual(nt.factorization(60), [2, 2, 3, 5])
        self.assertEqual(nt.factorization(17), [17])
        self.assertEqual(nt.factorization(100), [2, 2, 5, 5])
        self.assertEqual(nt.factorization(1), [])

    def test_phi_functions(self):
        """Тест функции Эйлера."""
        test_cases = [(1, 1), (2, 1), (3, 2), (5, 4), (10, 4), (12, 4), (30, 8)]
        for n, expected in test_cases:
            self.assertEqual(nt.phi_function_r(n), expected, f"phi_function_r({n})")
            self.assertEqual(nt.phi_function_t(n), expected, f"phi_function_t({n})")

    def test_inverse(self):
        """Тест обратного элемента."""
        self.assertEqual(nt.inverse(3, 11), 4)
        self.assertEqual(nt.inverse(5, 12), 5)
        self.assertIsNone(nt.inverse(3, 6))
        self.assertIsNone(nt.inverse(0, 5))


if __name__ == "__main__":
    unittest.main(verbosity=2)