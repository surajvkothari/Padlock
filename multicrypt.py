# Multicrypt organisation module

"""
Padlock Encryption Software
Copyright 2019

Created by: Suraj Kothari
For A-level Computer Science
at Woodhouse College.
"""

import caesarCipher
import vigenereCipher
import DES_Cipher
import AES_Cipher


def encrypt(passKey, cipher, dataformat, plaintext=None, filename=None, filepath=None, cipherMode=None):
    """ Checks the cipher used and returns the requested encrypted data """

    # If the data format is message, a plaintext argument will need to be passed.

    if dataformat == "Messages":
        if cipher == "Caesar Cipher":
            guide_data, encryptedData = caesarCipher.encrypt(plaintext=plaintext,
                passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

        elif cipher == "Vigenere Cipher":
            guide_data, encryptedData = vigenereCipher.encrypt(plaintext=plaintext,
                passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

        elif cipher == "DES Cipher":
            guide_data, encryptedData = DES_Cipher.encrypt(plaintext=plaintext,
                passKey=passKey, dataformat=dataformat)

        elif cipher == "Triple DES Cipher":
            guide_data, encryptedData = DES_Cipher.encrypt(plaintext=plaintext,
                passKey=passKey, dataformat=dataformat, isTripleDES=True)

        elif cipher == "AES Cipher":
            guide_data, encryptedData = AES_Cipher.encrypt(plaintext=plaintext,
                passKey=passKey, dataformat=dataformat)

    # If the data format is either a file or an image, a filename argument will need to be passed.

    else:
        if cipher == "Caesar Cipher":
            guide_data, encryptedData = caesarCipher.encrypt(filename=filename,
                filepath=filepath, passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

        elif cipher == "Vigenere Cipher":
            guide_data, encryptedData = vigenereCipher.encrypt(filename=filename,
                filepath=filepath, passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

        elif cipher == "DES Cipher":
            guide_data, encryptedData = DES_Cipher.encrypt(filename=filename,
                filepath=filepath, passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

        elif cipher == "Triple DES Cipher":
            guide_data, encryptedData = DES_Cipher.encrypt(filename=filename, filepath=filepath,
                passKey=passKey, dataformat=dataformat, cipherMode=cipherMode, isTripleDES=True)

        elif cipher == "AES Cipher":
            guide_data, encryptedData = AES_Cipher.encrypt(filename=filename,
                filepath=filepath, passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

    return guide_data, encryptedData


def decrypt(passKey, cipher, dataformat, ciphertext=None, filename=None, filepath=None, cipherMode=None):
    """ Checks the cipher used and returns the requested decrypted data """

    # If the data format is message, a ciphertext argument will need to be passed.

    if dataformat == "Messages":
        if cipher == "Caesar Cipher":
            guide_data, decryptedData = caesarCipher.decrypt(ciphertext=ciphertext,
                passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

        elif cipher == "Vigenere Cipher":
            guide_data, decryptedData = vigenereCipher.decrypt(ciphertext=ciphertext,
                passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

        elif cipher == "DES Cipher":
            guide_data, decryptedData = DES_Cipher.decrypt(ciphertext=ciphertext,
                passKey=passKey, dataformat=dataformat)

        elif cipher == "Triple DES Cipher":
            guide_data, decryptedData = DES_Cipher.decrypt(ciphertext=ciphertext,
                passKey=passKey, dataformat=dataformat, isTripleDES=True)

        elif cipher == "AES Cipher":
            guide_data, decryptedData = AES_Cipher.decrypt(ciphertext=ciphertext,
                passKey=passKey, dataformat=dataformat)


    # If the data format is either a file or an image, a filename argument will need to be passed.

    else:
        if cipher == "Caesar Cipher":
            guide_data, decryptedData = caesarCipher.decrypt(filename=filename,
                filepath=filepath, passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

        elif cipher == "Vigenere Cipher":
            guide_data, decryptedData = vigenereCipher.decrypt(filename=filename,
                filepath=filepath, passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

        elif cipher == "DES Cipher":
            guide_data, decryptedData = DES_Cipher.decrypt(filename=filename,
                filepath=filepath, passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

        elif cipher == "Triple DES Cipher":
            guide_data, decryptedData = DES_Cipher.decrypt(filename=filename, filepath=filepath,
                passKey=passKey, dataformat=dataformat, cipherMode=cipherMode, isTripleDES=True)

        elif cipher == "AES Cipher":
            guide_data, decryptedData = AES_Cipher.decrypt(filename=filename,
                filepath=filepath, passKey=passKey, dataformat=dataformat, cipherMode=cipherMode)

    return guide_data, decryptedData
