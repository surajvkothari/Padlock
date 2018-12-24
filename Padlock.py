#!/usr/bin/env python3
"""
Padlock Encryption Software
Copyright 2018
Created by: Suraj Kothari
"""

import multicrypt

def encryptMenu(cipher,dataFormat):
    print("   Encrypting {} with {} Cipher".format(dataFormat,cipher.title()))
    print()
    if dataFormat == "message":
        print("Enter plaintext:")
        plainText = input()
        while True:
            print("Enter passkey:")
            passKey = input()
            # Ensure the pass key entered is >= to 8 characters in length
            if len(passKey) >= 8:
                break
            else:
                print("Pass key must be at least 8 characters long.")
                print()

        if cipher == "triple-DES":
            while True:
                print("Enter second passkey:")
                passKey2 = input()
                # Ensure the second pass key entered is also >= to 8 characters in length
                if len(passKey2) >= 8:
                    break
                else:
                    print("Pass key must be at least 8 characters long.")
                    print()

            cipherText = multicrypt.encrypt(plaintext=plainText, passKey=(passKey,passKey2), cipher=cipher, dataformat=dataFormat)
        else:
            cipherText = multicrypt.encrypt(plaintext=plainText, passKey=passKey, cipher=cipher, dataformat=dataFormat)

        print("-"*40)
        print("Encrypted ciphertext:")
        print(cipherText)
        print("-"*40)

        mainMenu()
    elif dataFormat == "file":
        print("Enter file location:")
        fileLocation = input()
        while True:
            print("Enter passkey:")
            passKey = input()
            # Ensure the pass key entered is >= to 8 characters in length
            if len(passKey) >= 8:
                break
            else:
                print("Pass key must be at least 8 characters long.")
                print()

        encryptedFileLocation = multicrypt.encrypt(filename=fileLocation, passKey=passKey, cipher=cipher, dataformat=dataFormat)
        print("-"*40)
        print("Encrypted file saved as:")
        print(encryptedFileLocation)
        print("-"*40)

        mainMenu()
    elif dataFormat == "image":
        print("Enter image location:")
        fileLocation = input()
        while True:
            print("Enter passkey:")
            passKey = input()
            if len(passKey) >= 8:
                break
            else:
                print("Pass key must be at least 8 characters long.")
                print()

        if cipher == "triple-DES":
            while True:
                print("Enter second passkey:")
                passKey2 = input()
                # Ensure the second pass key entered is also >= to 8 characters in length
                if len(passKey2) >= 8:
                    break
                else:
                    print("Pass key must be at least 8 characters long.")
                    print()

            encryptedImageLocation = multicrypt.encrypt(filename=fileLocation, passKey=(passKey,passKey2), cipher=cipher, dataformat=dataFormat)
        else:
            encryptedImageLocation = multicrypt.encrypt(filename=fileLocation, passKey=passKey, cipher=cipher, dataformat=dataFormat)
        print("-"*40)
        print("Encrypted image saved as:")
        print(encryptedImageLocation)
        print("-"*40)

        mainMenu()

def decryptMenu(cipher,dataFormat):
    print("   Decrypting {} with {} Cipher".format(dataFormat,cipher.title()))

    print()
    if dataFormat == "message":
        print("Enter ciphertext:")
        cipherText = input()
        while True:
            print("Enter passkey:")
            passKey = input()
            if len(passKey) >= 8:
                break
            else:
                print("Pass key must be at least 8 characters long.")
                print()

        if cipher == "triple-DES":
            while True:
                print("Enter second passkey:")
                passKey2 = input()
                if len(passKey2) >= 8:
                    break
                else:
                    print("Pass key must be at least 8 characters long.")
                    print()

            plaintext = multicrypt.decrypt(ciphertext=cipherText, passKey=(passKey,passKey2), cipher=cipher, dataformat=dataFormat)
        else:
            plaintext = multicrypt.decrypt(ciphertext=cipherText, passKey=passKey, cipher=cipher, dataformat=dataFormat)

        print("-"*40)
        print("Decrypted plaintext:")
        print(plaintext)
        print("-"*40)

        mainMenu()
    elif dataFormat == "file":
        print("Enter encrypted file location:")
        fileLocation = input()
        print("Enter passkey:")
        passKey = input()
        decryptedFileLocation = multicrypt.decrypt(filename=fileLocation, passKey=passKey, cipher=cipher, dataformat=dataFormat)
        print("-"*40)
        print("Decrypted file saved at:")
        print(decryptedFileLocation)
        print("-"*40)

        mainMenu()
    elif dataFormat == "image":
        print("Enter encrypted image location:")
        fileLocation = input()
        while True:
            print("Enter passkey:")
            passKey = input()
            if len(passKey) >= 8:
                break
            else:
                print("Pass key must be at least 8 characters long.")
                print()

        if cipher == "triple-DES":
            while True:
                print("Enter second passkey:")
                passKey2 = input()
                # Ensure the second pass key entered is also >= to 8 characters in length
                if len(passKey2) >= 8:
                    break
                else:
                    print("Pass key must be at least 8 characters long.")
                    print()

            decryptedImageLocation = multicrypt.decrypt(filename=fileLocation, passKey=(passKey,passKey2), cipher=cipher, dataformat=dataFormat)
        else:
            decryptedImageLocation = multicrypt.decrypt(filename=fileLocation, passKey=passKey, cipher=cipher, dataformat=dataFormat)
        print("-"*40)
        print("Decrypted image saved at:")
        print(decryptedImageLocation)
        print("-"*40)

        mainMenu()
def cipherMenu(cipher,dataFormat):
    print("   {} Cipher on {}".format(cipher.title(),dataFormat))
    print()
    print("Choose process:")
    print("1. Encrypt the {}".format(dataFormat))
    print("2. Decrypt the {}".format(dataFormat))
    print("3. Back to cipher menu")

    while True:
        processOption = input(">> ")
        if processOption == "1":
            print("-"*40)
            encryptMenu(cipher=cipher,dataFormat=dataFormat)
            break
        elif processOption == "2":
            print("-"*40)
            decryptMenu(cipher=cipher,dataFormat=dataFormat)
            break
        elif processOption == "3":
            print("-"*40)
            cryptographyMenu(dataFormat=dataFormat)
            break
        else:
            print("ERROR. Invalid option.")

def cryptographyMenu(dataFormat):
    print("   {} encryption/decryption".format(dataFormat.title()))
    print()
    print("Choose a cipher:")
    print("1. Caesar Cipher on {}".format(dataFormat))
    print("2. Vigenere Cipher on {}".format(dataFormat))
    print("3. DES Cipher on {}".format(dataFormat))
    print("4. Triple DES Cipher on {}".format(dataFormat))
    print("5. Back to main menu")
    while True:
        cipherOption = input(">> ")
        if cipherOption == "1":
            print("-"*40)
            cipherMenu(cipher="caesar",dataFormat=dataFormat)
            break
        elif cipherOption == "2":
            print("-"*40)
            cipherMenu(cipher="vigenere",dataFormat=dataFormat)
            break
        elif cipherOption == "3":
            print("-"*40)
            cipherMenu(cipher="DES",dataFormat=dataFormat)
            break
        elif cipherOption == "4":
            print("-"*40)
            cipherMenu(cipher="triple-DES",dataFormat=dataFormat)
            break
        elif cipherOption == "5":
            print("-"*40)
            mainMenu()
            break
        else:
            print("ERROR. Invalid option.")

def mainMenu():
    print("--------------------------------")
    print(" Padlock Encryption Software ")
    print("--------------------------------")
    print()
    print("Choose a format to encrypt/decrypt:")
    print("1. Message")
    print("2. File")
    print("3. Image")
    print("4. Quit")

    while True:
        formatOption = input(">> ")
        if formatOption == "1":
            print("-"*40)
            cryptographyMenu(dataFormat="message")
            break
        elif formatOption == "2":
            print("-"*40)
            cryptographyMenu(dataFormat="file")
            break
        elif formatOption == "3":
            print("-"*40)
            cryptographyMenu(dataFormat="image")
            break
        elif formatOption == "4":
            print("-"*40)
            exit()
            break
        else:
            print("ERROR. Invalid option.")

if __name__ == '__main__':
    mainMenu()
