# Image encryption program

from PIL import Image
import itertools


def getPixelData(width, height, shifts):
    """Creates a generator function"""

    """
    Iterate through the pixel values of width and height combined from itertools.product()
    then iterate through the shifts in a cycle using itertools.cycle()
    """
    for pixelValue, key in zip(itertools.product(width, height), itertools.cycle(shifts)):
        # Returns a tuple: (width, height, key)
        yield (*pixelValue, key)


def encryptPixels(width, height, imageFormat, shifts, originalImagePixelData, copyImagePixelData, isJPG=None):
    """Encrypts the individual pixels with a shift value"""
    for pixelTuple in getPixelData(width=width, height=height, shifts=shifts):
        # Sets the pixel's X and Y values; and the key value, from the tuple given by the generator function
        pixelX, pixelY, shift = pixelTuple[0], pixelTuple[1], pixelTuple[2]

        # Gets each pixel value from the original image
        pixel = originalImagePixelData[pixelX, pixelY]

        # Sets the R, G, B values of each pixel
        R = pixel[0]
        G = pixel[1]
        B = pixel[2]

        # Shifts each colour of the pixel by the shift value to get the new pixel values
        colourRed = (R + shift) % 256
        colourGreen = (G + shift) % 256
        colourBlue = (B + shift) % 256

        # Checks if the image type is PNG and if Triple DES encryption is not used
        if imageFormat == "png" and isJPG is not True:
            # PNG images have an alpha channel
            A = pixel[3]
            alpha = (A + shift) % 256

            # Stores the changes onto the copied image’s pixel map with the alpha channel value
            copyImagePixelData[pixelX, pixelY] = (colourRed, colourGreen, colourBlue, alpha)
        else:
            # Stores the changes onto the copied image’s pixel map
            copyImagePixelData[pixelX, pixelY] = (colourRed, colourGreen, colourBlue)


def decryptPixels(width, height, shifts, encryptedImagePixelData, copyImagePixelData):
    """Encrypts the individual pixels with a shift value"""
    # Gets the number of pixel values. JPGs have 3 and PNGs have 4.
    numberOfPixelValues = len(encryptedImagePixelData[0, 0])

    for pixelTuple in getPixelData(width=width, height=height, shifts=shifts):
        """
        Determines the number of values in each pixel of the image.
        This will help to distinguish between PNG and JPG images
        as the encrypted image will always be saved as a PNG.
        PNG images have an alpha channel, however when converted from JPG to PNG,
        the alpha channel doesn't exist, so the pixels only have the RGB format.
        """

        # Sets the pixel's X and Y values; and the key value, from the tuple given by the generator function
        pixelX, pixelY, shift = pixelTuple[0], pixelTuple[1], pixelTuple[2]

        # Gets each pixel value from original image
        pixel = encryptedImagePixelData[pixelX, pixelY]

        # Sets the R,G,B values of each pixel
        R = pixel[0]
        G = pixel[1]
        B = pixel[2]

        # Shifts each colour of the pixel by the shift to get the new pixel values
        colourRed = (R - shift) % 256
        colourGreen = (G - shift) % 256
        colourBlue = (B - shift) % 256

        """
        Checks if the number of pixel values is 4, as that means the original
        image was a PNG and we need to decrypt its alpha channel as well.
        """
        if numberOfPixelValues == 4:
            # PNG images have an alpha channel
            A = pixel[3]
            alpha = (A - shift) % 256

            # Stores the changes onto the copied image data with the alpha channel value
            copyImagePixelData[pixelX, pixelY] = (colourRed, colourGreen, colourBlue, alpha)
        else:
            # Stores the changes onto the copied image data
            copyImagePixelData[pixelX, pixelY] = (colourRed, colourGreen, colourBlue)

    return numberOfPixelValues


def loadEncryption(filename, filepath, originalImage, imageFormat, shifts, cipherUsed, isJPG=None, isFirst=None, isFinal=None):
    """Gets the image pixel data, manipulates the image, then saves it"""

    """
    Gets a pixel access object for the original image
    The pixel access object will behave like a 2D array
    which will allow the program to read and modify individual pixels.
    """
    originalImagePixelData = originalImage.load()

    # Makes a copy of the input image and loads the copied image's pixel map
    copyImage = Image.new(originalImage.mode, originalImage.size)
    copyImagePixelData = copyImage.load()

    # Gets the width and height of the copied image
    width = range(copyImage.size[0])
    height = range(copyImage.size[1])

    # Encrypts the image pixels
    encryptPixels(width=width, height=height, imageFormat=imageFormat, shifts=shifts, originalImagePixelData=originalImagePixelData, copyImagePixelData=copyImagePixelData, isJPG=isJPG)

    # Closes the original image
    originalImage.close()

    # Rotates and flips the image to make the encrypted image more different than the original
    copyImage = copyImage.rotate(180)
    copyImage = copyImage.transpose(Image.FLIP_LEFT_RIGHT)

    # Controls the way Triple DES encryption filenames are generated
    if cipherUsed == "TripleDES":
        """
        All the filenames are saved as .png, as JPG files perform
        lossy compression. This alters the encrypted pixels and is
        not beneficial when decrypting.
        """
        if isFirst is True:
            newFilename = "{}/{}_{}ENC2.png".format(filepath, filename[:-4], cipherUsed)
        elif isFinal is True:
            newFilename = "{}".format(filename.replace("DEC2", "ENC"))
        else:
            newFilename = "{}".format(filename.replace("DEC3", "ENC3"))
    else:
        newFilename = "{}/{}_{}ENC.png".format(filepath, filename[:-4], cipherUsed)

    # Saves the encrypted image and then close it
    copyImage.save(newFilename)
    copyImage.close()

    return newFilename


def loadDecryption(filename, filepath, shifts, cipherUsed, isFirst=None, isFinal=None):
    """Gets the image pixel data, manipulates the image, then saves it"""

    # The filepath is only appended when the first TripleDES decryption doesn't occur
    if cipherUsed == "TripleDES" and isFirst is not True:
        inputImage = Image.open(filename)
    else:
        full_filename = filepath + "/" + filename
        inputImage = Image.open(full_filename)

    # Rotates and flips the image back to its original orientation
    inputImage = inputImage.transpose(Image.FLIP_LEFT_RIGHT)
    inputImage = inputImage.rotate(180)

    """
    Gets a pixel access object for the input image
    The pixel access object will behave like a 2D array
    which will allow the program to read and modify individual pixels.
    """
    encryptedImagePixelData = inputImage.load()

    # Makes a copy of the input image and loads the copied image's pixel map
    copyImage = Image.new(inputImage.mode, inputImage.size)
    copyPixelMap = copyImage.load()

    # Gets the width and height of the copied image
    width = range(copyImage.size[0])
    height = range(copyImage.size[1])

    # Decrypts the image pixels
    numberOfPixelValues = decryptPixels(width=width, height=height, shifts=shifts, encryptedImagePixelData=encryptedImagePixelData, copyImagePixelData=copyPixelMap)

    # Closes the input image
    inputImage.close()

    # Controls the way Triple DES decryption filenames are generated
    if cipherUsed == "TripleDES":
        """
        All the filenames are just replacements of ENC to DEC. In some cases it
        is necessary to add a number, such as DEC3, to prevent overriding existing
        files.
        """
        if isFirst is True:
            newFilename = "{}/{}".format(filepath, filename.replace("ENC", "DEC3"))
        elif isFinal is True:
            newFilename = "{}".format(filename.replace("ENC3", "DEC"))
        else:
            newFilename = "{}".format(filename.replace("ENC2", "DEC2"))
    else:
        newFilename = "{}/{}".format(filepath, filename.replace("ENC", "DEC"))

    # Saves the encrypted image
    copyImage.save(newFilename)
    copyImage.close()

    return newFilename, numberOfPixelValues


def encryptionImageHandler(filename, filepath, shifts, cipherUsed, isJPG=None, isFirst=None, isFinal=None):
    """Checks if the original image needs to be converted to RGBA format"""

    # The filepath is only appended when the first TripleDES encryption doesn't occur
    if cipherUsed == "TripleDES" and isFirst is not True:
        originalImage = Image.open(filename)
    else:
        full_filename = filepath + "/" + filename
        originalImage = Image.open(full_filename)

    # Gets the extension of the image
    extension = filename.split(".")[-1]

    # Checks if the image type is PNG and if Triple DES encryption is not used
    if extension == "png" and isJPG is not True:
        # PNG images need to be converted to RGBA format
        originalImage = originalImage.convert("RGBA")

    encryptedData = loadEncryption(filename=filename, filepath=filepath, originalImage=originalImage, imageFormat=extension, shifts=shifts, cipherUsed=cipherUsed, isJPG=isJPG, isFirst=isFirst, isFinal=isFinal)

    return encryptedData


def encrypt(filename, filepath, shifts, cipherUsed, isJPG=None, isFirst=None, isFinal=None):
    encryptedData = encryptionImageHandler(filename=filename, filepath=filepath, shifts=shifts, cipherUsed=cipherUsed, isJPG=isJPG, isFirst=isFirst, isFinal=isFinal)

    return encryptedData


def decrypt(filename, filepath, shifts, cipherUsed, isFirst=None, isFinal=None):
    decryptedData, numberOfPixelValues = loadDecryption(filename=filename, filepath=filepath, shifts=shifts, cipherUsed=cipherUsed, isFirst=isFirst, isFinal=isFinal)

    return decryptedData, numberOfPixelValues
