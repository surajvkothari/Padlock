# DES Cipher Algorithm

import imageCrypt
import encryptionBlocks
import os


def getShiftValuesFromPassKey(passKey):
    """Returns a list of denary values converted from their binary representation of the sub-keys"""

    # Converts the passkey into a hex string
    hexedKey = getHexedKey(key=passKey)

    # Runs a process on the hexed key to generate 16 sub-keys
    permutedSubKeys = generateSubKeys(key=hexedKey)

    # Converts the binary value of each subkey to denary
    denaryOfSubKeys = [int(i, 2) for i in permutedSubKeys]

    # Slices the denary values to get the first 4 digits and converts them back to integers
    truncatedDenaryValues = [int(str(i)[0:4]) for i in denaryOfSubKeys]

    return truncatedDenaryValues


def getHexedPlainText(plainText):
    """Returns the plaintext in hex form and separates it into blocks of 16 into a list."""

    # Creates a list of each character from the plaintext
    plainText = list(plainText)

    # Converts each character, in the plaintext, to hex from the list
    hexedCharsList = [hex(ord(char))[2:] for char in plainText]

    # Concatenates the list into a string
    hexedPlainText = "".join(hexedCharsList)

    """
    Padds the hexed plaintext with 0s to the beginning to ensure it is
    a multiple of 16 hexadecimal characters.
    """
    length = len(hexedPlainText)

    # Only add the 0s if the length is not a multiple of 16
    if length % 16 != 0:
        """
        The ammount of padding is determined by finding
        the next multiple of 16 closest to the length: ((length // 16) + 1).
        By subtracting this multiple from the actual length, it will give
        the number of 0s needed to make the length a multiple of 16.
        """
        padding = ((((length // 16) + 1) * 16) - length)

        # Adds the appropriate number of 0s onto the end of the hexed plaintext
        hexedPlainText += ("0"*padding)

    # Separates the hexed message into blocks of 16 into a list
    hexedPlainText = [hexedPlainText[i:i+16] for i in range(0, len(hexedPlainText), 16)]

    return hexedPlainText


def getHexedKey(key):
    """Returns the key in a hex form of exact size: 16 hex characters"""

    # Creates a list of each character from the key
    key = list(key)

    # Converts each character to hex in the list
    hexedCharsList = [hex(ord(char))[2:] for char in key]

    # Converts list into a string
    hexedKey = "".join(hexedCharsList)

    # Padds hexed key with 0s to make it a multiple of 16 hexadecimal characters
    length = len(hexedKey)
    padding = ((((length // 16) + 1) * 16) - length)
    hexedKey += ("0" * padding)

    # Truncates the hexed key to only 16 hex digits long
    hexedKey = hexedKey[0:16]

    return hexedKey


def generateSubKeys(key):
    """Processes the hexed key to generate 16 individual sub-keys"""

    # Converts the hexed key into binary
    binaryKey = getBinaryKey(key=key)

    # Permutates the binary key with PC1
    permutedBinaryKey = permutateBinaryKey_PC1(key=binaryKey)

    # Splits the permuted binary key into two halves
    leftHalf, rightHalf = splitPermutedKey(key=permutedBinaryKey)

    # Gets the 16 sub-keys as a list
    subKeys = getSubKeys(c=leftHalf, d=rightHalf)

    # Permutates the 16 sub-keys with PC2
    permutedSubKeys = permutateSubKeys(keys=subKeys)

    return permutedSubKeys


def getBinaryKey(key):
    """Returns the binary form of the hexed key"""

    # Converts the key to denary from hex, then to binary
    newKey = bin(int(key, 16))[2:]

    # Keeps the binary key in 64bit form by adding 0s to the beginning
    length = len(newKey)
    newKey = newKey.zfill(64 - (length % 64) + length)

    return newKey


def permutateBinaryKey_PC1(key):
    """Returns a permuted binary string using the PC1-block"""

    # Creates a list of each character from the binary key
    key = list(key)

    # Initialises the permuted keys to have a size of 56 bits
    permuted = [0 for x in range(56)]

    # Fetches the PC1-Block from the encryption blocks module
    PC_1 = encryptionBlocks.getPC_1()

    """
    Enumerates over the PC1-Block and sets the value, at the current position
    in the permuted list, to the bit in the position, from the PC1-block,
    of the key.
    """
    for i, pos in enumerate(PC_1, 1):
        permuted[i-1] = key[pos-1]

    # Joins the list into a string og binary
    permuted = "".join(permuted)

    return permuted


def splitPermutedKey(key):
    """Returns the left and right halves of the permuted key"""

    """
    The key is guaranteed to be 56 bits in length
    therefore it is alright to hardcode the index positions to split the key.
    """
    leftHalf = key[0:28]
    rightHalf = key[28:56]

    return leftHalf, rightHalf


def getSubKeys(c, d):
    """Returns the 16 sub-keys"""

    # The list of values to which the two halves of the key will be shifted by:
    shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    # The 2d array stores the pairs of keys which have been shifted
    subKeys = []

    # Initialises the previous sub-keys to the initial separate halves of the key c and d
    cPrev = c
    dPrev = d

    # Iterates over the given shift values
    for s in shifts:
        # Shifts the previous sub-keys by the shift value
        cNext = shiftItems(key=cPrev, shift=s)
        dNext = shiftItems(key=dPrev, shift=s)

        # Changes the previous sub-keys to the current ones
        cPrev = cNext
        dPrev = dNext

        subKeys.append([cNext, dNext])

    return subKeys


def shiftItems(key, shift):
    """Shifts the separate halves of the subkey by the shift value given"""

    # Creates a list of each bit from the binary key
    key = list(key)

    # Shifts (rotates) the key by the shift number
    shiftedKey = key[shift:] + key[:shift]

    # Joins the key into a string
    subKey = "".join(shiftedKey)

    return subKey


def permutateSubKeys(keys):
    """Returns the permuted sub-keys using the PC2-block"""

    # Joins the left and right halves of the sub-keys together into one key
    keys = ["".join(k) for k in keys]

    # Initialises the permuted sub-keys to have a size of 48 bits
    permutedSubKey = [0 for x in range(48)]

    # Stores the 16 permuted sub-keys
    setOfSubKeys = []

    # Fetches the PC2-Block from the encryption blocks module
    PC_2 = encryptionBlocks.getPC_2()

    # Iterates over each key from the 16 sub-keys
    for key in keys:
        # Creates a list of each bit from the key
        key = list(key)

        """
        Enumerates over the PC2-Block and sets the value, at the current
        position in the permuted list, to the bit in the position,
        from the PC2-Block, of the key.
        """
        for i, pos in enumerate(PC_2, 1):
            permutedSubKey[i-1] = key[pos-1]

        """
        Joins the list of permuted sub-keys into a string of binary digits
        Since the list contains integers of 1 and 0, the items need to be
        mapped to a string before joining them.
        """
        binaryString = "".join(map(str, permutedSubKey))

        setOfSubKeys.append(binaryString)

    return setOfSubKeys


def getBinaryMessage(message):
    """Returns the binary form of the plaintext/ciphertext which is a hex string"""

    # Converts the message to denary from hex then to binary
    binary_string = bin(int(message, 16))[2:]

    # Keeps the binary message in 64 bit form by adding 0s to the front
    length = len(message)
    binary_string = binary_string.zfill(64 - (length % 64) + length)

    return binary_string


def permutateMessage(message):
    """Returns the permuted message in binary using the IP-block"""

    # Creates a list of each bit from the binary message
    message = list(message)

    # Initialises the permuted message to have a size of 64 bits
    permuted = [0 for x in range(64)]

    # Fetches the IP-Block from the encryption blocks module
    IP = encryptionBlocks.getIP()

    """
    Enumerates over the IP-Block and sets the value, at the current position
    in the permuted list, to the bit in the position, from the IP-block, of
    the message.
    """
    for i, pos in enumerate(IP, 1):
        permuted[i-1] = message[pos-1]

    # Joins the list into a binary string
    permuted = "".join(permuted)

    return permuted


def splitPermutedMessage(message):
    """Returns the left and right halves of the binary message"""

    """
    The binary message block is guaranteed to be 64 bits in length
    therefore it is alright to hardcode the index positions to split the key.
    """
    leftHalf = message[0:32]
    rightHalf = message[32:64]

    return leftHalf, rightHalf


def encodeIteration(l, r, subKeys):
    """Returns the ciphertext by running the encoding iteration process"""

    # Initialises the previous halves to the inital separate halves of the plaintext
    lPrev = l
    rPrev = r

    # Iterates over each subkey in the list of permuted sub-keys
    for subKey in subKeys:
        """
        Converts the previous left half into a denary value.
        This is essential for later during the XOR operation which requires
        a denary value.
        """
        leftPrev = int(lPrev, 2)

        # Converts the function F's return into a denary value
        F = int(functionF(rightHalf=rPrev, key=subKey), 2)

        """
        Sets the next right half to the binary value of the calculation:
        (previous left half) XOR (F-function value)
        """
        rNext = bin(leftPrev ^ F)

        # Keeps the calculated binary value in 32bit form by adding 0s to the beginning
        rNext = rNext[2:].zfill(32)

        # Sets the next left half to the previous right half
        lNext = rPrev

        # Changes the previous l, r halves to the new ones
        lPrev = lNext
        rPrev = rNext

    """
    Creates a binary string from the two new left and right halves.
    This binary string is reversed by placing the right half before the left half.
    """
    reversedBinary = rNext + lNext

    # Permutates the binary string with IP-1
    permuted = permutate_IP_1(reversedBinary)

    """
    Converts the permuted binary string into a denary value which is then turned
    into a hex value.
    .zfill(16) makes sure the block of ciphertext is 16 hex characters long.
    """
    cipherText = hex(int(permuted, 2))[2:].zfill(16)

    return cipherText


def decodeIteration(l, r, subKeys):
    """Returns the plaintext by running the decoding iteration process"""

    # Initialises the previous halves to the separate halves of the plaintext
    lPrev = l
    rPrev = r

    # For decryption, iterate over each subkey in reverse order
    for subKey in reversed(subKeys):
        # Converts the previous left half into a denary value
        leftPrev = int(lPrev, 2)

        # Converts the function F's return into a denary value
        f = int(functionF(rPrev, subKey), 2)

        """
        Sets the next right half to the binary value of the calculation:
        (previous left half) XOR (F-function value)
        """
        rNext = bin(leftPrev ^ f)

        # Formats the calculated binary value into a 48bit string
        rNext = rNext[2:].zfill(32)

        # Sets the next left half to the previous right half
        lNext = rPrev

        # Changes the previous l, r halves to the new ones
        lPrev = lNext
        rPrev = rNext

    """
    Creates a binary string from the two new left and right halves.
    This binary string is reversed by placing the right half before the left half.
    """
    reversedBinary = rNext + lNext

    # Permutates the binary string with IP-1
    permuted = permutate_IP_1(reversedBinary)

    """
    Converts the permuted binary string into a denary value which is then turned
    into a hex value.
    .zfill(16) makes sure the block of ciphertext is 16 hex characters long.
    """
    cipherText = hex(int(permuted, 2))[2:].zfill(16)

    return cipherText


def functionF(rightHalf, key):
    """
    Function F carries out the XOR addition of the right half with the key.
    It then takes a group of 6bits and turns them into a group of 4bits
    """

    # Converts the key to denary
    key = int(key, 2)

    # Converts the function E's return to denary
    E = int(functionE(rightHalf=rightHalf), 2)

    # Calculates the XOR addition of the key and E function
    xorAddition = bin(key ^ E)

    # Formats the calculated binary value into a 48bit string
    xorAddition = xorAddition[2:].zfill(48)

    # Separates the binary string into 8 groups of 6bits
    blocks = [xorAddition[i:i+6] for i in range(0, len(xorAddition), 6)]

    S_String = ""

    # Enumerates over the binary blocks
    for i, block in enumerate(blocks):
        # Gets a 4bit subblock from function S
        subBlock = functionS(block=block, blockIndex=i)

        S_String += subBlock

    # Permutates the S_String with P
    permutatedS_String = permutateS_String(string=S_String)

    return permutatedS_String


def functionE(rightHalf):
    """Expands the right half from 32bits to 48bits using the E-Block"""

    # Creates a list of each bit
    rightHalf = list(rightHalf)

    # Fetches the E-Block from the encryption blocks module
    E_Table = encryptionBlocks.getE_Table()

    # This will store the expanded right side binary string
    expandedRight = ""

    """
    Iterates over the E-Block to append the bit, at the current position in the
    right half, to the expanded string
    """
    for pos in E_Table:
        expandedRight += rightHalf[pos-1]

    return expandedRight


def functionS(block, blockIndex):
    """Takes in 6 binary bits and returns 4 binary bits using the S-Block"""

    # Fetches the S-BOX for the specific block from the encryption blocks module
    SBOX = encryptionBlocks.getSBox(blockIndex)

    # Gets the first and last bit from the 6 bits input
    first, last = block[0], block[5]

    # Combines the first and last bits of the block to form a 2bit binary value
    i = first + last

    # Gets the middle part of the block to form a 4bit binary value
    j = block[1:5]

    # Converts the binary sections to denary which will represent the index positions
    iPos = int(i, 2)
    jPos = int(j, 2)

    # Gets the number at the position i, j in the SBOX
    outputNum = SBOX[iPos][jPos]

    # Converts the output number into a binary value of 4bits
    binaryOutput = bin(outputNum)[2:].zfill(4)

    return binaryOutput


def permutateS_String(string):
    """Returns the permuted S-String in binary using the P-block"""

    # Fetch the P Block from the encryption blocks module
    P_Table = encryptionBlocks.getP_Table()

    permuted = ""

    # Iterates over the P-Block to append the bit at the current position in the
    # string to the permuted string
    for pos in P_Table:
        permuted += string[pos-1]

    return permuted


def permutate_IP_1(binary):
    """Returns the final permuted binary string using the IP-1-block"""

    # Fetches the IP-1-Block from the encryption blocks module
    IP_1 = encryptionBlocks.getIP_1()

    permuted = ""

    # Iterates over the IP-1-Block to append the bit at the current position in the
    # binary string to the permuted string
    for pos in IP_1:
        permuted += binary[pos-1]

    return permuted


def encrypt(passKey, dataformat, plaintext=None, filename=None, isTripleDES=None):
    """Takes in a plaintext and passkey and returns the ciphertext using DES"""

    if isTripleDES:
        hexedPlainText = plaintext
    else:
        # Converts the plaintext into a hex string
        hexedPlainText = getHexedPlainText(plainText=plaintext)

    # Converts the passkey into a hex string
    hexedKey = getHexedKey(key=passKey)

    # Runs a process on the hexed key to generate 16 sub-keys
    permutedSubKeys = generateSubKeys(key=hexedKey)

    cipherText = ""

    # Iterates over each block of 16 hex chars in the hexed plaintext
    for hexBlock in hexedPlainText:
        # Converts each hex block to binary
        binaryPlainText = getBinaryMessage(message=hexBlock)

        # Permutates the binary plaintext with the IP-block
        permutedBinaryPlainText = permutateMessage(message=binaryPlainText)

        # Splits the permuted binary plaintext into two halves
        leftHalf, rightHalf = splitPermutedMessage(message=permutedBinaryPlainText)

        # Runs the encoding process to get the ciphertext of each hex block
        cipherPart = encodeIteration(leftHalf, rightHalf, permutedSubKeys)

        # Concatenatew the ciphertext parts of each hex block to form the main ciphertext
        cipherText += cipherPart

    return cipherText


def decrypt(passKey, dataformat, ciphertext=None, filename=None, isTripleDES=None):
    """Takes in a ciphertext and passkey and returns the plaintext using DES"""

    # Converts the passkey into a hex string
    hexedKey = getHexedKey(key=passKey)

    # Runs a process on the hexed key to generate 16 sub-keys
    permutedSubKeys = generateSubKeys(key=hexedKey)

    # Breaks ciphertext into blocks of 16
    cipherText = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]

    plainText = ""

    # Iterates over each block of 16 hex chars in the hexed ciphertext
    for hexBlock in cipherText:
        # Converts each hex block to binary
        binaryCipherText = getBinaryMessage(message=hexBlock)

        # Permutates the binary string of the message with the IP-block
        permutedBinaryCipherText = permutateMessage(message=binaryCipherText)

        # Splits the permuted binary message into two halves
        leftHalfMessage, rightHalfMessage = splitPermutedMessage(message=permutedBinaryCipherText)

        # Runs the decoding process to get the decrypted part of each hex block
        decryptedPart = decodeIteration(leftHalfMessage, rightHalfMessage, permutedSubKeys)

        """
        Creates a list comprehension of the decrypted parts broken up into twos.
        This represents each hex value.
        """
        hexedDecryptedPart = [decryptedPart[i:i+2] for i in range(0, len(decryptedPart), 2)]

        """
        In Triple DES, don't convert the decrypted part to ASCII,
        to allow the hexed version to be used again for the rest of the
        Triple DES process.
        """
        if isTripleDES:
            decryptedPart = "".join(hexedDecryptedPart)
        else:
            # Converts each hex part to ASCII
            decryptedPart = [chr(int(h, 16)) for h in hexedDecryptedPart]

            # Joins the characters in the list of ASCII characters
            decryptedPart = "".join(decryptedPart)

        # Concatenates the decrypted parts of each hex block to form the main plaintext
        plainText += decryptedPart

    """
    If the decyption method is Triple DES, the plaintext must be split up into
    blocks of 16 to be used later in the Triple DES process.
    """
    if isTripleDES:
        return [plainText[i:i+16] for i in range(0, len(plainText), 16)]
    else:
        return plainText


def encrypt_tripleDES(plaintext, passKey, dataformat):
    """Takes in a plaintext and passkey and returns the ciphertext using Triple DES"""

    key1 = passKey[0]
    key2 = passKey[1]

    """
    The first encryption doesn't need to be passed the argument isTripleDES,
    as the plaintext is from the user and not a hex string
    from the decryption process.
    """
    encryptedData1 = encrypt(plaintext=plaintext, passKey=key1, dataformat=dataformat)
    encryptedData2 = decrypt(ciphertext=encryptedData1, passKey=key2, dataformat=dataformat, isTripleDES=True)
    encryptedData = encrypt(plaintext=encryptedData2, passKey=key1, dataformat=dataformat, isTripleDES=True)

    return encryptedData


def decrypt_tripleDES(ciphertext, passKey, dataformat):
    """Takes in a ciphertext and passkey and returns the plaintext using Triple DES"""

    key1 = passKey[0]
    key2 = passKey[1]

    decryptedData1 = decrypt(ciphertext=ciphertext, passKey=key1, dataformat=dataformat, isTripleDES=True)
    decryptedData2 = encrypt(plaintext=decryptedData1, passKey=key2, dataformat=dataformat, isTripleDES=True)

    """
    For the last decryption, there is no need to pass the optional argument of isTripleDES,
    as it is required the DES algorithm does convert the plaintext to ASCII characters
    """
    decryptedData = decrypt(ciphertext=decryptedData2, passKey=key1, dataformat=dataformat)

    return decryptedData


def encryptImage(filename, filepath, passKey, isTripleDES=None):
    """Encryption for images"""

    # Checks if the encryption is done through Triple DES
    if isTripleDES:
        # In Triple DES, there will be two shift keys
        shift1 = getShiftValuesFromPassKey(passKey=passKey[0])
        shift2 = getShiftValuesFromPassKey(passKey=passKey[1])

        # Checks if the extension of the image is .jpg
        extension = filename.split(".")[1]
        if extension == "jpg":
            isJPG = True
        else:
            isJPG = False

        # Special encrypt-decrypt-encrypt process for Triple DES:
        encryptionPart1 = imageCrypt.encrypt(filename=filename, filepath=filepath, shifts=shift1, cipherUsed="TripleDES", isFirst=True)

        encryptionPart2, numberOfPixelValues = imageCrypt.decrypt(filename=encryptionPart1, filepath=filepath, shifts=shift2, cipherUsed="TripleDES")

        if isJPG:
            encryptedImageFilename = imageCrypt.encrypt(filename=encryptionPart2, filepath=filepath, shifts=shift1, cipherUsed="TripleDES", isJPG=True, isFinal=True)
        else:
            encryptedImageFilename = imageCrypt.encrypt(filename=encryptionPart2, filepath=filepath, shifts=shift1, cipherUsed="TripleDES", isFinal=True)

        # Deletes cetain images saved from the whole encryption process as they are no longer needed
        os.remove(encryptionPart1)
        os.remove(encryptionPart2)
    else:
        shifts = getShiftValuesFromPassKey(passKey=passKey)

        encryptedImageFilename = imageCrypt.encrypt(filename=filename, filepath=filepath, shifts=shifts, cipherUsed="DES")

    return encryptedImageFilename


def decryptImage(filename, filepath, passKey, isTripleDES=None):
    """Decryption for images"""

    # Checks if the decryption is done through Triple DES
    if isTripleDES:
        # In Triple DES, there will be two shift keys
        shift1 = getShiftValuesFromPassKey(passKey=passKey[0])
        shift2 = getShiftValuesFromPassKey(passKey=passKey[1])

        # Special decrypt-encrypt-decrypt process for Triple DES
        decryptionPart1, numberOfPixelValues = imageCrypt.decrypt(filename=filename, filepath=filepath, shifts=shift1, cipherUsed="TripleDES", isFirst=True)

        if numberOfPixelValues == 3:
            decryptionPart2 = imageCrypt.encrypt(filename=decryptionPart1, filepath=filepath, shifts=shift2, cipherUsed="TripleDES", isJPG=True)
        else:
            decryptionPart2 = imageCrypt.encrypt(filename=decryptionPart1, filepath=filepath, shifts=shift2, cipherUsed="TripleDES")

        decryptedImageFilename, numberOfPixelValues = imageCrypt.decrypt(filename=decryptionPart2, filepath=filepath, shifts=shift1, cipherUsed="TripleDES", isFinal=True)

        # Deletes cetain images saved from the whole decryption process as they are no longer needed
        os.remove(decryptionPart1)
        os.remove(decryptionPart2)
    else:
        shifts = getShiftValuesFromPassKey(passKey=passKey)

        decryptedImageFilename, numberOfPixelValues = imageCrypt.decrypt(filename=filename, filepath=filepath, shifts=shifts, cipherUsed="DES")

    return decryptedImageFilename
