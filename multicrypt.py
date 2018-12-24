import caesarCipher
import vigenereCipher
import DES_Cipher

# Check the cipher used and return the appropriate ncrypted data
def encrypt(passKey,cipher,dataformat,plaintext=None,filename=None):
    # If the data format is message, a plaintext argument will need to be passed.
    if dataformat == "message":
        if cipher == "caesar":
            encryptedData = caesarCipher.encrypt(plaintext=plaintext,passKey=passKey,dataformat=dataformat)
        elif cipher == "vigenere":
            encryptedData = vigenereCipher.encrypt(plaintext=plaintext,passKey=passKey,dataformat=dataformat)
        elif cipher == "DES":
            encryptedData = DES_Cipher.encrypt(plaintext=plaintext,passKey=passKey,dataformat=dataformat)
        elif cipher == "triple-DES":
            encryptedData = DES_Cipher.encrypt_tripleDES(plaintext=plaintext,passKey=passKey,dataformat=dataformat)

    # If the data format is either a file or an image, a filename argument will need to be passed.
    else:
        if cipher == "caesar":
            encryptedData = caesarCipher.encrypt(filename=filename,passKey=passKey,dataformat=dataformat)
        elif cipher == "vigenere":
            encryptedData = vigenereCipher.encrypt(filename=filename,passKey=passKey,dataformat=dataformat)
        elif cipher == "DES":
            encryptedData = DES_Cipher.encryptImage(filename=filename,passKey=passKey)
        elif cipher == "triple-DES":
            encryptedData = DES_Cipher.encryptImage(filename=filename,passKey=passKey,isTripleDES=True)

    return encryptedData

# Check the cipher used and return appropriate the decrypted data
def decrypt(passKey,cipher,dataformat,ciphertext=None,filename=None):
    # If the data format is message, a plaintext argument will need to be passed.
    if dataformat == "message":
        if cipher == "caesar":
            decryptedData = caesarCipher.decrypt(ciphertext=ciphertext,passKey=passKey,dataformat=dataformat)
        elif cipher == "vigenere":
            decryptedData = vigenereCipher.decrypt(ciphertext=ciphertext,passKey=passKey,dataformat=dataformat)
        elif cipher == "DES":
            decryptedData = DES_Cipher.decrypt(ciphertext=ciphertext,passKey=passKey,dataformat=dataformat)
        elif cipher == "triple-DES":
            decryptedData = DES_Cipher.decrypt_tripleDES(ciphertext=ciphertext,passKey=passKey,dataformat=dataformat)

    # If the data format is either a file or an image, a filename argument will need to be passed.
    else:
        if cipher == "caesar":
            decryptedData = caesarCipher.decrypt(filename=filename,passKey=passKey,dataformat=dataformat)
        elif cipher == "vigenere":
            decryptedData = vigenereCipher.decrypt(filename=filename,passKey=passKey,dataformat=dataformat)
        elif cipher == "DES":
            decryptedData = DES_Cipher.decryptImage(filename=filename,passKey=passKey)
        elif cipher == "triple-DES":
            decryptedData = DES_Cipher.decryptImage(filename=filename,passKey=passKey,isTripleDES=True)

    return decryptedData
