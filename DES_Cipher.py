# Vigenere Cipher Algorithm

import imageCrypt
import encryptionBlocks
import os

def getShiftsFromPassKey(passKey):
    # Convert the passkey to a hex string
    hexedKey = getHexedKey(key=passKey)

    # Run a process on the hexed key to generate 16 sub keys
    permutedSubKeys = generateKeys(key=hexedKey)

    # Convert the binary value of each subkey to denary
    denaryOfSubKeys = [int(i,2) for i in permutedSubKeys]
    # Convert the denary values to string
    # Then, slice the values to get the first 4 digits and convert back to ints
    truncatedDenaryValues = [int(str(i)[0:4]) for i in denaryOfSubKeys]

    return truncatedDenaryValues
# Return the plaintext in hex form and separate it into blocks of 16 in a list
def getHexedPlainText(plainText):
    # Create a list of each character from the plaintext
    plainText = list(plainText)

    # Convert each character in the plaintext to hex from the list
    hexedCharsList = [hex(ord(char))[2:] for char in plainText]

    # Convert list to string
    hexedPlainText = "".join(hexedCharsList)

    # Append the hexed plaintext with 0s to ensure it is
    # a multiple of 16 hexadecimal characters
    length = len(hexedPlainText)
    # Only add the 0s if the length of the hexed plaintext is
    # not a multiple of 16
    if length % 16 != 0:
        # The ammount of padding is determined by finding
        # the next multiple of 16 closest to the length ((length // 16) + 1)
        # By subtracting this multiple from the actual length, gives the number
        # of 0s needed to make the length a multiple of 16
        padding = ((((length // 16) + 1) * 16) - length)
        # Add the appropriate number of 0s onto the end of the hexed plaintext
        hexedPlainText += ("0"*padding)

    # Separate the hexed message into blocks of 16 into a list
    hexedPlainText = [hexedPlainText[i:i+16] for i in range(0, len(hexedPlainText), 16)]

    return hexedPlainText

# Convert the key into a hex form of exact size 16 hex characters
def getHexedKey(key):
    # Create a list of each character from the key
    key = list(key)

    # Convert each character to hex in the list
    hexedCharsList = [hex(ord(char))[2:] for char in key]

    # Convert list to string
    hexedKey = "".join(hexedCharsList)

    # Padd hexed key with 0s to make it a multiple of 16 hexadecimal characters
    length = len(hexedKey)
    padding = ((((length // 16) + 1) * 16) - length)
    hexedKey += ("0"*padding)

    # Truncate the hexed key to only 16 hex digits long
    hexedKey = hexedKey[0:16]

    return hexedKey

# Run a process on the hexed key to generate 16 individual sub keys
def generateKeys(key):
    # Convert the hexed key to binary
    binaryKey = getBinaryKey(key=key)

    # Permutate the binary key with PC1
    permutedBinaryKey = permutateBinaryKey(key=binaryKey)

    # Split the permuted binary key into two halves
    leftHalf, rightHalf = splitPermutedKey(key=permutedBinaryKey)

    # Get the 16 sub keys as a list
    subKeys = getSubKey(c=leftHalf, d=rightHalf)

    # Permutate the 16 sub keys with PC2
    permutedSubKeys = permutateSubKeys(keys=subKeys)

    return permutedSubKeys

# Return the binary form of the key
def getBinaryKey(key):
    # Convert the key to denary from hex then to binary
    newKey = bin(int(key, 16))[2:]

    # Keep the binary key in 64 bit form by adding 0s to the front
    length = len(newKey)
    newKey = newKey.zfill(64 - (length % 64) + length)

    return newKey

def permutateBinaryKey(key):
    # Create a list of each character from the binary key
    key = list(key)

    # Initialise the permuted keys to have a size of 56 bits
    permuted = [0 for x in range(56)]

    # Fetch the PC1 Block from the encryption blocks module
    PC_1 = encryptionBlocks.getPC_1()

    # Enumerate over the PC1 Block and set the value at the current position in the
    # permuted list to the bit in the position from the PC1 of the key
    for i,pos in enumerate(PC_1,1):
        permuted[i-1] = key[pos-1]

    # Join the list into a binary string
    permuted = "".join(permuted)

    return permuted

def splitPermutedKey(key):
    # Get the left and right halves of the permuted key
    # The key is guaranteed to be 56 bits in length
    # therefore it is alright to hardcode the index positions when splitting
    leftHalf = key[0:28]
    rightHalf = key[28:56]

    return leftHalf, rightHalf

def getSubKey(c,d):
    # The list of values to which the two halves of the key are shifted by
    shifts = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

    # A 2d array storing the pairs of keys which have been shifted
    subKeys = []

    # Initialise the previous sub keys to the separate halves of the key c, d
    cPrev = c
    dPrev = d

    # Iterate over the given shift values
    for s in shifts:
        # Shift the previous sub keys by the shift value
        cNext = shiftItems(key=cPrev,shift=s)
        dNext = shiftItems(key=dPrev,shift=s)

        # Change the previous sub key
        cPrev = cNext
        dPrev = dNext

        # Store the new sub keys
        subKeys.append([cNext,dNext])

    return subKeys

def shiftItems(key,shift):
    # Create a list of each character from the binary key
    key = list(key)

    # Shift the key by the shift number
    shiftedKey = key[shift:] + key[:shift]

    # Join the key into a string
    subKey = "".join(shiftedKey)

    return subKey

def permutateSubKeys(keys):
    # Join the left and right halves of the sub keys together and store them as
    # one whole key
    keys = ["".join(k) for k in keys]

    # Initialise the permuted sub keys to have a size of 48 bits
    permutedSubKey = [0 for x in range(48)]
    # This will store the 16 permuted sub keys at the end
    setOfSubKeys = []

    # Fetch the PC2 Block from the encryption blocks module
    PC_2 = encryptionBlocks.getPC_2()

    # Iterate over each key from the 16 subkeys
    for key in keys:
        # Create a list of each character from the key
        key = list(key)
        # Enumerate over the PC2 Block and set the value at the current position in the
        # permuted list to the bit in the position from the PC2 of the key
        for i,pos in enumerate(PC_2,1):
            permutedSubKey[i-1] = key[pos-1]

        # Join the list of permuted sub keys to a string of binary digits
        # Since the list contains integers of 1 and 0; the items need to be
        # mapped to a string before joining
        binaryString = "".join(map(str,permutedSubKey))
        setOfSubKeys.append(binaryString)

    return setOfSubKeys

# Return the binary form of the message which is a hex string
# The function is called for both plaintexts and ciphertexts
def getBinaryMessage(message):
    # Convert the message to denary from hex then to binary
    binary_string = bin(int(message, 16))[2:]

    # Keep the binary message in 64 bit form by adding 0s to the front
    length = len(message)
    binary_string = binary_string.zfill(64 - (length % 64) + length)

    return binary_string

def permutateMessage(message):
    # Create a list of each character from the binary message
    message = list(message)

    # Initialise the permuted message to have a size of 64 bits
    permuted = [0 for x in range(64)]

    # Fetch the IP Block from the encryption blocks module
    IP = encryptionBlocks.getIP()

    # Enumerate over the IP Block and set the value at the current position in the
    # permuted list to the bit in the position from the IP of the message
    for i,pos in enumerate(IP,1):
        permuted[i-1] = message[pos-1]

    # Join the list into a binary string
    permuted = "".join(permuted)

    return permuted

def splitPermutedMessage(message):
    # Get the left and right halves of the binary message
    # The binary message block is guaranteed to be 64 bits in length
    # therefore it is alright to hardcode the index positions when splitting
    leftHalf = message[0:32]
    rightHalf = message[32:64]

    return leftHalf, rightHalf

def encodeIteration(l,r,subKeys):
    # Initialise the previous halves to the separate halves of the plaintext
    lPrev = l
    rPrev = r

    # Iterate over each subkey in the list of permuted subkeys
    for subKey in subKeys:
        # Convert the previous left half to a denary value
        # This is essential for later during the XOR operation which requires
        # a denary value
        leftPrev = int(lPrev,2)

        # Convert the function F return to a denary value
        F = int(functionF(rightHalf=rPrev,key=subKey),2)

        # Set the next right half to the binary value of the calculation:
        # previous left half XOR F (function)
        rNext = bin(leftPrev ^ F)
        # Format the calculated binary value to a 32 bit string
        rNext = rNext[2:].zfill(32)

        # Set the next left half to the previous right half
        lNext = rPrev

        # Change the previous l, r halves to the new ones
        lPrev = lNext
        rPrev = rNext

    # Create a binary string from the two new left and right halves
    # This binary string is reversed by placing the right half before the left half
    reversedBinary = rNext + lNext

    # Permutate the binary string with IP-1
    permuted = permutate_IP_1(reversedBinary)
    # Convert the binary string to a denary value which is turned to a hex value
    # .zfill(16) makes sure the block of cipher text is 16 hex characters long
    cipherText = hex(int(permuted,2))[2:].zfill(16)

    return cipherText

def decodeIteration(l,r,subKeys):
    # Initialise the previous halves to the separate halves of the plaintext
    lPrev = l
    rPrev = r

    # For decryption, iterate over each subkey in the list of permuted subkeys
    # in reverse order
    for subKey in reversed(subKeys):
        # Convert the previous left half to a denary value
        leftPrev = int(lPrev,2)

        # Convert the function F return to a denary value
        f = int(functionF(rPrev,subKey),2)

        # Set the next right half to the binary value of the calculation:
        # previous left half XOR F (function)
        rNext = bin(leftPrev ^ f)

        # Format the calculated binary value to a 48 bit string
        rNext = rNext[2:].zfill(32)

        # Set the next left half to the previous right half
        lNext = rPrev

        # Change the previous l, r halves to the new ones
        lPrev = lNext
        rPrev = rNext

    # Create a binary string from the two new left and right halves
    # This binary string is reversed by placing the right half before the left half
    reversedBinary = rNext + lNext

    # Permutate the binary string with IP-1
    permuted = permutate_IP_1(reversedBinary)
    # Convert the binary string to a denary value which is turned to a hex value
    cipherText = hex(int(permuted,2))[2:].zfill(16)

    return cipherText

# This function carries out the XOR addition of the right half with the key
# It then takes a group of 6 bits and turns them into a group of 4 bits
def functionF(rightHalf,key):
    # Convert the key to denary
    key = int(key,2)
    # Convert the function E return to denary
    E = int(functionE(rightHalf=rightHalf),2)

    # Calculate: key XOR E function
    xorAddition = bin(key ^ E)
    # Format the calculated binary value to a 48 bit string
    xorAddition = xorAddition[2:].zfill(48)

    # Separate the binary string into 8 groups of 6 bits
    blocks = [xorAddition[i:i+6] for i in range(0, len(xorAddition), 6)]

    S_String = ""
    # Enumerate over the binary blocks
    for i,block in enumerate(blocks):
        # Get a 4-bit sub block from function S
        subBlock = functionS(block=block,blockIndex=i)
        S_String += subBlock

    # Permutate the S_String with P
    permutatedS_String = permutateS_String(string=S_String)

    return permutatedS_String

# This function will expand the right half from 32bits to 48bits
def functionE(rightHalf):
    # Create a list of each bit from the right half
    rightHalf = list(rightHalf)

    # Fetch the E Block from the encryption blocks module
    E_Table = encryptionBlocks.getE_Table()

    # This will store the expanded right side binary string
    # The binary will be expanded according to the eBitSelectionTable from 32 to 48 bits
    expandedRight = ""

    # Iterate over the E Block to append the bit at the current position in the
    # right half to the expanded string
    for pos in E_Table:
        expandedRight += rightHalf[pos-1]

    return expandedRight

# This function takes in a 6bit binary block and returns a 4bit block using
# the S Block
def functionS(block,blockIndex):
    # Fetch the S Box for the specific block from the encryption blocks module
    SBOX = encryptionBlocks.getSBox(blockIndex)

    # Get the first and last bit from the 6bit block
    first,last = block[0], block[5]
    # Combine the first and last bits of the block to form a 2-bit binary value
    i = first + last
    # The middle part of the binary block is a 4-bit binary value
    j = block[1:5]

    # Convert the binary sections to denary which will represent the index positions
    iPos = int(i,2)
    jPos = int(j,2)

    # Get the number at the position i,j in the SBOX
    output = SBOX[iPos][jPos]

    # Convert the output to a 4-bit binary value
    binaryOutput = bin(output)[2:].zfill(4)

    return binaryOutput

def permutateS_String(string):
    # Fetch the P Block from the encryption blocks module
    P_Table = encryptionBlocks.getP_Table()

    permuted = ""

    # Iterate over the P Block to append the bit at the current position in the
    # string to the permuted string
    for pos in P_Table:
        permuted += string[pos-1]

    return permuted

def permutate_IP_1(binary):
    # Fetch the IP-1 Block from the encryption blocks module
    IP_1 = encryptionBlocks.getIP_1()

    permuted = ""

    # Iterate over the IP-1 Block to append the bit at the current position in the
    # binary gstring to the permuted stringg
    for pos in IP_1:
        permuted += binary[pos-1]

    return permuted

# Organise the encryption and decryption process
def encrypt(passKey,dataformat,plaintext=None,filename=None,isTripleDES=None):
    if isTripleDES:
        hexedPlainText = plaintext
        #hexedPlainText = [hexedPlainText[i:i+16] for i in range(0, len(hexedPlainText), 16)]
    else:
        # Convert the plaintext to a hex string
        hexedPlainText = getHexedPlainText(plainText=plaintext)

    # Convert the passkey to a hex string
    hexedKey = getHexedKey(key=passKey)
    # Run a process on the hexed key to generate 16 sub keys
    permutedSubKeys = generateKeys(key=hexedKey)

    cipherText = ""

    # Iterate over each block of 16 hex chars in the hexed plaintext
    for hexBlock in hexedPlainText:
        # Convert each hex block to binary
        binaryPlainText = getBinaryMessage(message=hexBlock)

        # Permutate the binary plaintext with IP
        permutedBinaryPlainText = permutateMessage(message=binaryPlainText)

        # Split the permuted binary plaintext into two halves
        leftHalf, rightHalf = splitPermutedMessage(message=permutedBinaryPlainText)

        # Run the encoding process to get the ciphertext of each hex block
        cipherPart = encodeIteration(leftHalf,rightHalf,permutedSubKeys)

        # Concatenate the ciphertext parts of each hex block to form the main ciphertext
        cipherText += cipherPart

    return cipherText

def decrypt(passKey,dataformat,ciphertext=None,filename=None,isTripleDES=None):
    # Convert the passkey to a hex string
    hexedKey = getHexedKey(key=passKey)

    # Run a process on the hexed key to generate 16 sub keys
    permutedSubKeys = generateKeys(key=hexedKey)

    # Break ciphertext into blocks of 16
    cipherText = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]

    plainText = ""

    # Iterate over each block of 16 hex chars in the hexed ciphertext
    for hexBlock in cipherText:
        # Convert each hex string to binary
        binaryCipherText = getBinaryMessage(message=hexBlock)

        # Permutate the binary string of the message with IP
        permutedBinaryCipherText = permutateMessage(message=binaryCipherText)

        # Split the permuted binary message into two halves
        leftHalfMessage, rightHalfMessage = splitPermutedMessage(message=permutedBinaryCipherText)

        # Run the decoding process to get the decrypted part of each hex block
        decryptedPart = decodeIteration(leftHalfMessage,rightHalfMessage,permutedSubKeys)

        # Create a list comprehension from the decrypted parts by breaking it up in twos.
        # This represents each hex part
        hexedDecryptedPart = [decryptedPart[i:i+2] for i in range(0, len(decryptedPart), 2)]

        # In Triple DES, don't convert the decrypted part to ASCII,
        #  as to allow the hexed version to be used again for the rest of the
        # Triple DES process
        if isTripleDES:
            decryptedPart = "".join(hexedDecryptedPart)
        else:
            # Convert each hex part to ASCII
            decryptedPart = [chr(int(h,16)) for h in hexedDecryptedPart]

            # Join the characters in the list of ASCII characters
            decryptedPart = "".join(decryptedPart)

        # Concatenate the decrypted parts of each hex block to form the main plaintext
        plainText += decryptedPart

    # If the decyption method is Triple DES, the plaintext must be split up into
    # blocks of 16 to be used later in the Triple DES process
    if isTripleDES:
        return [plainText[i:i+16] for i in range(0, len(plainText), 16)]
    else:
        return plainText

def encrypt_tripleDES(plaintext,passKey,dataformat):
    key1 = passKey[0]
    key2 = passKey[1]

    # The first encryption doesn't need to be passed the argument isTripleDES,
    # as the plaintext is the plaintext entered by the user and
    # not a hex string from the decryption process
    encryptedData1 = encrypt(plaintext=plaintext,passKey=key1,dataformat=dataformat)
    encryptedData2 = decrypt(ciphertext=encryptedData1,passKey=key2,dataformat=dataformat,isTripleDES=True)
    encryptedData = encrypt(plaintext=encryptedData2,passKey=key1,dataformat=dataformat,isTripleDES=True)

    return encryptedData

def decrypt_tripleDES(plaintext,passKey,dataformat):
    key1 = passKey[0]
    key2 = passKey[1]

    decryptedData1 = decrypt(ciphertext=ciphertext,passKey=key1,dataformat=dataformat,isTripleDES=True)
    decryptedData2 = encrypt(plaintext=decryptedData1,passKey=key2,dataformat=dataformat,isTripleDES=True)
    # For the last decryption, there is no need to pass the optional argument of isTripleDES,
    # as it is required the DES algorithm does convert the plaintext to ASCII characters
    decryptedData = decrypt(ciphertext=decryptedData2,passKey=key1,dataformat=dataformat)

    return decryptedData

# Encryption for images
def encryptImage(filename,passKey,isTripleDES=None):
    if isTripleDES:
        shift1 = getShiftsFromPassKey(passKey=passKey[0])
        shift2 = getShiftsFromPassKey(passKey=passKey[1])

        extension = filename.split(".")[1]
        if extension == "jpg":
            isJPG = True
        else:
            isJPG = False

        encryptionPart1 = imageCrypt.encrypt(filename=filename,shifts=shift1,cipherUsed="tripleDES")
        encryptionPart2 = imageCrypt.decrypt(filename=encryptionPart1,shifts=shift2,cipherUsed="tripleDES")
        if isJPG:
            encryptedImageFilename = imageCrypt.encrypt(filename=encryptionPart2,shifts=shift1,cipherUsed="tripleDES",isTripleDES=True)
        else:
            encryptedImageFilename = imageCrypt.encrypt(filename=encryptionPart2,shifts=shift1,cipherUsed="tripleDES")

        # Delete the image saved from decryption as it is no longer needed
        #os.remove(encryptionPart2)
    else:
        shifts = getShiftsFromPassKey(passKey=passKey)
        encryptedImageFilename = imageCrypt.encrypt(filename=filename,shifts=shifts,cipherUsed="DES")
    return encryptedImageFilename

def decryptImage(filename,passKey,isTripleDES=None):
    if isTripleDES:
        shift1 = getShiftsFromPassKey(passKey=passKey[0])
        shift2 = getShiftsFromPassKey(passKey=passKey[1])

        extension = filename.split(".")[1]
        if extension == "jpg":
            isJPG = True
        else:
            isJPG = False

        decryptionPart1 = imageCrypt.decrypt(filename=filename,shifts=shift1,cipherUsed="tripleDES")
        if isJPG:
            decryptionPart2 = imageCrypt.encrypt(filename=decryptionPart1,shifts=shift2,cipherUsed="tripleDES",isTripleDES=True)
        else:
            decryptionPart2 = imageCrypt.encrypt(filename=decryptionPart1,shifts=shift2,cipherUsed="tripleDES")
        decryptedImageFilename = imageCrypt.decrypt(filename=decryptionPart2,shifts=shift1,cipherUsed="tripleDES")

        # Delete the image saved from encryption as it is no longer needed
        #os.remove(decryptionPart2)
    else:
        shifts = getShiftsFromPassKey(passKey=passKey)
        decryptedImageFilename = imageCrypt.decrypt(filename=filename,shifts=shifts,cipherUsed="DES")

    return decryptedImageFilename
