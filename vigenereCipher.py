# Vigenere Cipher Algorithm

import imageCrypt


def getPositionInAscii(i):
    """
    Returns the ASCII value of a character minus 1.
    """

    """
    Returns 126 if character is a (SPACE).
    In ASCII, (SPACE) is first, however in this shifted ASCII,
    the first character is a (!) starting at index 1.
    """
    if i == " ":
        return 126
    else:
        return ord(i) - 1


def getShiftValuesFromPassKey(passKey):
    """Returns a list of ASCII values for each character in the passkey"""

    return [ord(char) for char in passKey]


def getPassKeyString(text, passKey):
    """
    Returns the special pass-key-string.

    This section calculates the pass-key-string to match the message length.

    Let the passkey be: king
    Let the message be: Hide in the forest.
    The pass-key-string length should match the length of the message like this:

    k i n g k i n g k i n g k i n g k i
    H i d e   i n   t h e   f o r e s t

    Here, the passkey (king) is repeated 4 whole times.
    This is the result of: len(message) DIV len(passkey).
    The (2) extra characters to fill the rest of the message are: k i
    The (2) comes from the result of: len(message) MOD len(passkey).

    The pass-key-string is the concatenation of the passkey repeated
    the (whole number of times + the remaining characters):
    ("king" * 4) + ki
    (kingkingkingkingki)
    """

    # Gets the whole number of times the pass key is repeated
    repeatedNum = (len(text) // len(passKey))

    # Gets the remaining characters
    extraChars = passKey[0:(len(text) % len(passKey))]

    """
    Repeats the original passkey the correct number of times
    and then concatenates both parts to form the pass-key-string.
    """
    passKeyString = (passKey * repeatedNum) + extraChars

    return passKeyString


def encryptMessage(plaintext, passKey):
    """Encrypts a plaintext with the passkey"""

    cipherText = ""
    passKeyString = getPassKeyString(text=plaintext, passKey=passKey)

    # Iterates through the pass-key-string and the plaintext simultaneously
    for keyChar, plaintextChar in list(zip(passKeyString, plaintext)):
        # Gets the ASCII position for each character in the pass key string
        shift = getPositionInAscii(keyChar)

        # Gets ASCII value of each plain text character
        characterASCII = ord(plaintextChar)

        # Gets new position of encrypted character in ASCII
        shiftedValue = (((characterASCII - 32) + shift) % 95) + 32

        # Gets the character at this new position
        newChar = chr(shiftedValue)

        # Concatenates each encrypted character onto the plaintext string
        cipherText += newChar

    return cipherText


def decryptMessage(ciphertext, passKey):
    """Decrypts a ciphertext with the passkey"""

    plainText = ""
    passKeyString = getPassKeyString(text=ciphertext, passKey=passKey)

    # Iterates through the pass-key-string and the ciphertext simultaneously
    for keyChar, plaintextChar in list(zip(passKeyString, ciphertext)):
        # Finds the ASCII position for each character in the pass key string
        shift = getPositionInAscii(keyChar)

        # Gets ASCII value of each ciphertext character.
        characterASCII = ord(plaintextChar)

        # Gets position of decrypted character in ASCII
        shiftedValue = (((characterASCII - 32) - shift) % 95) + 32

        # Gets the character at this position
        newChar = chr(shiftedValue)

        # Concatenates each decrypted character onto the ciphertext string
        plainText += newChar

    return plainText


def encryptFile(filename, passKey):
    """Encrypts the contents of a text file"""
    pass


def decryptFile(filename, passKey):
    """Decrypts the contents of a text file"""
    pass


def encryptCheck(passKey, dataformat, plaintext=None, filename=None, filepath=None):
    """Organises how the different dataformats are encrypted"""

    if dataformat == "Messages":
        encryptedData = encryptMessage(plaintext=plaintext, passKey=passKey)
    elif dataformat == "Files":
        encryptedData = encryptFile(filename=filename, passKey=passKey)
    elif dataformat == "Images":
        shifts = getShiftValuesFromPassKey(passKey=passKey)
        encryptedData = imageCrypt.encrypt(filename=filename, filepath=filepath, shifts=shifts, cipherUsed="vigenere")

    return encryptedData


def decryptCheck(passKey, dataformat, ciphertext=None, filename=None, filepath=None):
    """Organises how the different dataformats are decrypted"""

    if dataformat == "Messages":
        decryptedData = decryptMessage(ciphertext=ciphertext, passKey=passKey)
    elif dataformat == "Files":
        decryptedData = decryptFile(filename=filename, passKey=passKey)
    elif dataformat == "Images":
        shifts = getShiftValuesFromPassKey(passKey=passKey)
        decryptedData = imageCrypt.decrypt(filename=filename, filepath=filepath, shifts=shifts, cipherUsed="vigenere")

    return decryptedData


def encrypt(passKey, dataformat, plaintext=None, filename=None, filepath=None):
    return encryptCheck(passKey, dataformat, plaintext=plaintext, filename=filename, filepath=filepath)


def decrypt(passKey, dataformat, ciphertext=None, filename=None, filepath=None):
    return decryptCheck(passKey, dataformat, ciphertext=ciphertext, filename=filename, filepath=filepath)
