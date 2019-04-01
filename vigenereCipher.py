# Vigenere Cipher Algorithm

"""
Padlock Encryption Software
Copyright 2019

Created by: Suraj Kothari
For A-level Computer Science
at Woodhouse College.
"""

import imageCrypt
import itertools
import os
import base64

guide_data = {}


def getShiftValuesForImages(passKey):
    """Returns a list of ASCII values for each character in the passkey for image encryption and decryption"""

    return [ord(char) for char in passKey]


def getPassKeyString_classic(text, passKey):
    # A generator cycling through the characters in the pass key
    passKeyCycle = itertools.cycle(passKey)

    passKeyString = ""

    for i, t in enumerate(text, 1):
        if t.isalpha():
            nextKey = next(passKeyCycle)  # Gets the next key
            passKeyString += nextKey

            # If text is smaller than 5, then not all keywords are needed for guide data
            if len(text) <= 5:
                # Inititialises all keywords to a blank value
                guide_data['pks_demo_t1'] = ""
                guide_data['pks_demo_k1'] = ""
                guide_data['pks_demo_t2'] = ""
                guide_data['pks_demo_k2'] = ""
                guide_data['pks_demo_t3'] = ""
                guide_data['pks_demo_k3'] = ""
                guide_data['pks_demo_t4'] = ""
                guide_data['pks_demo_k4'] = ""
                guide_data['pks_demo_t5'] = ""
                guide_data['pks_demo_k5'] = ""

            if i == 1:
                guide_data['pks_demo_t1'] = t
                guide_data['pks_demo_k1'] = nextKey
            elif i == 2:
                guide_data['pks_demo_t2'] = t
                guide_data['pks_demo_k2'] = nextKey
            elif i == 3:
                guide_data['pks_demo_t3'] = t
                guide_data['pks_demo_k3'] = nextKey
            elif i == 4:
                guide_data['pks_demo_t4'] = t
                guide_data['pks_demo_k4'] = nextKey
            elif i == 5:
                guide_data['pks_demo_t5'] = t
                guide_data['pks_demo_k5'] = nextKey
        else:
            # Add on any special characters WITHOUT incrementing the key character
            passKeyString += t

            if i == 1:
                guide_data['pks_demo_t1'] = t
                guide_data['pks_demo_k1'] = t
            elif i == 2:
                guide_data['pks_demo_t2'] = t
                guide_data['pks_demo_k2'] = t
            elif i == 3:
                guide_data['pks_demo_t3'] = t
                guide_data['pks_demo_k3'] = t
            elif i == 4:
                guide_data['pks_demo_t4'] = t
                guide_data['pks_demo_k4'] = t
            elif i == 5:
                guide_data['pks_demo_t5'] = t
                guide_data['pks_demo_k5'] = t

    guide_data['pks'] = passKeyString

    return passKeyString


def getPassKeyString_ASCII(text, passKey):
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

    guide_data['pks_n'] = repeatedNum
    guide_data['pks_r'] = extraChars
    guide_data['pks'] = passKeyString

    return passKeyString


def encryptMessage_CLASSIC(plaintext, passKey):
    """Encrypts a plaintext with the passkey in CLASSIC mode"""

    guide_data['fc'] = 'Encryption'
    guide_data['txt'] = plaintext
    guide_data['key'] = passKey

    cipherText = ""

    passKeyString = getPassKeyString_classic(text=plaintext, passKey=passKey)

    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # Iterates through the pass-key-string and the plaintext simultaneously
    for x, (keyChar, plaintextChar) in enumerate(list(zip(passKeyString, plaintext))):
        if plaintextChar.lower() in alphabet:
            if plaintextChar.isupper():
                # Gets the letter position for each letter in the pass key string
                passKeyString_letter = alphabet.index(keyChar.lower()) + 1

                # Gets the letter position of each plain text character
                character_letter = alphabet.index(plaintextChar.lower()) + 1

                # Gets new position of encrypted character in the alphabet
                shiftedValue = (((character_letter - 1) + (passKeyString_letter - 1)) % 26) + 1

                # Gets the character at this new position
                newChar = alphabet[shiftedValue - 1]

                # We only need to save the first shifted value and new character
                if x == 0:
                    guide_data['sv'] = shiftedValue
                    guide_data['nc'] = newChar

                # Concatenates each encrypted character onto the plaintext string
                cipherText += newChar.upper()

            else:
                # Gets the letter position for each letter in the pass key string
                passKeyString_letter = alphabet.index(keyChar.lower()) + 1

                # Gets the letter position of each plain text character
                character_letter = alphabet.index(plaintextChar.lower()) + 1

                # Gets new position of encrypted character in the alphabet
                shiftedValue = (((character_letter - 1) + (passKeyString_letter - 1)) % 26) + 1

                # Gets the character at this new position
                newChar = alphabet[shiftedValue - 1]

                # We only need to save the first shifted value and new character
                if x == 0:
                    guide_data['sv'] = shiftedValue
                    guide_data['nc'] = newChar

                # Concatenates each encrypted character onto the plaintext string
                cipherText += newChar
        else:
            # Any non-alphabetical character is just added
            cipherText += plaintextChar

    guide_data['f_txt'] = cipherText

    return cipherText


def encryptMessage_ASCII(plaintext, passKey):
    """Encrypts a plaintext with the passkey in ASCII mode"""

    guide_data['fc'] = 'Encryption'
    guide_data['txt'] = plaintext
    guide_data['key'] = passKey

    cipherText = ""
    passKeyString = getPassKeyString_ASCII(text=plaintext, passKey=passKey)

    # Iterates through the pass-key-string and the plaintext simultaneously
    for x, (keyChar, plaintextChar) in enumerate(list(zip(passKeyString, plaintext))):
        # Gets the ASCII value for each character in the pass key string
        passKeyString_ASCII = ord(keyChar)

        # Gets ASCII value of each plain text character
        character_ASCII = ord(plaintextChar)

        # Gets new position of encrypted character in ASCII
        shiftedValue = (((character_ASCII - 32) + (passKeyString_ASCII - 32)) % 95) + 32

        # Gets the character at this new position
        newChar = chr(shiftedValue)

        # We only need to save the first shifted value and new character
        if x == 0:
            guide_data['sv'] = shiftedValue
            guide_data['nc'] = newChar

        # Concatenates each encrypted character onto the plaintext string
        cipherText += newChar

    guide_data['f_txt'] = cipherText

    return cipherText


def decryptMessage_CLASSIC(ciphertext, passKey):
    """Decrypts a ciphertext with the passkey in CLASSIC mode"""

    guide_data['fc'] = 'Decryption'
    guide_data['txt'] = ciphertext
    guide_data['key'] = passKey

    plainText = ""

    passKeyString = getPassKeyString_classic(text=ciphertext, passKey=passKey)

    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # Iterates through the pass-key-string and the plaintext simultaneously
    for x, (keyChar, ciphertextChar) in enumerate(list(zip(passKeyString, ciphertext))):
        if ciphertextChar.lower() in alphabet:
            if ciphertextChar.isupper():
                # Gets the letter position for each letter in the pass key string
                passKeyString_letter = alphabet.index(keyChar.lower()) + 1

                # Gets the letter position of each plain text character
                character_letter = alphabet.index(ciphertextChar.lower()) + 1

                # Gets new position of encrypted character in the alphabet
                shiftedValue = (((character_letter - 1) - (passKeyString_letter - 1)) % 26) + 1

                # Gets the character at this new position
                newChar = alphabet[shiftedValue - 1]

                # We only need to save the first shifted value and new character
                if x == 0:
                    guide_data['sv'] = shiftedValue
                    guide_data['nc'] = newChar

                # Concatenates each encrypted character onto the plaintext string
                plainText += newChar.upper()

            else:
                # Gets the letter position for each letter in the pass key string
                passKeyString_letter = alphabet.index(keyChar.lower()) + 1

                # Gets the letter position of each ciphertext character
                character_letter = alphabet.index(ciphertextChar.lower()) + 1

                # Gets new position of encrypted character in the alphabet
                shiftedValue = (((character_letter - 1) - (passKeyString_letter - 1)) % 26) + 1

                # Gets the character at this new position
                newChar = alphabet[shiftedValue - 1]

                # We only need to save the first shifted value and new character
                if x == 0:
                    guide_data['sv'] = shiftedValue
                    guide_data['nc'] = newChar

                # Concatenates each decrypted character onto the plaintext string
                plainText += newChar
        else:
            # Any non-alphabetical character is just added
            plainText += ciphertextChar

    guide_data['f_txt'] = plainText

    return plainText


def decryptMessage_ASCII(ciphertext, passKey):
    """Decrypts a ciphertext with the passkey in ASCII mode"""

    guide_data['fc'] = 'Decryption'
    guide_data['txt'] = ciphertext
    guide_data['key'] = passKey

    plainText = ""
    passKeyString = getPassKeyString_ASCII(text=ciphertext, passKey=passKey)

    # Iterates through the pass-key-string and the ciphertext simultaneously
    for x, (keyChar, ciphertextChar) in enumerate(list(zip(passKeyString, ciphertext))):
        # Finds the ASCII value for each character in the pass key string
        passKeyString_ASCII = ord(keyChar)

        # Gets ASCII value of each ciphertext character.
        character_ASCII = ord(ciphertextChar)

        # Gets position of decrypted character in ASCII
        shiftedValue = (((character_ASCII - 32) - (passKeyString_ASCII - 32)) % 95) + 32

        # Gets the character at this position
        newChar = chr(shiftedValue)

        # We only need to save the first shifted value and new character
        if x == 0:
            guide_data['sv'] = shiftedValue
            guide_data['nc'] = newChar

        # Concatenates each decrypted character onto the ciphertext string
        plainText += newChar

    guide_data['f_txt'] = plainText

    return plainText


def encryptFile(filename, filepath, passKey, cipherMode):
    """Encrypts the contents of a text file"""
    full_filename = filepath + "/" + filename

    # Generates lines from the file
    def getLines():
        with open(full_filename) as f:
            for line in f:
                if line != "\n":
                    yield line.split("\n")[0]
                else:
                    yield "\n"

    # Generates encrypted data
    def getEncryptedData():
        # Gets file lines from generator
        for L in getLines():
            if L != "\n":
                if cipherMode == "ASCII":
                    E = encryptMessage_ASCII(plaintext=L, passKey=passKey)
                else:
                    E = encryptMessage_CLASSIC(plaintext=L, passKey=passKey)

            else:
                E = "\n"

            yield E

    newFilename = "{}/{}_{}ENC.txt".format(filepath, filename[:-4], 'vigenere')

    # Writes each line of encrypted data
    with open(newFilename, 'w') as f2:
        for e in getEncryptedData():
            if e != "\n":
                f2.write(e + "\n")
            else:
                f2.write("\n")

    return newFilename


def encryptFileBase64(filename, filepath, passKey):
    """Encrypts the contents of any file"""
    full_filename = filepath + "/" + filename

    with open(full_filename, "rb") as f:
        test = f.read()
        """
        Converts the binary file contents to base64
        and then formats it into ASCII form.
        """
        encoded = base64.b64encode(test).decode("ascii")

    Encrypted = encryptMessage_ASCII(plaintext=encoded, passKey=passKey)

    extension = os.path.splitext(filename)[1]
    eLength = len(extension)
    newFilename = "{}/{}_{}ENC{}".format(filepath, filename[:-1*(eLength+1)], 'vigenere', extension)

    # Converts the ASCII encryption into bytes form to write to new file
    Encrypted = bytes(Encrypted,'utf-8')

    # Writes encrypted data to new file
    with open(newFilename, 'wb') as f2:
        f2.write(Encrypted)

    return newFilename


def decryptFile(filename, filepath, passKey, cipherMode):
    """Decrypts the contents of a text file"""
    full_filename = filepath + "/" + filename

    # Generates lines from the file
    def getLines():
        with open(full_filename) as f:
            for line in f:
                if line != "\n":
                    yield line.split("\n")[0]
                else:
                    yield "\n"

    # Generates decrypted data
    def getDecryptedData():
        # Gets file lines from generator
        for L in getLines():
            if L != "\n":
                if cipherMode == "ASCII":
                    D = decryptMessage_ASCII(ciphertext=L, passKey=passKey)
                else:
                    D = decryptMessage_CLASSIC(ciphertext=L, passKey=passKey)
            else:
                D = "\n"

            yield D

    newFilename = "{}/{}".format(filepath, filename.replace("ENC", "DEC"))

    # Writes each line of encrypted data
    with open(newFilename, 'w') as f2:
        for d in getDecryptedData():
            if d != "\n":
                f2.write(d + "\n")
            else:
                f2.write("\n")

    return newFilename


def decryptFileBase64(filename, filepath, passKey):
    """Decrypts the contents of any file"""
    full_filename = filepath + "/" + filename

    with open(full_filename, "rb") as f:
        # Formats the binary file into ASCII form.
        content = f.read().decode("ascii")

    Decrypted = decryptMessage_ASCII(ciphertext=content, passKey=passKey)

    newFilename = "{}/{}".format(filepath, filename.replace("ENC", "DEC"))

    # Converts the ASCII into bytes and then decodes it from base64 to original
    decryptedContent = base64.b64decode(bytes(Decrypted,'utf-8'))

    # Creates decrypted file
    with open(newFilename, 'wb') as f2:
        f2.write(decryptedContent)

    return newFilename


def encryptCheck(passKey, dataformat, cipherMode, plaintext=None, filename=None, filepath=None):
    """Organises how the different dataformats are encrypted"""

    if dataformat == "Messages":
        if cipherMode == "ASCII":
            encryptedData = encryptMessage_ASCII(plaintext=plaintext, passKey=passKey)
        else:
            encryptedData = encryptMessage_CLASSIC(plaintext=plaintext, passKey=passKey)

    elif dataformat == "Files":
        if cipherMode == "Base64":
            encryptedData = encryptFileBase64(filename=filename, filepath=filepath, passKey=passKey)
        else:
            encryptedData = encryptFile(filename=filename, filepath=filepath, passKey=passKey, cipherMode=cipherMode)

    elif dataformat == "Images":
        shifts = getShiftValuesForImages(passKey=passKey)
        encryptedData = imageCrypt.encrypt(filename=filename, filepath=filepath, shifts=shifts, cipherUsed="vigenere")

    return encryptedData


def decryptCheck(passKey, dataformat, cipherMode, ciphertext=None, filename=None, filepath=None):
    """Organises how the different dataformats are decrypted"""

    if dataformat == "Messages":
        if cipherMode == "ASCII":
            decryptedData = decryptMessage_ASCII(ciphertext=ciphertext, passKey=passKey)
        else:
            decryptedData = decryptMessage_CLASSIC(ciphertext=ciphertext, passKey=passKey)

    elif dataformat == "Files":
        if cipherMode == "Base64":
            decryptedData = decryptFileBase64(filename=filename, filepath=filepath, passKey=passKey)
        else:
            decryptedData = decryptFile(filename=filename, filepath=filepath, passKey=passKey, cipherMode=cipherMode)

    elif dataformat == "Images":
        shifts = getShiftValuesForImages(passKey=passKey)
        decryptedData = imageCrypt.decrypt(filename=filename, filepath=filepath, shifts=shifts, cipherUsed="vigenere")

    return decryptedData


def encrypt(passKey, dataformat, cipherMode, plaintext=None, filename=None, filepath=None):
    return guide_data, encryptCheck(passKey, dataformat, plaintext=plaintext, filename=filename, filepath=filepath,
        cipherMode=cipherMode)


def decrypt(passKey, dataformat, cipherMode, ciphertext=None, filename=None, filepath=None):
    return guide_data, decryptCheck(passKey, dataformat, ciphertext=ciphertext, filename=filename, filepath=filepath,
        cipherMode=cipherMode)
