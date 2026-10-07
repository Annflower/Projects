"""
Модуль language_detect.py
Определение языка текста (русский/английский).

Использует:
- Словари слов (опционально)
- Процент совпадений букв (основной метод)
"""

import string


def load_english_dictionary():
    """Загружает английский словарь (заглушка)."""
    return set()


def load_russian_dictionary():
    """Загружает русский словарь (заглушка)."""
    return set()


ENGLISH_DICTIONARY = load_english_dictionary()
RUSSIAN_DICTIONARY = load_russian_dictionary()

ENGLISH_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz \t\n'
RUSSIAN_LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя \t\n'


def remove_non_letters(message, allowed_letters):
    """
    Удаляет все символы, кроме разрешенных букв и пробелов.

    Args:
        message: Исходный текст
        allowed_letters: Разрешенные символы

    Returns:
        Очищенный текст
    """
    letters_only = []

    for symbol in message:
        if symbol in allowed_letters:
            letters_only.append(symbol)

    return ''.join(letters_only)


def get_language_count(message, dictionary, allowed_letters):
    """
    Подсчитывает процент слов из словаря в тексте.

    Args:
        message: Текст
        dictionary: Словарь
        allowed_letters: Разрешенные символы

    Returns:
        Процент совпадений
    """
    message_upper = message.upper()
    message_clean = remove_non_letters(message_upper, allowed_letters.upper())
    possible_words = message_clean.split()

    if not possible_words:
        return 0.0

    matches = 0
    for word in possible_words:
        if word in dictionary:
            matches += 1

    return (float(matches) / len(possible_words)) * 100


def is_english(message, letter_percentage=60):
    """
    Проверяет, является ли текст английским.

    Алгоритм: подсчитывает процент английских букв в тексте.
    Если процент >= 60% — текст считается английским.

    Args:
        message: Текст
        letter_percentage: Минимальный процент английских букв

    Returns:
        True если английский
    """
    if not message.strip():
        return False

    english_letters = "abcdefghijklmnopqrstuvwxyz"
    total_letters = sum(1 for char in message.lower() if char.isalpha())

    if total_letters == 0:
        return False

    english_chars = sum(1 for char in message.lower() if char in english_letters)
    letter_match = (english_chars / total_letters) * 100

    return letter_match >= letter_percentage


def is_russian(message, letter_percentage=60):
    """
    Проверяет, является ли текст русским.

    Алгоритм: подсчитывает процент русских букв в тексте.
    Если процент >= 60% — текст считается русским.

    Args:
        message: Текст
        letter_percentage: Минимальный процент русских букв

    Returns:
        True если русский
    """
    if not message.strip():
        return False

    russian_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    total_letters = sum(1 for char in message.lower() if char.isalpha())

    if total_letters == 0:
        return False

    russian_chars = sum(1 for char in message.lower() if char in russian_letters)
    letter_match = (russian_chars / total_letters) * 100

    return letter_match >= letter_percentage


def main():
    """Демонстрация определения языка."""
    print("=" * 50)
    print("ОПРЕДЕЛЕНИЕ ЯЗЫКА ТЕКСТА")
    print("=" * 50)

    test_texts = [
        "Бегемоты, гиппопотамы — род парнокопытных.",
        "Hippopotamus is a genus of artiodactyl mammals.",
    ]

    for text in test_texts:
        print(f"\nТекст: {text[:40]}...")
        print(f"  is_russian: {is_russian(text)}")
        print(f"  is_english: {is_english(text)}")

    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()