# Caesar Cipher Algorithm

import imageCrypt


def getShiftKey(passKey):
    """Returns a shift key value from the pass key"""

    ASCII_sum = 0

    for chr in passKey:
        ASCII_sum += ord(chr)

    """
    If the shift key value generated is a multiple of 95, then change it to 100
    as a shift of 95 would obtain the same character.
    """
    if ASCII_sum % 95 == 0:
        ASCII_sum = 100

    return ASCII_sum


def encryptMessage(plaintext, passKey):
    """Encrypts a plaintext with a passkey"""

    cipherText = ""
    shift = getShiftKey(passKey)

    for i in plaintext:
        characterASCII = ord(i)

        # Gets the new position of the encrypted character in ASCII
        shiftedValue = (((characterASCII - 32) + shift) % 95) + 32

        # Gets the character at the new position.
        newChar = chr(shiftedValue)

        # Concatenates the encrypted character onto the ciphertext
        cipherText += newChar

    return cipherText


def decryptMessage(ciphertext, passKey):
    """Decrypts a ciphertext with a passkey"""

    plainText = ""

    shift = getShiftKey(passKey)

    for i in ciphertext:
        characterASCII = ord(i)

        # Gets the new position of the decrypted character in ASCII
        shiftedValue = (((characterASCII - 32) - shift) % 95) + 32

        # Gets the character at the new position.
        newChar = chr(shiftedValue)

        # Concatenates the decrypted character onto the plaintext
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
        shift = getShiftKey(passKey=passKey)
        encryptedData = imageCrypt.encrypt(filename=filename, filepath=filepath, shifts=[shift], cipherUsed="caesar")

    return encryptedData


def decryptCheck(passKey, dataformat, ciphertext=None, filename=None, filepath=None):
    """Organises how the different dataformats are decrypted"""
    if dataformat == "Messages":
        decryptedData = decryptMessage(ciphertext=ciphertext, passKey=passKey)
    elif dataformat == "Files":
        decryptedData = decryptFile(filename=filename, passKey=passKey)
    elif dataformat == "Images":
        shift = getShiftKey(passKey=passKey)
        decryptedData = imageCrypt.decrypt(filename=filename, filepath=filepath, shifts=[shift], cipherUsed="caesar")

    return decryptedData


def encrypt(passKey, dataformat, plaintext=None, filename=None, filepath=None):
    return encryptCheck(passKey=passKey, dataformat=dataformat, plaintext=plaintext, filename=filename, filepath=filepath)


def decrypt(passKey, dataformat, ciphertext=None, filename=None, filepath=None):
    return decryptCheck(passKey=passKey, dataformat=dataformat, ciphertext=ciphertext, filename=filename, filepath=filepath)
