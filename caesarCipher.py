# Caesar Cipher Algorithm
import imageCrypt

# Algorithm to generate a shift key from pass key
def getShiftKey(passKey):
    ASCII_sum = 0
    for chr in passKey:
        # Increment ASCII sum by ASCII value of character
        print(ord(chr))
        ASCII_sum += ord(chr)

    # If shift key is divisbible by 95, change it to 1
    # as it means it will go all the way round back to the same characters.
    if ASCII_sum % 95 == 0:
        ASCII_sum = 100

    return ASCII_sum

# Encrypts a message
def encryptMessage(plaintext,passKey):
    """
    To encrypt:
    let c = character ASCII value
    let s = shift value

    shiftedValue = (((c - 32) + s) % 95) + 32
    """
    cipherText = ""
    shift = getShiftKey(passKey)

    for i in plaintext:
        # Get ASCII value of each plain text character.
        characterASCII = ord(i)
        print(characterASCII)

        # Get position of encrypted character in ASCII
        shiftedValue = (((characterASCII - 32) + shift) % 95) + 32

        # Get character at the shifted ASCII position.
        newChar = chr(shiftedValue)

        # Concatenate the encrypted character onto the cipher text
        cipherText += newChar

    return cipherText

# Decrypts a message
def decryptMessage(ciphertext,passKey):
    """
    To decrypt:
    let c = encrypted character ASCII value
    let s = shift value

    plainTextCharacterValue = (((c - 32) - s) % 95) + 32
    """
    plainText = ""
    shift = getShiftKey(passKey)

    for i in ciphertext:
        # Get ASCII value of each plain text character.
        characterASCII = ord(i)

        # Get position of decrypted character in ASCII
        shiftedValue = (((characterASCII - 32) - shift) % 95) + 32

        # Get character at the shifted ASCII position.
        newChar = chr(shiftedValue)

        # Concatenate the decrypted character onto the plain text
        plainText += newChar
    return plainText

# Encrypts the contents of a text file
def encryptFile(filename,passKey):
    lines = []
    with open(filename, "r") as file:
        for line in file:
            # Ommit any new line characters to encrypt the raw line itself.
            line = line.strip("\n")

            # Check line is not empty
            if line != "":
                lines.append(encryptMessage(plaintext=line,passKey=passKey)+"\n")

            # Otherwise don't encrypt empty lines.
            # Instead append a new line character to represent blanks
            else:
                lines.append("\n")

    # Sperate original file name into the title and extension
    filenameSplit = filename.split(".")
    newFilename = "{}_encrypted.{}".format(filenameSplit[0],filenameSplit[1])

    with open(newFilename, "w") as file:
        for encryptedLine in lines:
            file.write(encryptedLine)

    return newFilename

# Decrypts the contents of a text file
def decryptFile(filename,passKey):
    lines = []
    with open(filename) as file:
        for line in file:
            # Ommit any new line characters to decrypt the raw line itself.
            line = line.strip("\n")
            # Check line is not empty
            if line != "":
                lines.append(decryptMessage(ciphertext=line,passKey=passKey)+"\n")
            # Otherwise don't decrypt empty lines.
            # Instead append a new line character to represent blanks
            else:
                lines.append("\n")

    # Save the file, now that it's encrypted, to a custom filename

    # Sperate original file name into the title and extension
    filenameSplit = filename.split(".")
    # Get name of original file before being encrypted
    originalFilename = filename.split(".")[0].split("_encrypted")[0]
    # Generate a new file name with _decrypted concatenated onto the original filename
    newFilename = "{}_decrypted.{}".format(originalFilename,filenameSplit[1])
    with open(newFilename, "w") as file:
        for decryptedLine in lines:
            file.write(decryptedLine)

    return newFilename

# Organise how the different dataformats are encrypted
def encryptCheck(passKey,dataformat,plaintext=None,filename=None):
    if dataformat == "message":
        encryptedData = encryptMessage(plaintext=plaintext,passKey=passKey)
    elif dataformat == "file":
        encryptedData = encryptFile(filename=filename,passKey=passKey)
    elif dataformat == "image":
        shift = getShiftKey(passKey=passKey)
        encryptedData = imageCrypt.encrypt(filename=filename,shifts=[shift],cipherUsed="caesar")
    return encryptedData

# Organise how the different dataformats are decrypted
def decryptCheck(passKey,dataformat,ciphertext=None,filename=None):
    if dataformat == "message":
        decryptedData = decryptMessage(ciphertext=ciphertext,passKey=passKey)
    elif dataformat == "file":
        decryptedData = decryptFile(filename=filename,passKey=passKey)
    elif dataformat == "image":
        # imageCrypt module will automatically save the decrypted image
        shift = getShiftKey(passKey=passKey)
        decryptedData = imageCrypt.decrypt(filename=filename,shifts=[shift],cipherUsed="caesar")
    return decryptedData

# Organise the encryption and decryption process
def encrypt(passKey,dataformat,plaintext=None,filename=None):
    return encryptCheck(passKey=passKey,dataformat=dataformat,plaintext=plaintext,filename=filename)

def decrypt(passKey,dataformat,ciphertext=None,filename=None):
    return decryptCheck(passKey=passKey,dataformat=dataformat,ciphertext=ciphertext,filename=filename)
