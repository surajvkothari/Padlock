# Caesar Cipher Algorithm

import imageCrypt

guide_data = {}


def getShiftKey(passKey):
    """Returns a shift key value from the pass key"""

    ASCII_sum = 0

    for chr in passKey:
        ASCII_sum += ord(chr)

    """
    If the shift key value generated is a multiple of 95, then add 50 to it
    as a shift of 95 would obtain the same character.
    """
    guide_data['c_key'] = ASCII_sum  # Before

    if ASCII_sum % 95 == 0:
        ASCII_sum += 50

    guide_data['f_c_key'] = ASCII_sum  # After
    return ASCII_sum


def encryptMessage(plaintext, passKey):
    """Encrypts a plaintext with a passkey"""

    guide_data['fc'] = 'Encryption'
    guide_data['txt'] = plaintext
    guide_data['key'] = passKey

    cipherText = ""
    shift = getShiftKey(passKey)

    for x, i in enumerate(plaintext):
        characterASCII = ord(i)

        # Gets the new position of the encrypted character in ASCII
        shiftedValue = (((characterASCII - 32) + shift) % 95) + 32

        # We only need to save the first shifted value
        if x == 0:
            guide_data['sv'] = shiftedValue

        # Gets the character at the new position.
        newChar = chr(shiftedValue)

        # Concatenates the encrypted character onto the ciphertext
        cipherText += newChar

    guide_data['f_txt'] = cipherText

    return cipherText


def decryptMessage(ciphertext, passKey):
    """Decrypts a ciphertext with a passkey"""

    guide_data['fc'] = 'Decryption'
    guide_data['txt'] = ciphertext
    guide_data['key'] = passKey

    plainText = ""

    shift = getShiftKey(passKey)

    for x, i in enumerate(ciphertext):
        characterASCII = ord(i)

        # Gets the new position of the decrypted character in ASCII
        shiftedValue = (((characterASCII - 32) - shift) % 95) + 32

        # We only need to save the first shifted value
        if x == 0:
            guide_data['sv'] = shiftedValue

        # Gets the character at the new position.
        newChar = chr(shiftedValue)

        # Concatenates the decrypted character onto the plaintext
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

    newFilename = "{}/{}_{}ENC.txt".format(filepath, filename[:-4], 'caesar')

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
        shift = getShiftKey(passKey=passKey)
        encryptedData = imageCrypt.encrypt(filename=filename, filepath=filepath, shifts=[shift], cipherUsed="caesar")

    return encryptedData


def decryptCheck(passKey, dataformat, ciphertext=None, filename=None, filepath=None):
    """Organises how the different dataformats are decrypted"""
    if dataformat == "Messages":
        decryptedData = decryptMessage(ciphertext=ciphertext, passKey=passKey)
    elif dataformat == "Files":
        decryptedData = decryptFile(filename=filename, filepath=filepath, passKey=passKey)
    elif dataformat == "Images":
        shift = getShiftKey(passKey=passKey)
        decryptedData = imageCrypt.decrypt(filename=filename, filepath=filepath, shifts=[shift], cipherUsed="caesar")

    return decryptedData


def encrypt(passKey, dataformat, plaintext=None, filename=None, filepath=None):
    return guide_data, encryptCheck(passKey=passKey, dataformat=dataformat, plaintext=plaintext, filename=filename, filepath=filepath)


def decrypt(passKey, dataformat, ciphertext=None, filename=None, filepath=None):
    return guide_data, decryptCheck(passKey=passKey, dataformat=dataformat, ciphertext=ciphertext, filename=filename, filepath=filepath)
