# Vigenere Cipher Algorithm

import imageCrypt

guide_data = {}


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

    guide_data['pks_n'] = repeatedNum
    guide_data['pks_r'] = extraChars
    guide_data['pks'] = passKeyString

    return passKeyString


def encryptMessage(plaintext, passKey):
    """Encrypts a plaintext with the passkey"""

    guide_data['fc'] = 'Encryption'
    guide_data['txt'] = plaintext
    guide_data['key'] = passKey

    cipherText = ""
    passKeyString = getPassKeyString(text=plaintext, passKey=passKey)

    # Iterates through the pass-key-string and the plaintext simultaneously
    for x, (keyChar, plaintextChar) in enumerate(list(zip(passKeyString, plaintext))):
        # Gets the ASCII position for each character in the pass key string
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


def decryptMessage(ciphertext, passKey):
    """Decrypts a ciphertext with the passkey"""

    guide_data['fc'] = 'Decryption'
    guide_data['txt'] = ciphertext
    guide_data['key'] = passKey

    plainText = ""
    passKeyString = getPassKeyString(text=ciphertext, passKey=passKey)

    # Iterates through the pass-key-string and the ciphertext simultaneously
    for x, (keyChar, ciphertextChar) in enumerate(list(zip(passKeyString, ciphertext))):
        # Finds the ASCII position for each character in the pass key string
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


def encryptFile(filename, filepath, passKey):
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
                E = encryptMessage(plaintext=L, passKey=passKey)
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


def decryptFile(filename, filepath, passKey):
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
                D = decryptMessage(ciphertext=L, passKey=passKey)
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


def encryptCheck(passKey, dataformat, plaintext=None, filename=None, filepath=None):
    """Organises how the different dataformats are encrypted"""

    if dataformat == "Messages":
        encryptedData = encryptMessage(plaintext=plaintext, passKey=passKey)
    elif dataformat == "Files":
        encryptedData = encryptFile(filename=filename, filepath=filepath, passKey=passKey)
    elif dataformat == "Images":
        shifts = getShiftValuesFromPassKey(passKey=passKey)
        encryptedData = imageCrypt.encrypt(filename=filename, filepath=filepath, shifts=shifts, cipherUsed="vigenere")

    return encryptedData


def decryptCheck(passKey, dataformat, ciphertext=None, filename=None, filepath=None):
    """Organises how the different dataformats are decrypted"""

    if dataformat == "Messages":
        decryptedData = decryptMessage(ciphertext=ciphertext, passKey=passKey)
    elif dataformat == "Files":
        decryptedData = decryptFile(filename=filename, filepath=filepath, passKey=passKey)
    elif dataformat == "Images":
        shifts = getShiftValuesFromPassKey(passKey=passKey)
        decryptedData = imageCrypt.decrypt(filename=filename, filepath=filepath, shifts=shifts, cipherUsed="vigenere")

    return decryptedData


def encrypt(passKey, dataformat, plaintext=None, filename=None, filepath=None):
    return guide_data, encryptCheck(passKey, dataformat, plaintext=plaintext, filename=filename, filepath=filepath)


def decrypt(passKey, dataformat, ciphertext=None, filename=None, filepath=None):
    return guide_data, decryptCheck(passKey, dataformat, ciphertext=ciphertext, filename=filename, filepath=filepath)
