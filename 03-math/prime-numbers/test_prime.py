"""
Тесты для модулей prime_test и prime_gen.
"""

import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prime_test import is_prime_trivial, eratosthenes_sieve, is_prime_m_r
from prime_gen import is_prime, gen_large_prime


class TestPrimeTest(unittest.TestCase):
    """Тесты для модуля проверки простых чисел."""

    def test_is_prime_trivial(self):
        """Тест тривиального метода."""
        self.assertTrue(is_prime_trivial(2))
        self.assertTrue(is_prime_trivial(3))
        self.assertTrue(is_prime_trivial(17))
        self.assertTrue(is_prime_trivial(97))
        self.assertTrue(is_prime_trivial(7919))
        self.assertTrue(is_prime_trivial(104729))

        self.assertFalse(is_prime_trivial(1))
        self.assertFalse(is_prime_trivial(4))
        self.assertFalse(is_prime_trivial(15))
        self.assertFalse(is_prime_trivial(100))

        self.assertFalse(is_prime_trivial(0))
        self.assertFalse(is_prime_trivial(-5))

    def test_eratosthenes_sieve(self):
        """Тест решета Эратосфена."""
        self.assertEqual(eratosthenes_sieve(10), [2, 3, 5, 7])
        self.assertEqual(eratosthenes_sieve(20), [2, 3, 5, 7, 11, 13, 17, 19])
        self.assertEqual(eratosthenes_sieve(1), [])
        self.assertEqual(eratosthenes_sieve(2), [2])

        primes_100 = eratosthenes_sieve(100)
        self.assertEqual(len(primes_100), 25)

    def test_is_prime_m_r(self):
        """Тест метода Миллера-Рабина."""
        self.assertTrue(is_prime_m_r(2))
        self.assertTrue(is_prime_m_r(17))
        self.assertTrue(is_prime_m_r(104729))

        self.assertFalse(is_prime_m_r(1))
        self.assertFalse(is_prime_m_r(4))
        self.assertFalse(is_prime_m_r(15))
        self.assertFalse(is_prime_m_r(104727))

    def test_consistency(self):
        """Тест согласованности."""
        for i in range(2, 200):
            self.assertEqual(
                is_prime_trivial(i),
                is_prime_m_r(i),
                f"Несоответствие для {i}"
            )


class TestPrimeGen(unittest.TestCase):
    """Тесты для модуля генерации простых чисел."""

    def test_is_prime(self):
        """Тест гибридной проверки."""
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(1009))
        self.assertFalse(is_prime(4))

    def test_gen_large_prime(self):
        """Тест генерации простых чисел."""
        for size in [16, 32, 64]:
            prime, attempts = gen_large_prime(size)
            self.assertTrue(is_prime(prime), f"{prime} не простое")
            self.assertGreaterEqual(prime.bit_length(), size - 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)