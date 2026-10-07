"""
solve_tom.py
Решение задачи: найти ключ, которым зашифрован tom_enc.txt.

У нас есть:
- tom_open.txt — открытый текст
- tom_enc.txt — зашифрованный текст
- Нужно найти ключ (число столбцов)
"""

from transposition import transposition_encrypt, transposition_decrypt
from language_detect import is_russian


def read_file(filename):
    """Читает файл в UTF-8."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def find_key(open_text, enc_text, max_key=50):
    """
    Перебирает ключи от 1 до max_key и ищет такой,
    при котором transposition_encrypt(open_text, key) == enc_text.
    """
    print(f"Открытый текст: {len(open_text)} символов")
    print(f"Зашифрованный текст: {len(enc_text)} символов")
    print()

    for key in range(1, max_key + 1):
        try:
            candidate = transposition_encrypt(open_text, key)

            # Сравниваем первые 200 символов (чтобы избежать проблем с пробелами)
            if candidate[:200] == enc_text[:200]:
                print(f"✓ Найден ключ: {key}")
                print(f"  Первые 100 символов шифра: {candidate[:100]}")
                return key

        except Exception as e:
            continue

    print("✗ Ключ не найден в диапазоне 1..50")
    return None


def main():
    print("=" * 60)
    print("ПОИСК КЛЮЧА ШИФРА ВЕРТИКАЛЬНОЙ ПЕРЕСТАНОВКИ")
    print("=" * 60)
    print()

    # Читаем файлы
    try:
        open_text = read_file('tom_open.txt')
        enc_text = read_file('tom_enc.txt')
    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден — {e}")
        print("Убедись, что tom_open.txt и tom_enc.txt лежат в папке ciphers.")
        return

    # Ищем ключ
    key = find_key(open_text, enc_text)

    if key is None:
        print("\nПопробуем другой подход: перебор с проверкой языка.")

        for k in range(1, 51):
            try:
                decrypted = transposition_decrypt(enc_text, k)

                # Проверяем: похоже ли на русский текст
                if is_russian(decrypted) and 'Том' in decrypted:
                    print(f"✓ Возможный ключ: {k}")
                    print(f"  Расшифровка: {decrypted[:100]}")
                    key = k
                    break
            except Exception:
                continue

    if key:
        print(f"\nИТОГ: ключ = {key}")
    else:
        print("\nКлюч не найден. Проверь файлы.")


if __name__ == "__main__":
    main()