import caesarCipher
import base64
import os
import difflib

def encryptFile(filename, passKey):
    """Encrypts the contents of any file"""

    with open(filename, "rb") as f:
        test = f.read()
        """
        Converts the binary file contents to base64
        and then formats it into ASCII form.
        """
        encoded = base64.b64encode(test).decode("ascii")
    
    #Encrypted = encoded
    guide_data, Encrypted = caesarCipher.encrypt(plaintext=encoded, passKey=passKey, dataformat="Messages", cipherMode="ASCII")

    extension = os.path.splitext(filename)[1]
    newFilename = "{}_{}ENC{}".format(filename[:-5], 'caesar', extension)
        
    # Converts the ASCII encryption into bytes form to write to new file
    Encrypted = bytes(Encrypted,'utf-8')  

    # Writes encrypted data to new file
    with open(newFilename, 'wb') as f2:
        f2.write(Encrypted) 

    return newFilename


def decryptFile(filename, passKey):
    """Decrypts the contents of any file"""
    
    with open(filename, "rb") as f:
        # Formats the binary file into ASCII form.
        content = f.read().decode("ascii")

    guide_data, Decrypted = caesarCipher.decrypt(ciphertext=content, passKey=passKey, dataformat="Messages", cipherMode="ASCII")

    #Decrypted = content
    newFilename = "test_over2.docx"#"{}/{}".format(filename[:-5], filename.replace("ENC", "DEC"))

    # Converts the ASCII into bytes and then decodes it from base64 to original
    
    decryptedContent = base64.b64decode(bytes(Decrypted,'utf-8'))

    # Creates decrypted file   
    with open(newFilename, 'wb') as f2:
        f2.write(decryptedContent)

    return newFilename

encryptFile("C:/Users/Suraj/Documents/Computer Science - A Level/NEA Project/Version 11 - Base 64 Encoding/Scripts/test2.docx", "helloWorld123")
decryptFile("C:/Users/Suraj/Documents/Computer Science - A Level/NEA Project/Version 11 - Base 64 Encoding/Scripts/test2_caesarENC.docx", "helloWorld123")
