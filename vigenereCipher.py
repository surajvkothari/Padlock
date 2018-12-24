# Vigenere Cipher Algorithm
import imageCrypt

# Returns the ASCII value of a character in the shifted ASCII
def posInAscii(i):
  # Return 126 if character is a (SPACE) so it moves to the end of the shifted ASCII table
  # Although, in ASCII, (SPACE) is first; in this shifted ASCII, the first character is a (!) starting at index 1.
  if i == " ":
    return 126
  else:
    return ord(i) - 1

def getShiftsFromPassKey(passKey):
    return [ord(char) for char in passKey]

def getShiftKey(text,passKey):
    """
    This section calculates the pass-key-string to match the message length
    If the pass key is: king
    And the message is: Hide in the forest.
    The pass key should match the length of the message like this:

    k i n g k i n g k i n g k i n g k i
    H i d e   i n   t h e   f o r e s t

    Here the pass key (king) is repeated 4 times as whole.
    This is the result of: len(message) DIV len(passkey)
    The (2) extra characters to fill the rest of the message are: k i
    The (2) comes from the result of: len(message) MOD len(passkey)

    The pass-key-string is the concatenation of the pass key repeated the whole number of times + the remaining characters:
    (king) * 4 + ki
    """

    # Find the whole number of times the pass key is repeated
    repeatedNum = (len(text) // len(passKey))
    # Find the extra characters by slicing that part of from the rest of the pass key
    extraChars = passKey[0:(len(text) % len(passKey))]
    # Concatenate both parts to form the pass-key-string
    passKeyString = (passKey *  repeatedNum) + extraChars

    return passKeyString

# Encrypts a message
def encryptMessage(plaintext,passKey):
    cipherText = ""
    shiftKeyString = getShiftKey(text=plaintext,passKey=passKey)

    # Iterate through the pass-key-string and the message
    for i,j in list(zip(shiftKeyString,plaintext)):
        # Find the ASCII position for each character in the pass key string
        shift = posInAscii(i)

        # Get ASCII value of each plain text character.
        characterASCII = ord(j)

        # Get position of encrypted character in ASCII
        shiftedValue = (((characterASCII - 32) + shift) % 95) + 32

        # Get the character at this position
        newChar = chr(shiftedValue)

        # Concatenate each character onto the encrypted message string
        cipherText += newChar
    return cipherText

# Decrypts a message
def decryptMessage(ciphertext,passKey):
    plainText = ""
    shiftKeyString = getShiftKey(text=ciphertext,passKey=passKey)

    # Iterate through the pass-key-string and the message
    for i,j in list(zip(shiftKeyString,ciphertext)):
        # Find the ASCII position for each character in the pass key string
        shift = posInAscii(i)

        # Get ASCII value of each cipher text character.
        characterASCII = ord(j)

        # Get position of decrypted character in ASCII
        shiftedValue = (((characterASCII - 32) - shift) % 95) + 32

        # Get the character at this position
        newChar = chr(shiftedValue)
        # Concatenate each character onto the encrypted message string
        plainText += newChar
    return plainText

# Encrypts the contents of a text file
def encryptFile(filename,passKey):
    pass

# Decrypts the contents of a text file
def decryptFile(filename,passKey):
    pass

# Organise how the different dataformats are encrypted
def encryptCheck(passKey,dataformat,plaintext=None,filename=None):
    if dataformat == "message":
        encryptedData = encryptMessage(plaintext=plaintext,passKey=passKey)
    elif dataformat == "file":
        encryptedData = encryptFile(filename=filename,passKey=passKey)
    elif dataformat == "image":
        shifts = getShiftsFromPassKey(passKey=passKey)
        encryptedData = imageCrypt.encrypt(filename=filename,shifts=shifts,cipherUsed="vigenere")
    return encryptedData
# Organise how the different dataformats are decrypted
def decryptCheck(passKey,dataformat,ciphertext=None,filename=None):
    if dataformat == "message":
        decryptedData = decryptMessage(ciphertext=ciphertext,passKey=passKey)
    elif dataformat == "file":
        decryptedData = decryptFile(filename=filename,passKey=passKey)
    elif dataformat == "image":
        shifts = getShiftsFromPassKey(passKey=passKey)
        decryptedData = imageCrypt.decrypt(filename=filename,shifts=shifts,cipherUsed="vigenere")
    return decryptedData

# Organise the encryption and decryption process
def encrypt(passKey,dataformat,plaintext=None,filename=None):
    return encryptCheck(passKey,dataformat,plaintext=plaintext,filename=filename)

def decrypt(passKey,dataformat,ciphertext=None,filename=None):
    return decryptCheck(passKey,dataformat,ciphertext=ciphertext,filename=filename)
