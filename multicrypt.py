# Organises the encryption and decryption processes

import caesarCipher
import vigenereCipher
import DES_Cipher


def encrypt(passKey, cipher, dataformat, plaintext=None, filename=None, filepath=None):
    """Checks the cipher used and returns the requested encrypted data"""

    # If the data format is message, a plaintext argument will need to be passed.
    if dataformat == "Messages":
        if cipher == "Caesar Cipher":
            encryptedData = caesarCipher.encrypt(plaintext=plaintext, passKey=passKey, dataformat=dataformat)
        elif cipher == "Vigenere Cipher":
            encryptedData = vigenereCipher.encrypt(plaintext=plaintext, passKey=passKey, dataformat=dataformat)
        elif cipher == "DES Cipher":
            encryptedData = DES_Cipher.encrypt(plaintext=plaintext, passKey=passKey, dataformat=dataformat)
        elif cipher == "Triple DES Cipher":
            encryptedData = DES_Cipher.encrypt_tripleDES(plaintext=plaintext, passKey=passKey, dataformat=dataformat)

    # If the data format is either a file or an image, a filename argument will need to be passed.
    else:
        if cipher == "Caesar Cipher":
            encryptedData = caesarCipher.encrypt(filename=filename, filepath=filepath, passKey=passKey, dataformat=dataformat)
        elif cipher == "Vigenere Cipher":
            encryptedData = vigenereCipher.encrypt(filename=filename, filepath=filepath, passKey=passKey, dataformat=dataformat)
        elif cipher == "DES Cipher":
            encryptedData = DES_Cipher.encryptImage(filename=filename, filepath=filepath, passKey=passKey)
        elif cipher == "Triple DES Cipher":
            encryptedData = DES_Cipher.encryptImage(filename=filename, filepath=filepath, passKey=passKey, isTripleDES=True)

    return encryptedData


def decrypt(passKey, cipher, dataformat, ciphertext=None, filename=None, filepath=None):
    """Checks the cipher used and returns the requested decrypted data"""

    # If the data format is message, a ciphertext argument will need to be passed.
    if dataformat == "Messages":
        if cipher == "Caesar Cipher":
            decryptedData = caesarCipher.decrypt(ciphertext=ciphertext, passKey=passKey, dataformat=dataformat)
        elif cipher == "Vigenere Cipher":
            decryptedData = vigenereCipher.decrypt(ciphertext=ciphertext, passKey=passKey, dataformat=dataformat)
        elif cipher == "DES Cipher":
            decryptedData = DES_Cipher.decrypt(ciphertext=ciphertext, passKey=passKey, dataformat=dataformat)
        elif cipher == "Triple DES Cipher":
            decryptedData = DES_Cipher.decrypt_tripleDES(ciphertext=ciphertext, passKey=passKey, dataformat=dataformat)

    # If the data format is either a file or an image, a filename argument will need to be passed.
    else:
        if cipher == "Caesar Cipher":
            decryptedData = caesarCipher.decrypt(filename=filename, filepath=filepath, passKey=passKey, dataformat=dataformat)
        elif cipher == "Vigenere Cipher":
            decryptedData = vigenereCipher.decrypt(filename=filename, filepath=filepath, passKey=passKey, dataformat=dataformat)
        elif cipher == "DES Cipher":
            decryptedData = DES_Cipher.decryptImage(filename=filename, filepath=filepath, passKey=passKey)
        elif cipher == "Triple DES Cipher":
            decryptedData = DES_Cipher.decryptImage(filename=filename, filepath=filepath, passKey=passKey, isTripleDES=True)

    return decryptedData
