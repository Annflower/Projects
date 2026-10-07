"""
Тесты для модулей transposition и language_detect.
"""

import unittest
from transposition import transposition_encrypt, transposition_decrypt, brute_force
from language_detect import is_russian, is_english


class TestTransposition(unittest.TestCase):
    """Тесты для шифра перестановки."""

    def test_encrypt_decrypt(self):
        """Тест шифрования и дешифрования."""
        text = "ПРИВЕТМИР"
        key = 3

        encrypted = transposition_encrypt(text, key)
        decrypted = transposition_decrypt(encrypted, key)

        self.assertEqual(decrypted, text)

    def test_encrypt_empty(self):
        """Тест пустого текста."""
        self.assertEqual(transposition_encrypt("", 3), "")
        self.assertEqual(transposition_decrypt("", 3), "")

    def test_invalid_key(self):
        """Тест некорректного ключа."""
        with self.assertRaises(ValueError):
            transposition_encrypt("ТЕКСТ", 0)
        with self.assertRaises(ValueError):
            transposition_decrypt("ТЕКСТ", -1)

    def test_brute_force(self):
        """Тест подбора ключа."""
        text = "Бегемоты, гиппопотамы — род парнокопытных, в который входит один современный вид, обыкновенный бегемот, и значительное число вымерших."
        key = 5

        encrypted = transposition_encrypt(text, key)
        found_key = brute_force(encrypted)

        self.assertIsInstance(found_key, int)
        self.assertGreater(found_key, 0)


class TestLanguageDetect(unittest.TestCase):
    """Тесты для определения языка."""

    def test_is_russian(self):
        """Тест русского текста."""
        self.assertTrue(is_russian("Привет, мир! Как дела?"))
        self.assertTrue(is_russian("Бегемоты и гиппопотамы"))

    def test_is_english(self):
        """Тест английского текста."""
        self.assertTrue(is_english("Hello, world! How are you?"))
        self.assertTrue(is_english("Hippopotamus is a genus"))

    def test_not_russian(self):
        """Тест нерусского текста."""
        self.assertFalse(is_russian("Hello, world!"))


if __name__ == "__main__":
    unittest.main(verbosity=2)