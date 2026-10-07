"""
Модуль language_detect.py
Определение языка текста (русский/английский).

Использует:
- Словари слов
- Процент совпадений
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


def is_english(message, word_percentage=20, letter_percentage=60):
    """
    Проверяет, является ли текст английским.

    Args:
        message: Текст
        word_percentage: Минимальный процент английских слов
        letter_percentage: Минимальный процент английских букв

    Returns:
        True если английский
    """
    if not message.strip():
        return False

    word_match = get_language_count(message, ENGLISH_DICTIONARY, ENGLISH_LETTERS)
    clean_message = remove_non_letters(message, ENGLISH_LETTERS)

    if len(message) == 0:
        return False

    letter_match = (len(clean_message) / len(message)) * 100

    return word_match >= word_percentage and letter_match >= letter_percentage


def is_russian(message, word_percentage=20, letter_percentage=60):
    """
    Проверяет, является ли текст русским.

    Args:
        message: Текст
        word_percentage: Минимальный процент русских слов
        letter_percentage: Минимальный процент русских букв

    Returns:
        True если русский
    """
    if not message.strip():
        return False

    # Если в тексте есть русские буквы — считаем русским
    russian_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    russian_chars = sum(1 for char in message.lower() if char in russian_letters)

    if len(message) == 0:
        return False

    letter_match = (russian_chars / len(message)) * 100

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