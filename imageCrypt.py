# Image encryption module

from PIL import Image
import itertools


def getEncryptedPixel(input_pixel, shift):
    """Encrypts the individual pixels with a shift value"""
    # Gets the number of pixel values. JPGs have 3 and PNGs have 4.
    numberOfPixelValues = len(input_pixel)

    pixel = input_pixel

    # Sets the R, G, B values of each pixel
    R = pixel[0]
    G = pixel[1]
    B = pixel[2]

    # Shifts each colour of the pixel by the shift value to get the new pixel values
    colourRed = (R + shift) % 256
    colourGreen = (G + shift) % 256
    colourBlue = (B + shift) % 256

    # Checks if the image type is PNG and if Triple DES encryption is not used
    if numberOfPixelValues == 4:
        # PNG images have an alpha channel
        A = pixel[3]
        alpha = (A + shift) % 256

        return (colourRed, colourGreen, colourBlue, alpha)
    else:
        return (colourRed, colourGreen, colourBlue)


def getDecryptedPixel(input_pixel, shift):
    """Encrypts the individual pixels with a shift value"""
    # Gets the number of pixel values. JPGs have 3 and PNGs have 4.
    numberOfPixelValues = len(input_pixel)

    pixel = input_pixel

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

        return (colourRed, colourGreen, colourBlue, alpha)
    else:
        return (colourRed, colourGreen, colourBlue)


def getPixelData(width, height, shifts):
    """Creates a generator function"""

    """
    Iterate through the pixel values of the width and height combined from itertools.product()
    then iterate through the shifts in a cycle using itertools.cycle()
    """
    for pixelValue, key in zip(itertools.product(width, height), itertools.cycle(shifts)):
        # Returns a tuple: (width, height, key)
        yield (*pixelValue, key)

def encryptPixels(width, height, shifts, originalImagePixelData, copyImagePixelData, isTripleDES=None):
    # In Triple DES, the shifts come in a pair
    if isTripleDES is True:
        shifts_list = shifts[0]
        second_shifts = shifts[1]
    else:
        shifts_list = shifts

    for pixelTuple in getPixelData(width=width, height=height, shifts=shifts_list):
        # Sets the pixel's X and Y values; and the key value, from the tuple given by the generator function
        pixelX, pixelY, shift = pixelTuple[0], pixelTuple[1], pixelTuple[2]

        # Gets each pixel value from the original image
        pixel = originalImagePixelData[pixelX, pixelY]

        if isTripleDES is True:
            E_pixel_temp = getEncryptedPixel(input_pixel=pixel, shift=shift)

            shift2 = second_shifts[shifts_list.index(shift)]
            D_pixel = getDecryptedPixel(input_pixel=E_pixel_temp, shift=shift2)

            E_pixel = getEncryptedPixel(input_pixel=D_pixel, shift=shift)
        else:
            E_pixel = getEncryptedPixel(input_pixel=pixel, shift=shift)

        # Stores the changes onto the copied image’s pixel map
        copyImagePixelData[pixelX, pixelY] = E_pixel


def decryptPixels(width, height, shifts, encryptedImagePixelData, copyImagePixelData, isTripleDES=None):
    # In Triple DES, the shifts come in a pair
    if isTripleDES is True:
        shifts_list = shifts[0]
        second_shifts = shifts[1]
    else:
        shifts_list = shifts

    for pixelTuple in getPixelData(width=width, height=height, shifts=shifts_list):
        # Sets the pixel's X and Y values; and the key value, from the tuple given by the generator function
        pixelX, pixelY, shift = pixelTuple[0], pixelTuple[1], pixelTuple[2]

        # Gets each pixel value from the original image
        pixel = encryptedImagePixelData[pixelX, pixelY]

        if isTripleDES is True:
            D_pixel_temp = getDecryptedPixel(input_pixel=pixel, shift=shift)

            shift2 = second_shifts[shifts_list.index(shift)]
            E_pixel = getEncryptedPixel(input_pixel=D_pixel_temp, shift=shift2)

            D_pixel = getDecryptedPixel(input_pixel=E_pixel, shift=shift)
        else:
            D_pixel = getDecryptedPixel(input_pixel=pixel, shift=shift)

        # Stores the changes onto the copied image’s pixel map
        copyImagePixelData[pixelX, pixelY] = D_pixel

def loadEncryption(filename, filepath, originalImage, imageFormat, shifts, cipherUsed):
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
    if cipherUsed == "TripleDES":
        encryptPixels(width=width, height=height, shifts=shifts, originalImagePixelData=originalImagePixelData, copyImagePixelData=copyImagePixelData, isTripleDES=True)
    else:
        encryptPixels(width=width, height=height, shifts=shifts, originalImagePixelData=originalImagePixelData, copyImagePixelData=copyImagePixelData)

    # Closes the original image
    originalImage.close()

    # Rotates and flips the image to make the encrypted image more different than the original
    copyImage = copyImage.rotate(180)
    copyImage = copyImage.transpose(Image.FLIP_LEFT_RIGHT)

    """
    All the filenames are saved as .png, as JPG files perform
    lossy compression. This alters the encrypted pixels and is
    not beneficial when decrypting.
    """
    newFilename = "{}/{}_{}ENC.png".format(filepath, filename[:-4], cipherUsed)

    # Saves the encrypted image and then close it
    copyImage.save(newFilename)
    copyImage.close()

    return newFilename


def loadDecryption(filename, filepath, shifts, cipherUsed):
    """Gets the image pixel data, manipulates the image, then saves it"""

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
    if cipherUsed == "TripleDES":
        decryptPixels(width=width, height=height, shifts=shifts, encryptedImagePixelData=encryptedImagePixelData, copyImagePixelData=copyPixelMap, isTripleDES=True)
    else:
        decryptPixels(width=width, height=height, shifts=shifts, encryptedImagePixelData=encryptedImagePixelData, copyImagePixelData=copyPixelMap)

    # Closes the input image
    inputImage.close()

    newFilename = "{}/{}".format(filepath, filename.replace("ENC", "DEC"))

    # Saves the encrypted image
    copyImage.save(newFilename)
    copyImage.close()

    return newFilename


def encryptionImageHandler(filename, filepath, shifts, cipherUsed):
    """Checks if the original image needs to be converted to RGBA format"""

    full_filename = filepath + "/" + filename
    originalImage = Image.open(full_filename)

    # Gets the extension of the image
    extension = filename.split(".")[-1]

    # Checks if the image type is PNG and if Triple DES encryption is not used
    if extension == "png":
        # PNG images need to be converted to RGBA format
        originalImage = originalImage.convert("RGBA")

    encryptedData = loadEncryption(filename=filename, filepath=filepath, originalImage=originalImage, imageFormat=extension, shifts=shifts, cipherUsed=cipherUsed)

    return encryptedData


def encrypt(filename, filepath, shifts, cipherUsed):
    encryptedData = encryptionImageHandler(filename=filename, filepath=filepath, shifts=shifts, cipherUsed=cipherUsed)

    return encryptedData


def decrypt(filename, filepath, shifts, cipherUsed):
    decryptedData = loadDecryption(filename=filename, filepath=filepath, shifts=shifts, cipherUsed=cipherUsed)

    return decryptedData
