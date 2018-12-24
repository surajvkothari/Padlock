from PIL import Image
import itertools

# Define a generator function
def getPixelData(width, height, shifts):
    # Iterate through the pixel values of width and height combined from itertools.product()
    # and iterate through the shifts in a cycle using itertools.cycle()
    for pixelValue, key in zip(itertools.product(width, height), itertools.cycle(shifts)):
        # Returns a tuple: (width,height,key)
        yield (*pixelValue, key)

# Encrypt the individual pixels with a shift
def encryptPixels(width,height,imageFormat,shifts,originalImagePixelData,copyImagePixelData,isTripleDES=None):
    for pixelTuple in getPixelData(width=width, height=height, shifts=shifts):
        # Set the pixel X,Y values and the key value from the tuple returned from the generator function
        pixelX,pixelY,shift = pixelTuple[0],pixelTuple[1],pixelTuple[2]

        # Get each pixel value from original image
        pixel = originalImagePixelData[pixelX,pixelY]

        # Set the R,G,B values of each pixel
        R = pixel[0]
        G = pixel[1]
        B = pixel[2]

        # Shift each colour of the pixel by the shift to get the new pixel values
        colourRed = (R + shift) % 256
        colourGreen = (G + shift) % 256
        colourBlue = (B + shift) % 256

        # Check if the image is of a PNG format
        # if R == 199 and G == 198 and B == 199:
        #     print(imageFormat,isTripleDES)
        if imageFormat == "png" and isTripleDES != True:
            # PNG images have an alpha channel
            A = pixel[3]
            alpha = (A + shift) % 256


            # Store the changes onto the copied image’s pixel map with the alpha channel value
            copyImagePixelData[pixelX,pixelY] = (colourRed,colourGreen,colourBlue,alpha)
        else:
            # Store the changes onto the copied image’s pixel map
            copyImagePixelData[pixelX,pixelY] = (colourRed,colourGreen,colourBlue)

def decryptPixels(width,height,shifts,encryptedImagePixelData,copyImagePixelData):
    pixelValues = len(encryptedImagePixelData[0,0])
    for pixelTuple in getPixelData(width=width, height=height, shifts=shifts):
        """
        Determine the number of values in each pixel of the image.
        This will help to distinguish between PNG and JPG images
        as the encrypted image will always be saved as a PNG.
        PNG images have an alpha channel, however when converted from JPG to PNG,
        the alpha channel doesn't exist, so the pixels have only RGB
        """

        # Set the pixel X,Y values and the key value from the tuple returned from the generator function
        pixelX,pixelY,shift = pixelTuple[0],pixelTuple[1],pixelTuple[2]

        # Get each pixel value from original image
        pixel = encryptedImagePixelData[pixelX,pixelY]

        # Set the R,G,B values of each pixel
        R = pixel[0]
        G = pixel[1]
        B = pixel[2]

        # Shift each colour of the pixel by the shift to get the new pixel values
        colourRed = (R - shift) % 256
        colourGreen = (G - shift) % 256
        colourBlue = (B - shift) % 256

        # Check if the number of pixel values is = 4, as that means the original
        # image was a png and we need to decrypt its alpha channel aswell.
        if pixelValues == 4:
            # PNG images have an alpha channel
            A = pixel[3]
            alpha = (A - shift) % 256

            # Copy the changes onto the copied image data with the alpha channel value
            copyImagePixelData[pixelX,pixelY] = (colourRed,colourGreen,colourBlue,alpha)
        else:
            # Copy the changes onto the copied image data
            copyImagePixelData[pixelX,pixelY] = (colourRed,colourGreen,colourBlue)

def loadEncryption(filename,originalImage,imageFormat,shifts,cipherUsed,isTripleDES=None):
    # Get a pixel access object for the original image
    # The pixel access object will behave like a 2D array
    # This will allow me to read and modify individual pixels
    originalImagePixelData = originalImage.load()

    # Create a new image with the mode and size attributes taken from the original image
    copyImage = Image.new(originalImage.mode, originalImage.size)
    # Get a pixel access object for the copied image
    copyImagePixelData = copyImage.load()

    # Get width and height of the copied image
    width = range(copyImage.size[0])
    height = range(copyImage.size[1])

    # Pass all the necessary arguments to encrypt the pixels
    encryptPixels(width=width,height=height,imageFormat=imageFormat,shifts=shifts,
    originalImagePixelData=originalImagePixelData,copyImagePixelData=copyImagePixelData,isTripleDES=isTripleDES)

    # Close the original image
    originalImage.close()

    # Rotate and flip the image to make the encrypted image more different than the original
    copyImage = copyImage.rotate(180)
    copyImage = copyImage.transpose(Image.FLIP_LEFT_RIGHT)

    # Save the image as a PNG, as JPGs compress the image, resulting in a change of pixel values
    newFilename = "../Resources/doctorwho_" + cipherUsed + "ENC" + ".png"

    # Save the encrypted image and then close it
    copyImage.save(newFilename)
    copyImage.close()

    return newFilename

def loadDecryption(encryptedImage,shifts,cipherUsed):
    # Flip the image to original format
    encryptedImage = encryptedImage.transpose(Image.FLIP_LEFT_RIGHT)

    # Rotate the image to original format
    encryptedImage = encryptedImage.rotate(180)

    # Get a pixel access object for the encrypted image
    # The pixel access object will behave like a 2D array
    encryptedImagePixelData = encryptedImage.load()

    # Make a copy of the input image and load the new pixel map
    copyImage = Image.new(encryptedImage.mode, encryptedImage.size)
    copyPixelMap = copyImage.load()

    # Get width and height of the copied encrypted image
    width = range(copyImage.size[0])
    height = range(copyImage.size[1])

    # Pass all the necessary arguments to encrypt the pixels
    decryptPixels(width=width,height=height,shifts=shifts,
    encryptedImagePixelData=encryptedImagePixelData,copyImagePixelData=copyPixelMap)

    # Close the input image
    encryptedImage.close()

    newFilename = "../Resources/doctorwho_" + cipherUsed + "DEC" + ".png"

    # Save the encrypted image
    copyImage.save(newFilename)
    copyImage.close()

    return newFilename

# Distinguishes the type of image before encrypting it.
def encryptionImageHandler(filename,shifts,cipherUsed,isTripleDES=None):
    # Open the original image
    originalImage = Image.open(filename)

    # Determine the extension of the image by taking the last item of splitting
    # the filename from a "."
    extension = filename.split(".")[-1]

    # Jpg images don't need to be converted
    # therefore check extension for the other file format: PNG
    if extension == "png" and isTripleDES != True:
        # PNG images need to be converted to RGBA format
        originalImage = originalImage.convert("RGBA")

    encryptedData = loadEncryption(filename=filename,originalImage=originalImage,imageFormat=extension,shifts=shifts,cipherUsed=cipherUsed,isTripleDES=isTripleDES)
    return encryptedData

def encrypt(filename,shifts,cipherUsed,isTripleDES=None):
    encryptedData = encryptionImageHandler(filename=filename,shifts=shifts,cipherUsed=cipherUsed,isTripleDES=isTripleDES)
    return encryptedData

def decrypt(filename,shifts,cipherUsed):
    inputImage = Image.open(filename)
    decryptedData = loadDecryption(encryptedImage=inputImage,shifts=shifts,cipherUsed=cipherUsed)
    return decryptedData
