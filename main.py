import nltk
from nltk.corpus import words, names
import string
import ssl


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


nltk.download('words', quiet=True)
nltk.download('names', quiet=True)

try:
    nltk.download('words')
    nltk.download('names')
except:
    print('Error downloading the required NLTK corpus. Please check your internet connection and try again.')

words_list = set(nltk.corpus.words.words())
names_list = set(nltk.corpus.names.words())


def encrypt(plain_text, key):
    cipher_text = ''
    for char in plain_text:
        if char.isalpha():
            int_num = ord(char.upper()) - ord('A')
            shifted_number = (int_num + key) % 26
            shifted_char = chr(shifted_number + ord('A'))
            if char.islower():
                shifted_char = shifted_char.lower()
            cipher_text += shifted_char
        else:
            cipher_text += char
    return cipher_text


def decrypt(cipher_text, key):
    plain_text = ''
    for char in cipher_text:
        if char.isalpha():
            int_num = ord(char.upper()) - ord('A')
            shifted_number = (int_num - key) % 26
            shifted_char = chr(shifted_number + ord('A'))
            if char.islower():
                shifted_char = shifted_char.lower()
            plain_text += shifted_char
        else:
            plain_text += char
    return plain_text


def crack(cipher_text):
    word_list = words.words()
    name_list = names.words()

    # keep track of uppercase letters in the original ciphertext
    uppercase_indices = [i for i, c in enumerate(cipher_text) if c.isupper()]

    # convert cipher_text to lowercase for comparison with word list and name list
    cipher_text = cipher_text.lower()

    for key in range(26):
        plain_text = ''
        for i, char in enumerate(cipher_text):
            if char in string.ascii_lowercase:
                plain_text += chr((ord(char) - key - 97) % 26 + 97)
            elif char in string.ascii_uppercase:
                # handle uppercase letters
                plain_text += chr((ord(char.lower()) - key - 97) % 26 + 97).upper()
            else:
                plain_text += char

        # uppercase the corresponding letters in the decrypted plaintext
        for index in uppercase_indices:
            plain_text = plain_text[:index] + plain_text[index].upper() + plain_text[index+1:]

        # split the decrypted text into words and check if they are in the word list or name list
        decrypted_words = plain_text.split()
        word_match = [word for word in decrypted_words if word in word_list]
        name_match = [word for word in decrypted_words if word in name_list]

        # if more than half the words are in either the word list or name list, return the decrypted text
        if len(word_match) > len(decrypted_words) / 2 or len(name_match) > len(decrypted_words) / 2:
            return plain_text

    return 'Unable to decrypt.'


if __name__ == '__main__':
    print(encrypt('Mandela', 47))
    print(encrypt('zzz', 47))
    print(encrypt('Roger', 47))

    print(decrypt('Hviyzgv', 47))
    print(decrypt('uuu', 47))
    print(decrypt('Mjbzm', 47))

    print(encrypt('apple', 47))
    print(crack('vkkgz'))

    print(encrypt('Mandela', 47))
    print(crack('Hviyzgv'))



