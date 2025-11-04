def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    # Приводим ключ к верхнему регистру для удобства вычислений
    keyword = keyword.upper()
    key_length = len(keyword)

    for i, char in enumerate(plaintext):
        if char.isalpha():
            # Определяем сдвиг для текущего символа
            key_char = keyword[i % key_length]
            shift = ord(key_char) - ord('A')

            # Определяем базовый код в зависимости от регистра
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')

            # Вычисляем зашифрованный символ
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            ciphertext += encrypted_char
        else:
            # Не-буквенные символы остаются без изменений
            ciphertext += char

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    # Приводим ключ к верхнему регистру для удобства вычислений
    keyword = keyword.upper()
    key_length = len(keyword)

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            # Определяем сдвиг для текущего символа
            key_char = keyword[i % key_length]
            shift = ord(key_char) - ord('A')

            # Определяем базовый код в зависимости от регистра
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')

            # Вычисляем исходный символ (вычитаем сдвиг)
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
            plaintext += decrypted_char
        else:
            # Не-буквенные символы остаются без изменений
            plaintext += char

    return plaintext