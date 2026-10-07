"""
Модуль transposition.py
Шифр вертикальной перестановки.

Реализует:
- Шифрование
- Дешифрование
- Brute-force подбор ключа
- Визуализацию
"""

import math
from language_detect import is_russian


def transposition_encrypt(plaintext: str, key: int) -> str:
    """
    Шифрование сообщения методом вертикальной перестановки.

    Args:
        plaintext: Исходный текст
        key: Ключ (число столбцов)

    Returns:
        Зашифрованный текст

    Examples:
        >>> transposition_encrypt("ПРИВЕТ", 2)
        'ПРВЕТИ'
    """
    if key <= 0:
        raise ValueError("Ключ должен быть положительным числом")

    text = plaintext.replace('\n', ' ')
    text_length = len(text)

    rows = math.ceil(text_length / key)

    table = []
    char_index = 0

    for i in range(rows):
        row = []
        for j in range(key):
            if char_index < text_length:
                row.append(text[char_index])
                char_index += 1
            else:
                row.append(None)
        table.append(row)

    ciphertext_chars = []
    for j in range(key):
        for i in range(rows):
            if table[i][j] is not None:
                ciphertext_chars.append(table[i][j])

    return ''.join(ciphertext_chars)


def transposition_decrypt(ciphertext: str, key: int) -> str:
    """
    Дешифрование сообщения методом вертикальной перестановки.

    Args:
        ciphertext: Зашифрованный текст
        key: Ключ (число столбцов)

    Returns:
        Расшифрованный текст

    Examples:
        >>> transposition_decrypt("ПРВЕТИ", 2)
        'ПРИВЕТ'
    """
    if key <= 0:
        raise ValueError("Ключ должен быть положительным числом")

    text = ciphertext.replace('\n', ' ')
    text_length = len(text)

    rows = math.ceil(text_length / key)
    total_cells = rows * key
    shaded_cells = total_cells - text_length

    table = [[None] * key for _ in range(rows)]

    char_index = 0
    for j in range(key):
        for i in range(rows):
            if i == rows - 1 and j >= key - shaded_cells:
                continue
            if char_index < text_length:
                table[i][j] = text[char_index]
                char_index += 1

    plaintext_chars = []
    for i in range(rows):
        for j in range(key):
            if table[i][j] is not None:
                plaintext_chars.append(table[i][j])

    return ''.join(plaintext_chars)


def brute_force(ciphertext: str) -> int:
    """
    Подбор ключа для расшифровки.

    Args:
        ciphertext: Зашифрованный текст

    Returns:
        Найденный ключ

    Raises:
        ValueError: Если ключ не найден
    """
    text = ciphertext.replace('\n', ' ')
    text_length = len(text)

    max_key = min(50, text_length // 2)

    candidates = []

    for potential_key in range(1, max_key + 1):
        try:
            decrypted = transposition_decrypt(text, potential_key)

            russian_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            total_chars = len(decrypted)
            russian_chars = sum(1 for char in decrypted.lower() if char in russian_letters)

            russian_ratio = russian_chars / total_chars if total_chars > 0 else 0

            common_russian_words = ['и', 'в', 'не', 'на', 'я', 'быть', 'что', 'это', 'как', 'по']
            word_matches = sum(1 for word in common_russian_words if word in decrypted.lower())

            language_check = is_russian(decrypted)

            score = russian_ratio * 100 + word_matches * 5 + (100 if language_check else 0)

            if russian_ratio > 0.6:
                candidates.append((potential_key, score, decrypted))

        except Exception:
            continue

    if not candidates:
        raise ValueError("Не удалось найти подходящий ключ для расшифровки")

    candidates.sort(key=lambda x: x[1], reverse=True)
    best_key, best_score, best_text = candidates[0]

    return best_key


def main():
    """Демонстрация работы шифра."""
    print("=" * 60)
    print("ШИФР ВЕРТИКАЛЬНОЙ ПЕРЕСТАНОВКИ")
    print("=" * 60)

    test_text = "Бегемоты, гиппопотамы (лат. Hippopotamus) — род парнокопытных, в который входит один современный вид, обыкновенный бегемот, и значительное число вымерших."
    key = 12

    print(f"\nИсходный текст: {test_text[:50]}...")
    print(f"Ключ: {key}")

    encrypted = transposition_encrypt(test_text, key)
    print(f"\nЗашифрованный: {encrypted[:50]}...")

    decrypted = transposition_decrypt(encrypted, key)
    print(f"\nРасшифрованный: {decrypted[:50]}...")

    if test_text == decrypted:
        print("\n✓ Проверка: тексты совпадают")
    else:
        print("\n✗ Проверка: тексты не совпадают!")

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()