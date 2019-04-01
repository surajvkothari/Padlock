#!/usr/bin/env python3
"""
Padlock Encryption Software
Copyright 2019

Created by: Suraj Kothari
For A-level Computer Science
at Woodhouse College.
"""

import multicrypt
import tkinter as tk
import tkinter.ttk
import tkinter.filedialog
import os
import urllib
import webbrowser
import time
from PIL import Image, ImageTk
from styles import *


class Padlock(tk.Tk):
    """The main application class that manages the individual frames"""

    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Padlock Encryption Software")
        self.geometry("1100x600")  # Default application window size

        # Doesn't allow the application to resize below the given resolution
        self.minsize(1100, 600)

        """Makes the application responsive when resizing"""
        top = self.winfo_toplevel()  # Gets the top level window to resize

        # Makes the rows and columns of the window responsive by scale factor 1
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)
        top.rowconfigure(1, weight=1)

        self.configure(background="white")

        """Creates a footer"""
        footer = tk.Frame(self, bg=Colours.SECONDARY)
        self.copyrightMessage = "Copyright 2019 - Padlock Encryption Software. \
Created by: Suraj Kothari. For A-level Computer Science at Woodhouse College."
        copyrightText = tk.Label(footer, text=self.copyrightMessage,
            bg=Colours.SECONDARY, fg="white", font=Fonts.SMALL_PRINT)

        footer.grid(row=2, sticky="ew")
        copyrightText.grid()

        self._frame = None  # Clears the current frame

        # Sets the current frame to the home page
        self.switch_frame(HomePage)
        #self.switch_frame(EncryptMenu, process="Encrypt", dataFormat="Files", cipher="Triple DES Cipher", cipherMode="Base64")

    def switch_frame(self, frame_class, process=None, dataFormat=None, cipher=None, cipherMode=None):
        """Destroys current frame and replaces it with a new one."""

        """
        By default, all extra necessary arguments are passed to all classes,
        even if they don't require it. This removes the need to check
        which class needs individual extra arguments.
        """
        new_frame = frame_class(self, process, dataFormat, cipher, cipherMode)

        # Check if the current frame exists, then destroy it
        if self._frame is not None:
            self._frame.destroy()

        self._frame = new_frame

        # Position the individual frames on the first row (above the footer)
        self._frame.grid(row=1, sticky="n")


class HomePage(tk.Frame):
    """Creates the home page frame"""

    def __init__(self, master, process, dataFormat, cipher, cipherMode):
        tk.Frame.__init__(self, master)

        self.configure(background=Colours.BACKGROUND)

        # Initialises the icons used for this frame
        self.icon = Image.open("Images/encryptIcon.png")
        self.icon2 = Image.open("Images/decryptIcon.png")

        # Makes the icon able to be used by widgets with these references
        self.ENCRYPT_ICON = ImageTk.PhotoImage(self.icon)
        self.DECRYPT_ICON = ImageTk.PhotoImage(self.icon2)

        self.createWidgets()

    def createWidgets(self):
        self.master = self.winfo_toplevel()  # Gets the top level window

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN,
            fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.BACKGROUND,
            fg=Colours.FOREGROUND, font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, sticky="ns", ipadx=40, pady=(10, 0))

        self.encryptButton = tk.Button(self, text="Encrypt", compound="left", image=self.ENCRYPT_ICON,
            command=lambda: self.master.switch_frame(FormatSelctionMenu, process="Encrypt"),
                **ButtonStyle.ENCRYPT_BUTTON)
        self.verticalSeparator = tk.ttk.Separator(self, orient="vertical")
        self.decryptButton = tk.Button(self, text="Decrypt", compound="left", image=self.DECRYPT_ICON,
            command=lambda: self.master.switch_frame(FormatSelctionMenu, process="Decrypt"),
                **ButtonStyle.DECRYPT_BUTTON)

        # Keeps an extra reference to the image objects
        self.encryptButton.image = self.ENCRYPT_ICON
        self.decryptButton.image = self.DECRYPT_ICON

        self.encryptButton.grid(padx=26)
        self.verticalSeparator.grid(column=1, row=0, rowspan=1, sticky="ns")
        self.decryptButton.grid(column=2, row=0, padx=26)

        # Creates hover listeners for the buttons to change colour when hovered
        self.encryptButton.bind("<Enter>", lambda e: self.encryptButton.configure(
            bg=ButtonStyle.ENCRYPT_BUTTON["activebackground"]))
        self.encryptButton.bind("<Leave>", lambda e: self.encryptButton.configure(
            bg=ButtonStyle.ENCRYPT_BUTTON["bg"]))
        self.decryptButton.bind("<Enter>", lambda e: self.decryptButton.configure(
            bg=ButtonStyle.DECRYPT_BUTTON["activebackground"]))
        self.decryptButton.bind("<Leave>", lambda e: self.decryptButton.configure(
            bg=ButtonStyle.DECRYPT_BUTTON["bg"]))


class FormatSelctionMenu(tk.Frame):
    """Creates the data format selection page frame"""

    def __init__(self, master, process, dataFormat, cipher, cipherMode):
        tk.Frame.__init__(self, master)

        self.process = process

        # Initialises the icons used in this frame
        self.icon = Image.open("Images/messageIcon.png")
        self.icon2 = Image.open("Images/fileIcon.png")
        self.icon3 = Image.open("Images/imageIcon.png")

        # Makes the icon able to be used by widgets with these references
        self.MESSAGE_ICON = ImageTk.PhotoImage(self.icon)
        self.FILE_ICON = ImageTk.PhotoImage(self.icon2)
        self.IMAGE_ICON = ImageTk.PhotoImage(self.icon3)

        self.configure(background=Colours.BACKGROUND)

        self.createWidgets()

    def createWidgets(self):
        self.master = self.winfo_toplevel()  # Gets the top level window

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN,
            fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN,
            fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process,
            bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, sticky="ns", ipadx=40,
            padx=10, pady=(10, 0))

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))

        self.messageButton = tk.Button(self, text="Messages", compound="left", image=self.MESSAGE_ICON,
            command=lambda: self.master.switch_frame(CipherMenu, process=self.process, dataFormat="Messages"),
        **ButtonStyle.MESSAGE_BUTTON)

        self.verticalSeparator = tk.ttk.Separator(self, orient="vertical")

        self.fileButton = tk.Button(self, text="Files", compound="left", image=self.FILE_ICON,
            command=lambda: self.master.switch_frame(CipherMenu, process=self.process, dataFormat="Files"),
        **ButtonStyle.FILE_BUTTON)

        self.verticalSeparator2 = tk.ttk.Separator(self, orient="vertical")

        self.imageButton = tk.Button(self, text="Images", compound="left", image=self.IMAGE_ICON,
            command=lambda: self.master.switch_frame(CipherMenu, process=self.process, dataFormat="Images"),
        **ButtonStyle.IMAGE_BUTTON)

        self.messageButton.grid(padx=26)
        self.verticalSeparator.grid(column=1, row=0, rowspan=1, sticky="ns")
        self.fileButton.grid(column=2, row=0, padx=26)
        self.verticalSeparator2.grid(column=3, row=0, rowspan=1, sticky="ns")
        self.imageButton.grid(column=4, row=0, padx=26)

        # Creates hover listeners for the buttons to change colour when hovered
        self.messageButton.bind("<Enter>", lambda e: self.messageButton.configure(
            bg=ButtonStyle.MESSAGE_BUTTON["activebackground"]))
        self.messageButton.bind("<Leave>", lambda e: self.messageButton.configure(
            bg=ButtonStyle.MESSAGE_BUTTON["bg"]))
        self.fileButton.bind("<Enter>", lambda e: self.fileButton.configure(
            bg=ButtonStyle.FILE_BUTTON["activebackground"]))
        self.fileButton.bind("<Leave>", lambda e: self.fileButton.configure(
            bg=ButtonStyle.FILE_BUTTON["bg"]))
        self.imageButton.bind("<Enter>", lambda e: self.imageButton.configure(
            bg=ButtonStyle.IMAGE_BUTTON["activebackground"]))
        self.imageButton.bind("<Leave>", lambda e: self.imageButton.configure(
            bg=ButtonStyle.IMAGE_BUTTON["bg"]))


class CipherMenu(tk.Frame):
    """Creates the cipher selection page frame"""
    def __init__(self, master, process, dataFormat, cipher, cipherMode):
        tk.Frame.__init__(self, master)

        self.process = process
        self.dataFormat = dataFormat

        self.configure(background=Colours.BACKGROUND)

        self.createWidgets()

    def createWidgets(self):
        self.master = self.winfo_toplevel()  # Gets the top level window

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))

        if self.dataFormat == "Images":
            # If an image format is chosen, the button will go directly to the encrypt/decrypt menu. Mode selection is ignored.
            self.caesar_Button = tk.Button(self, text="Caesar",
                command=lambda: self.master.switch_frame(EncryptMenu, process=self.process,
                    dataFormat=self.dataFormat, cipher="Caesar Cipher") \
                    if self.process == "Encrypt" else \
                    self.master.switch_frame(DecryptMenu, process=self.process,
                        dataFormat=self.dataFormat, cipher="Caesar Cipher"), **ButtonStyle.CAESAR_BUTTON)

            self.vigenere_Button = tk.Button(self, text="Vigenere",
                command=lambda: self.master.switch_frame(EncryptMenu, process=self.process,
                    dataFormat=self.dataFormat, cipher="Vigenere Cipher") \
                        if self.process == "Encrypt" else \
                        self.master.switch_frame(DecryptMenu, process=self.process,
                            dataFormat=self.dataFormat, cipher="Vigenere Cipher"), **ButtonStyle.VIGENERE_BUTTON)

        else:
            self.caesar_Button = tk.Button(self, text="Caesar",
                command=lambda: self.master.switch_frame(CipherModeMenu, process=self.process,
                    dataFormat=self.dataFormat, cipher="Caesar Cipher"), **ButtonStyle.CAESAR_BUTTON)

            self.vigenere_Button = tk.Button(self, text="Vigenere",
                command=lambda: self.master.switch_frame(CipherModeMenu, process=self.process,
                    dataFormat=self.dataFormat, cipher="Vigenere Cipher"), **ButtonStyle.VIGENERE_BUTTON)

        self.verticalSeparator = tk.ttk.Separator(self, orient="vertical")

        if self.dataFormat == "Files":
            self.DES_Button = tk.Button(self, text="DES",
                command=lambda: self.master.switch_frame(CipherModeMenu, process=self.process,
                    dataFormat=self.dataFormat, cipher="DES Cipher"), **ButtonStyle.DES_BUTTON)

            self.triple_DES_Button = tk.Button(self, text="Triple DES",
                command=lambda: self.master.switch_frame(CipherModeMenu, process=self.process,
                    dataFormat=self.dataFormat, cipher="Triple DES Cipher"), **ButtonStyle.TRIPLE_DES_BUTTON)
        else:
            self.DES_Button = tk.Button(self, text="DES",
                command=lambda: self.master.switch_frame(EncryptMenu, process=self.process,
                    dataFormat=self.dataFormat, cipher="DES Cipher") \
                        if self.process == "Encrypt" else \
                            self.master.switch_frame(DecryptMenu, process=self.process,
                                dataFormat=self.dataFormat, cipher="DES Cipher"), **ButtonStyle.DES_BUTTON)

            self.triple_DES_Button = tk.Button(self, text="Triple DES",
                command=lambda: self.master.switch_frame(EncryptMenu, process=self.process,
                    dataFormat=self.dataFormat, cipher="Triple DES Cipher") \
                        if self.process == "Encrypt" else \
                            self.master.switch_frame(DecryptMenu, process=self.process,
                                dataFormat=self.dataFormat, cipher="Triple DES Cipher"), **ButtonStyle.TRIPLE_DES_BUTTON)

        self.weakText = tk.Label(self, text="WEAK CIPHERS", bg=Colours.BACKGROUND,
            fg=Colours.INFO, font=Fonts.INFO)
        self.medText = tk.Label(self, text="MEDIUM CIPHERS", bg=Colours.BACKGROUND,
            fg=Colours.INFO, font=Fonts.INFO)

        self.weakText.grid(row=0, column=0, padx=26, pady=(0,5))
        self.caesar_Button.grid(row=1, column=0, padx=26, pady=(0, 10))
        self.vigenere_Button.grid(row=2, column=0, padx=26, pady=(10, 0))
        self.verticalSeparator.grid(column=1, row=1, rowspan=2, sticky="ns")
        self.medText.grid(column=2, row=0, padx=26, pady=(0,5))
        self.DES_Button.grid(column=2, row=1, padx=26, pady=(0, 10))
        self.triple_DES_Button.grid(column=2, row=2, padx=26, pady=(10, 0))

        # Creates hover listeners for the buttons to change colour when hovered
        self.caesar_Button.bind("<Enter>", lambda e: self.caesar_Button.configure(
            bg=ButtonStyle.CAESAR_BUTTON["activebackground"]))
        self.caesar_Button.bind("<Leave>", lambda e: self.caesar_Button.configure(
            bg=ButtonStyle.CAESAR_BUTTON["bg"]))
        self.vigenere_Button.bind("<Enter>", lambda e: self.vigenere_Button.configure(
            bg=ButtonStyle.VIGENERE_BUTTON["activebackground"]))
        self.vigenere_Button.bind("<Leave>", lambda e: self.vigenere_Button.configure(
            bg=ButtonStyle.VIGENERE_BUTTON["bg"]))
        self.DES_Button.bind("<Enter>", lambda e: self.DES_Button.configure(
            bg=ButtonStyle.DES_BUTTON["activebackground"]))
        self.DES_Button.bind("<Leave>", lambda e: self.DES_Button.configure(
            bg=ButtonStyle.DES_BUTTON["bg"]))
        self.triple_DES_Button.bind("<Enter>", lambda e: self.triple_DES_Button.configure(
            bg=ButtonStyle.TRIPLE_DES_BUTTON["activebackground"]))
        self.triple_DES_Button.bind("<Leave>", lambda e: self.triple_DES_Button.configure(
            bg=ButtonStyle.TRIPLE_DES_BUTTON["bg"]))


class CipherModeMenu(tk.Frame):
    """Creates the mode selection page frame"""

    """Creates the cipher selection page frame"""
    def __init__(self, master, process, dataFormat, cipher, cipherMode):
        tk.Frame.__init__(self, master)

        self.process = process
        self.dataFormat = dataFormat
        self.cipher = cipher
        self.cipherMode = cipherMode

        self.configure(background=Colours.BACKGROUND)

        self.createWidgets()

    def createWidgets(self):
        self.master = self.winfo_toplevel()  # Gets the top level window

        self.classic_text = "Uses the English Alphabet. This will NOT encrypt/decrypt ASCII characters, \
such as punctuation and numbers. Use for text files."
        self.classic_text2 = "Encrypts/decrypts just text files."
        self.ascii_text = "This will encrypt/decrypt ASCII characters such as punctuation and numbers. Use for text files."
        self.base64_text = "Uses Base64 to encode files before encrypting/decrypting them. Use for files of any type."
        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text="Mode Select", bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))

        # If chosen format is files and either DES or Triple DES is selected, create these widgets
        if self.dataFormat == "Files" and self.cipher in ("DES Cipher", "Triple DES Cipher"):
            self.classicButton = tk.Button(self, text="Classic",
            command=lambda: self.master.switch_frame(EncryptMenu, process=self.process, dataFormat=self.dataFormat,
                cipher=self.cipher, cipherMode="Classic") \
                    if self.process == "Encrypt" else \
                        self.master.switch_frame(DecryptMenu, process=self.process,
                            dataFormat=self.dataFormat, cipher=self.cipher, cipherMode="Classic"), **ButtonStyle.CLASSIC_BUTTON)
            self.classicText = tk.Label(self, text=self.classic_text2, wraplength=220, bg=Colours.BACKGROUND,
                fg=Colours.INFO, font=Fonts.INFO)

            self.verticalSeparator = tk.ttk.Separator(self, orient="vertical")

            self.base64Button = tk.Button(self, text="Base64",
            command=lambda: self.master.switch_frame(EncryptMenu, process=self.process,
                dataFormat=self.dataFormat, cipher=self.cipher, cipherMode="Base64") \
                    if self.process == "Encrypt" else \
                        self.master.switch_frame(DecryptMenu, process=self.process,
                            dataFormat=self.dataFormat, cipher=self.cipher, cipherMode="Base64"), **ButtonStyle.BASE64_BUTTON)
            self.Base64_Text = tk.Label(self, text=self.base64_text, bg=Colours.BACKGROUND,
                wraplength=220, fg=Colours.INFO, font=Fonts.INFO)

            self.classicButton.grid(padx=20)
            self.classicText.grid(row=1, padx=20, pady=10)
            self.verticalSeparator.grid(column=1, row=0, rowspan=1, sticky="ns")
            self.base64Button.grid(column=2, row=0, padx=20)
            self.Base64_Text.grid(column=2, row=1, padx=20, pady=10)

            # Creates hover listeners for the buttons to change colour when hovered
            self.classicButton.bind("<Enter>", lambda e: self.classicButton.configure(
                bg=ButtonStyle.CLASSIC_BUTTON["activebackground"]))
            self.classicButton.bind("<Leave>", lambda e: self.classicButton.configure(
                bg=ButtonStyle.CLASSIC_BUTTON["bg"]))
            self.base64Button.bind("<Enter>", lambda e: self.base64Button.configure(
                bg=ButtonStyle.BASE64_BUTTON["activebackground"]))
            self.base64Button.bind("<Leave>", lambda e: self.base64Button.configure(
                bg=ButtonStyle.BASE64_BUTTON["bg"]))
        else:
            self.classicButton = tk.Button(self, text="Classic",
            command=lambda: self.master.switch_frame(EncryptMenu, process=self.process, dataFormat=self.dataFormat,
                cipher=self.cipher, cipherMode="Classic") \
                    if self.process == "Encrypt" else \
                        self.master.switch_frame(DecryptMenu, process=self.process,
                            dataFormat=self.dataFormat, cipher=self.cipher, cipherMode="Classic"), **ButtonStyle.CLASSIC_BUTTON)
            self.classicText = tk.Label(self, text=self.classic_text, wraplength=300, bg=Colours.BACKGROUND,
                fg=Colours.INFO, font=Fonts.INFO)

            self.verticalSeparator = tk.ttk.Separator(self, orient="vertical")

            self.asciiButton = tk.Button(self, text="ASCII",
            command=lambda: self.master.switch_frame(EncryptMenu, process=self.process,
                dataFormat=self.dataFormat, cipher=self.cipher, cipherMode="ASCII") \
                    if self.process == "Encrypt" else \
                        self.master.switch_frame(DecryptMenu, process=self.process,
                            dataFormat=self.dataFormat, cipher=self.cipher, cipherMode="ASCII"), **ButtonStyle.ASCII_BUTTON)
            self.ASCII_Text = tk.Label(self, text=self.ascii_text, bg=Colours.BACKGROUND,
                wraplength=310, fg=Colours.INFO, font=Fonts.INFO)

            self.classicButton.grid(padx=20)
            self.classicText.grid(row=1, padx=20, pady=10)
            self.verticalSeparator.grid(column=1, row=0, rowspan=1, sticky="ns")
            self.asciiButton.grid(column=2, row=0, padx=20)
            self.ASCII_Text.grid(column=2, row=1, padx=20, pady=10)

            if self.dataFormat == "Files":
                self.base64Button = tk.Button(self, text="Base64",
                command=lambda: self.master.switch_frame(EncryptMenu, process=self.process,
                    dataFormat=self.dataFormat, cipher=self.cipher, cipherMode="Base64") \
                        if self.process == "Encrypt" else \
                            self.master.switch_frame(DecryptMenu, process=self.process,
                                dataFormat=self.dataFormat, cipher=self.cipher, cipherMode="Base64"), **ButtonStyle.BASE64_BUTTON)
                self.Base64_Text = tk.Label(self, text=self.base64_text, bg=Colours.BACKGROUND,
                    wraplength=220, fg=Colours.INFO, font=Fonts.INFO)

                self.verticalSeparator2 = tk.ttk.Separator(self, orient="vertical")

                self.verticalSeparator2.grid(column=3, row=0, rowspan=1, sticky="ns")
                self.base64Button.grid(column=4, row=0, padx=20)
                self.Base64_Text.grid(column=4, row=1, padx=20, pady=10)

                self.base64Button.bind("<Enter>", lambda e: self.base64Button.configure(
                    bg=ButtonStyle.BASE64_BUTTON["activebackground"]))
                self.base64Button.bind("<Leave>", lambda e: self.base64Button.configure(
                    bg=ButtonStyle.BASE64_BUTTON["bg"]))

            # Creates hover listeners for the buttons to change colour when hovered
            self.classicButton.bind("<Enter>", lambda e: self.classicButton.configure(
                bg=ButtonStyle.CLASSIC_BUTTON["activebackground"]))
            self.classicButton.bind("<Leave>", lambda e: self.classicButton.configure(
                bg=ButtonStyle.CLASSIC_BUTTON["bg"]))
            self.asciiButton.bind("<Enter>", lambda e: self.asciiButton.configure(
                bg=ButtonStyle.ASCII_BUTTON["activebackground"]))
            self.asciiButton.bind("<Leave>", lambda e: self.asciiButton.configure(
                bg=ButtonStyle.ASCII_BUTTON["bg"]))


class EncryptMenu(tk.Frame):
    """Creates the encryption page frame"""

    def __init__(self, master, process, dataFormat, cipher, cipherMode):
        tk.Frame.__init__(self, master)

        self.process = process
        self.dataFormat = dataFormat
        self.cipher = cipher
        self.cipherMode = cipherMode

        self.configure(background=Colours.GREY_BACKGROUND, padx=10, pady=50)

        # Initialises the icon used for this frame
        self.icon = Image.open("Images/copyIcon.png")
        self.icon2 = Image.open("Images/imageUpload.png")

        # Makes the icon able to be used by widgets with these references
        self.COPY_ICON = ImageTk.PhotoImage(self.icon)
        self.IMAGE_UPLOAD = ImageTk.PhotoImage(self.icon2)

        """
        Calls the necessary functions that create the widgets
        for the corresponding section based on the data format
        """

        if self.dataFormat == "Messages":
            # Triple DES requires a separate section
            if self.cipher == "Triple DES Cipher":
                self.messageSectionForTripleDES()
            else:
                self.messageSection()

        elif self.dataFormat == "Files":
            if self.cipher == "Triple DES Cipher":
                self.fileSectionForTripleDES()
            else:
                self.fileSection()

        elif self.dataFormat == "Images":
            if self.cipher == "Triple DES Cipher":
                self.imageSectionForTripleDES()
            else:
                self.imageSection()

    def messageSection(self):
        def updateOutputBox():
            """
            Gets the contents of the input and key boxes, then checks them for
            validation, before retrieving the ciphertext from the
            multicrypt module. Lastly, the ciphertext is placed in the output box.
            """

            p = self.inputBox.get()
            k = self.keyBox.get()

            self.outputBox.delete("1.0", "end")
            self.outputBox.configure(state="disabled", cursor="X_cursor")
            self.error.grid(sticky="w", pady=(5, 0))

            if p == "":
                self.errorMessage.set("The plaintext field is empty.")
                self.guidelink.grid_forget()
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                self.guidelink.grid_forget()
                return None

            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.guidelink.grid_forget()
                return None

            # ONLY for Vigenere Cipher in CLASSIC mode
            if self.cipher == "Vigenere Cipher" and self.cipherMode == "Classic" and not(k.isalpha()):
                self.errorMessage.set("The key must not contain any ASCII characters.")
                self.guidelink.grid_forget()
                return None

            self.error.grid_forget()  # Removes the error message
            self.errorMessage.set("")

            self.guide_data, cipherText = multicrypt.encrypt(plaintext=p, passKey=k, cipher=self.cipher,
                dataformat=self.dataFormat, cipherMode=self.cipherMode)

            self.outputBox.configure(state="normal", cursor="xterm")
            self.outputBox.insert("1.0", cipherText)
            self.horizontalSeparatorGuide.grid(sticky="we")
            self.guidelink.grid(sticky="w", pady=(5, 0))

        def copyInputToClipboard():
            i = self.inputBox.get()
            i = i.split("\n")[0]  # The new line character is ommited.
            self.master.clipboard_clear()
            self.master.clipboard_append(i)

        def copyOutputToClipboard():
            o = self.outputBox.get("1.0", "end")
            o = o.split("\n")[0]  # The new line character is ommited.
            self.master.clipboard_clear()
            self.master.clipboard_append(o)

        def openguide():
            # Converts guide data dictionary to url form
            url_data = urllib.parse.urlencode(self.guide_data)

            # Opens default windows browser. Without it, it opens IE.
            if self.cipher == "Caesar Cipher":
                if self.cipherMode == "ASCII":
                    #url = r"https://alpha.prkl.tech/suraj-padlockserver/caesar/caesar.html?" + (url_data)
                    url = r"http://localhost/padlock/caesar/caesar_ASCII.html?" + (url_data)
                else:
                    url = r"http://localhost/padlock/caesar/caesar_classic.html?" + (url_data)

            elif self.cipher == "Vigenere Cipher":
                if self.cipherMode == "ASCII":
                    url = r"http://localhost/padlock/vigenere/vigenere_ASCII.html?" + (url_data)
                else:
                    url = r"http://localhost/padlock/vigenere/vigenere_classic.html?" + (url_data)

            elif self.cipher == "DES Cipher":
                #url = r"https://alpha.prkl.tech/suraj-padlockserver/DES/DES.html?" + (url_data)
                url = r"http://localhost/padlock/DES/DES.html?" + (url_data)

            webbrowser.get('windows-default').open_new(url)

        self.errorMessage = tk.StringVar()  # Text variable that stores the different error messages

        self.master = self.winfo_toplevel()  # Gets the top level window

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipherMode, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag4 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)

        # DES cipher has no modes so this won't display the mode tag
        if self.cipher == "DES Cipher":
            self.sectionTag4.grid(column=5, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)
        else:
            self.sectionTag3.grid(column=4, row=0, pady=(10, 0), padx=10)
            self.sectionTag4.grid(column=5, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))
        self.sectionTag3.bind("<Button-1>", lambda e: self.master.switch_frame(CipherModeMenu, process=self.process,
            dataFormat=self.dataFormat, cipher=self.cipher))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.title = tk.Label(self.subFrame, text="Plaintext", bg=Colours.BACKGROUND, fg=Colours.TITLE_FG, font=Fonts.TITLE)
        self.copyButton = tk.Button(self.subFrame, text="Copy Plaintext", compound="left", image=self.COPY_ICON,
        command=lambda: copyInputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.subFrame2 = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.inputBox = tk.Entry(self.subFrame2, width=24, font=Fonts.TEXT, relief="flat")
        self.inputScrollbar = tk.Scrollbar(self.subFrame2, orient="horizontal", command=self.inputBox.xview)
        self.inputBox['xscrollcommand'] = self.inputScrollbar.set

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame5, text="Encrypt", command=lambda: updateOutputBox(),
            **ButtonStyle.ENCRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame5, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Output frame section"""

        self.outputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame6 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame6, text="Ciphertext", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.copyButton2 = tk.Button(self.subFrame6, text="Copy Ciphertext", compound="left", image=self.COPY_ICON,
        command=lambda: copyOutputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator4 = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.subFrame7 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.outputBox = tk.Text(self.subFrame7, width=25, height=5, bd=0, wrap="word", bg=Colours.BACKGROUND,
            fg=Colours.GREY_FOREGROUND, font=Fonts.TEXT, state="disabled", cursor="X_cursor")
        self.outputScrollbar = tk.Scrollbar(self.subFrame7, command=self.outputBox.yview)
        self.outputBox['yscrollcommand'] = self.outputScrollbar.set

        self.subFrameGuide = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparatorGuide = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.guidelink = tk.Label(self.outputFrame, text="Want to learn how the process is done? Click here!",
            bg=Colours.BACKGROUND, fg=Colours.GUIDE_LINK, cursor="hand2")
        self.guidelink.bind("<Button-1>", lambda e: openguide())

        self.inputFrame.grid(padx=50, sticky="n")
        self.subFrame.grid(sticky="w")
        self.title.grid(padx=16, pady=16)
        self.copyButton.grid(column=1, row=0, padx=5)
        self.horizontalSeparator.grid(sticky="we")
        self.subFrame2.grid(sticky="w")
        self.inputBox.grid(padx=16, pady=10, ipady=10)
        self.inputScrollbar.grid(row=1, column=0, sticky='we', padx=15, pady=(0, 70))

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.outputFrame.grid(column=2, row=0, padx=50, sticky="n")
        self.subFrame6.grid(sticky="w")
        self.title2.grid(padx=16, pady=16)
        self.copyButton2.grid(column=1, row=0, padx=5)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame7.grid(sticky="w")
        self.outputBox.grid(padx=16, pady=25)
        self.outputScrollbar.grid(row=0, column=1, sticky='nsew')
        self.subFrameGuide.grid(sticky="w")

    def messageSectionForTripleDES(self):
        def updateOutputBox():
            """
            Gets the contents of the input and key boxes, then checks them for
            validation, before retrieving the ciphertext from the
            multicrypt module. Lastly, the ciphertext is placed in the output box.
            """

            p = self.inputBox.get()
            k = self.keyBox.get()
            k2 = self.keyBox2.get()

            self.outputBox.delete("1.0", "end")
            self.outputBox.configure(state="disabled", cursor="X_cursor")
            self.error.grid(sticky="w", pady=(5, 0))

            if p == "":
                self.errorMessage.set("The plaintext field is empty.")
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The first key must be at least 8 characters long.")
                return None

            if k2 == "":
                self.errorMessage.set("The second key field is empty.")
                return None

            if len(k2) < 8:
                self.errorMessage.set("The second key must be at least 8 characters long.")
                return None

            self.error.grid_forget()  # Removes the error message
            self.errorMessage.set("")

            self.guide_data, cipherText = multicrypt.encrypt(plaintext=p, passKey=(k, k2), cipher=self.cipher, dataformat=self.dataFormat)

            self.outputBox.configure(state="normal", cursor="xterm")
            self.outputBox.insert("1.0", cipherText)
            self.horizontalSeparatorGuide.grid(sticky="we")
            self.guidelink.grid(sticky="w", pady=(5, 0))

        def copyInputToClipboard():
            i = self.inputBox.get()
            i = i.split("\n")[0]  # The new line character is ommited.
            self.master.clipboard_clear()
            self.master.clipboard_append(i)

        def copyOutputToClipboard():
            o = self.outputBox.get("1.0", "end")
            o = o.split("\n")[0]  # The new line character is ommited.
            self.master.clipboard_clear()
            self.master.clipboard_append(o)

        def openguide():
            # Converts guide data dictionary to url form
            url_data = urllib.parse.urlencode(self.guide_data)

            # Opens default windows browser. Without it, it opens IE.
            url = r"https://localhost/padlock/triple-DES/triple-DES.html?" + (url_data)
            webbrowser.get('windows-default').open_new(url)

        self.errorMessage = tk.StringVar()  # Text variable that stores the different error messages

        self.master = self.winfo_toplevel()  # Gets the top level window

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.title = tk.Label(self.subFrame, text="Plaintext", bg=Colours.BACKGROUND, fg=Colours.TITLE_FG, font=Fonts.TITLE)
        self.copyButton = tk.Button(self.subFrame, text="Copy Plaintext", compound="left", image=self.COPY_ICON,
        command=lambda: copyInputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.subFrame2 = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.inputBox = tk.Entry(self.subFrame2, width=24, font=Fonts.TEXT, relief="flat")
        self.inputScrollbar = tk.Scrollbar(self.subFrame2, orient="horizontal", command=self.inputBox.xview)
        self.inputBox['xscrollcommand'] = self.inputScrollbar.set

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")

        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subtext2 = tk.Label(self.subFrame5, text="SECOND KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE,
            font=Fonts.TITLE2)
        self.keyBox2 = tk.Entry(self.subFrame5, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator4 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame6 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame6, text="Encrypt", command=lambda: updateOutputBox(),
            **ButtonStyle.ENCRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame6, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Output frame section"""

        self.outputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Ciphertext", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.copyButton2 = tk.Button(self.subFrame7, text="Copy Ciphertext", compound="left", image=self.COPY_ICON,
        command=lambda: copyOutputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator5 = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.outputBox = tk.Text(self.subFrame8, width=25, height=10, bd=0, wrap="word", bg=Colours.BACKGROUND,
            fg=Colours.GREY_FOREGROUND, font=Fonts.TEXT, state="disabled", cursor="X_cursor")
        self.outputScrollbar = tk.Scrollbar(self.subFrame8, command=self.outputBox.yview)
        self.outputBox['yscrollcommand'] = self.outputScrollbar.set

        self.subFrameGuide = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparatorGuide = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.guidelink = tk.Label(self.outputFrame, text="Want to learn how the process is done? Click here!",
            bg=Colours.BACKGROUND, fg=Colours.GUIDE_LINK, cursor="hand2")
        self.guidelink.bind("<Button-1>", lambda e: openguide())

        self.inputFrame.grid(padx=50, sticky="n")
        self.subFrame.grid(sticky="w")
        self.title.grid(padx=16, pady=16)
        self.copyButton.grid(column=1, row=0, padx=5)
        self.horizontalSeparator.grid(sticky="we")
        self.subFrame2.grid(sticky="w")
        self.inputBox.grid(padx=16, pady=10, ipady=10)
        self.inputScrollbar.grid(row=1, column=0, sticky='we', padx=15, pady=(0, 155))

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid()
        self.subtext2.grid(sticky="w", pady=(8, 0))
        self.keyBox2.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame6.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.outputFrame.grid(column=2, row=0, padx=50, sticky="n")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=16, pady=16)
        self.copyButton2.grid(column=1, row=0, padx=5)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.outputBox.grid(padx=16, pady=20)
        self.outputScrollbar.grid(row=0, column=1, sticky='nsew')
        self.subFrameGuide.grid(sticky="w")

    def fileSection(self):
        def uploadFile():
            if self.cipherMode == "Base64":
                fileObj = tk.filedialog.askopenfile(title='Choose any file to encrypt', filetypes=[("Select files", "*.*")])
            else:
                fileObj = tk.filedialog.askopenfile(title='Choose a text file to encrypt', filetypes=[("Select files", "*.txt")])

            # An error is thrown if the dialog box is closed without an file chosen
            try:
                self.filepath = os.path.split(fileObj.name)[0]
                self.filename = os.path.basename(fileObj.name)
            except:
                return None

            if os.path.getsize(fileObj.name) > 1000000:
                self.fileInfo.grid(sticky="w", padx=10, pady=(5, 0))
                self.fileInfo.configure(fg="red")
                self.fileInfo_text.set("ERROR: File size too large to upload.")
            else:
                self.fileInfo.grid(sticky="w", padx=10, pady=(5, 0))
                self.fileInfo.configure(fg=Colours.INFO)
                self.fileInfo_text.set("Text File uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(
                    self.filepath, self.filename))

                self.error.grid_forget()
                self.errorMessage.set("")

                self.status.config(fg=Colours.STATUS_WAIT)
                self.statusMessage.set("Awaiting key input")

        def encryptFile():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.config(fg=Colours.STATUS_ERROR)
            k = self.keyBox.get()

            if self.filepath is None:
                self.errorMessage.set("No file uploaded.")
                self.statusMessage.set("File encryption failed!\nCheck ERROR message.")
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("File encryption failed!\nCheck ERROR message.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("File encryption failed!\nCheck ERROR message.")
                return None

            # ONLY for Vigenere Cipher in CLASSIC mode
            if self.cipher == "Vigenere Cipher" and self.cipherMode == "Classic" and not(k.isalpha()):
                self.errorMessage.set("The key must not contain any ASCII characters.")
                self.guidelink.grid_forget()
                return None

            self.error.grid_forget()  # Removes the error message
            self.errorMessage.set("")

            try:
                BLANK, newFilepath = multicrypt.encrypt(filename=self.filename, filepath=self.filepath, passKey=k,
                    cipher=self.cipher, dataformat=self.dataFormat, cipherMode=self.cipherMode)
            except Exception as ex:
                self.statusMessage.set("File encryption failed!")
                self.status.config(fg=Colours.STATUS_ERROR)
                print(ex)
            else:
                self.statusMessage.set("File encrypted successfully!\n\nFilepath: {}".format(newFilepath))
                self.status.config(fg=Colours.STATUS_OK)

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.fileInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()
        self.statusMessage.set('Awaiting file upload.')

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS,
            cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipherMode, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag4 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, pady=(10, 0), padx=10)
        self.sectionTag4.grid(column=5, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))
        self.sectionTag3.bind("<Button-1>", lambda e: self.master.switch_frame(CipherModeMenu, process=self.process,
            dataFormat=self.dataFormat, cipher=self.cipher))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_fileButton = tk.Button(self.subFrame, text="UPLOAD TEXT FILE", compound="left", image=self.IMAGE_UPLOAD,
        command=lambda: uploadFile(), **ButtonStyle.UPLOAD_BUTTON)
        self.fileInfo = tk.Label(self.subFrame, textvariable=self.fileInfo_text, wraplength=300, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame5, text="Encrypt", command=lambda: encryptFile(),
            **ButtonStyle.ENCRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame5, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.STATUS_WAIT, font=Fonts.INFO)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_fileButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16, 50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status.grid(sticky="w", padx=10, pady=(5, 0))

    def fileSectionForTripleDES(self):
        def uploadFile():
            if self.cipherMode == "Base64":
                fileObj = tk.filedialog.askopenfile(title='Choose any file to encrypt', filetypes=[("Select files", "*.*")])
            else:
                fileObj = tk.filedialog.askopenfile(title='Choose a text file to encrypt', filetypes=[("Select files", "*.txt")])

            # An error is thrown if the dialog box is closed without an image chosen
            try:
                self.filepath = os.path.split(fileObj.name)[0]
                self.filename = os.path.basename(fileObj.name)
            except:
                return None

            if os.path.getsize(fileObj.name) > 1000000:
                self.fileInfo.grid(sticky="w", padx=10, pady=(5, 0))
                self.fileInfo.configure(fg="red")
                self.fileInfo_text.set("ERROR: File size too large to upload.")
            else:
                self.fileInfo.grid(sticky="w", padx=10, pady=(5, 0))
                self.fileInfo.configure(fg=Colours.INFO)
                self.fileInfo_text.set("File uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(
                    self.filepath, self.filename))

                self.error.grid_forget()
                self.errorMessage.set("")

                self.status.config(fg=Colours.STATUS_WAIT)
                self.statusMessage.set("Awaiting key inputs")

        def encryptFile():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.config(fg=Colours.STATUS_ERROR)

            k = self.keyBox.get()
            k2 = self.keyBox2.get()

            if self.filepath is None:
                self.errorMessage.set("No file uploaded.")
                self.statusMessage.set("File encryption failed!\nCheck ERROR message.")
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("File encryption failed!\nCheck ERROR message.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("File encryption failed!\nCheck ERROR message.")
                return None

            if k2 == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("File encryption failed!\nCheck ERROR message.")
                return None

            if len(k2) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("File encryption failed!\nCheck ERROR message.")
                return None

            self.error.grid_forget()
            self.errorMessage.set("")

            try:
                BLANK, newFilepath = multicrypt.encrypt(filename=self.filename, filepath=self.filepath,
                    passKey=(k, k2), cipher=self.cipher, dataformat=self.dataFormat, cipherMode=self.cipherMode)
            except Exception as ex:
                self.statusMessage.set("File encryption failed!")
                self.status.config(fg=Colours.STATUS_ERROR)
                print(ex)
            else:
                self.statusMessage.set("File encrypted successfully!\n\nFilepath: {}".format(newFilepath))
                self.status.config(fg=Colours.STATUS_OK)

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.fileInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()
        self.statusMessage.set('Awaiting file upload.')

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS,
            cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipherMode, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag4 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, pady=(10, 0), padx=10)
        self.sectionTag4.grid(column=5, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))
        self.sectionTag3.bind("<Button-1>", lambda e: self.master.switch_frame(CipherModeMenu, process=self.process,
            dataFormat=self.dataFormat, cipher=self.cipher))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_fileButton = tk.Button(self.subFrame, text="UPLOAD TEXT FILE", compound="left", image=self.IMAGE_UPLOAD,
        command=lambda: uploadFile(), **ButtonStyle.UPLOAD_BUTTON)
        self.fileInfo = tk.Label(self.subFrame, textvariable=self.fileInfo_text, wraplength=400, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subtext2 = tk.Label(self.subFrame5, text="SECOND KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE,
            font=Fonts.TITLE2)
        self.keyBox2 = tk.Entry(self.subFrame5, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator4 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame6 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame6, text="Encrypt", command=lambda: encryptFile(),
            **ButtonStyle.ENCRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame6, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.STATUS_WAIT, font=Fonts.INFO)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_fileButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid()
        self.subtext2.grid(sticky="w", pady=(8, 0))
        self.keyBox2.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame6.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16, 50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status.grid(sticky="w", padx=10, pady=(5, 0))

    def imageSection(self):
        def uploadImage():
            self.imgObj = tk.filedialog.askopenfile(title='Choose an image to encrypt', filetypes=[("Select images", "*.jpg *.png")])

            # An error is thrown if the dialog box is closed without an image chosen
            try:
                self.filepath = os.path.split(self.imgObj.name)[0]
                self.filename = os.path.basename(self.imgObj.name)
            except:
                return None

            if os.path.getsize(self.imgObj.name) > 1000000:
                self.imageInfo.grid(sticky="w", padx=10, pady=(5, 0))
                self.imageInfo.configure(fg="red")
                self.imageInfo_text.set("ERROR: File size too large to upload.")
            else:
                self.imageInfo.grid(sticky="w", padx=10, pady=(5, 0))
                self.imageInfo_text.set("Image uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(
                    self.filepath, self.filename))

                self.error.grid_forget()
                self.errorMessage.set("")

                self.status.config(fg=Colours.STATUS_WAIT)
                self.statusMessage.set("Awaiting key input")

        def encryptImage():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.config(fg=Colours.STATUS_ERROR)

            k = self.keyBox.get()

            if self.filepath is None:
                self.errorMessage.set("No file uploaded.")
                self.statusMessage.set("Image encryption failed!\nCheck ERROR message.")
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("Image encryption failed!\nCheck ERROR message.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("Image encryption failed!\nCheck ERROR message.")
                return None

            self.error.grid_forget()
            self.errorMessage.set("")

            try:
                BLANK, newFilepath = multicrypt.encrypt(filename=self.filename, filepath=self.filepath, passKey=k,
                    cipher=self.cipher, dataformat=self.dataFormat)
            except Exception as ex:
                self.statusMessage.set("Image encryption failed!")
                self.status.config(fg=Colours.STATUS_ERROR)
                print(ex)
            else:
                self.statusMessage.set("Image encrypted successfully!\n\nFilepath: {}".format(newFilepath))
                self.status.config(fg=Colours.STATUS_OK)

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.imageInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()
        self.statusMessage.set('Awaiting image upload.')

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS,
            cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_imageButton = tk.Button(self.subFrame, text="UPLOAD IMAGE", compound="left", image=self.IMAGE_UPLOAD,
        command=lambda: uploadImage(), **ButtonStyle.UPLOAD_BUTTON)
        self.imageInfo = tk.Label(self.subFrame, textvariable=self.imageInfo_text, wraplength=400, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame5, text="Encrypt", command=lambda: encryptImage(),
            **ButtonStyle.ENCRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame5, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.STATUS_WAIT, font=Fonts.INFO)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_imageButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16, 50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status.grid(sticky="w", padx=10, pady=(5, 0))

    def imageSectionForTripleDES(self):
        def uploadImage():
            self.imgObj = tk.filedialog.askopenfile(title='Choose an image to encrypt', filetypes=[("Select images", "*.jpg *.png")])

            # An error is thrown if the dialog box is closed without an image chosen
            try:
                self.filepath = os.path.split(self.imgObj.name)[0]
                self.filename = os.path.basename(self.imgObj.name)
            except:
                return None

            if os.path.getsize(self.imgObj.name) > 1000000:
                self.imageInfo.grid(sticky="w", padx=10, pady=(5, 0))
                self.imageInfo.configure(fg="red")
                self.imageInfo_text.set("ERROR: File size too large to upload.")
            else:
                self.imageInfo.grid(sticky="w", padx=10, pady=(5, 0))
                self.imageInfo_text.set("Image uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(
                    self.filepath, self.filename))

                self.error.grid_forget()
                self.errorMessage.set("")

                self.status.config(fg=Colours.STATUS_WAIT)
                self.statusMessage.set("Awaiting key input")

        def encryptImage():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.config(fg=Colours.STATUS_WAIT)
            k = self.keyBox.get()
            k2 = self.keyBox2.get()

            if self.filepath is None:
                self.errorMessage.set("No file uploaded.")
                self.statusMessage.set("Image encryption failed!\nCheck ERROR message.")
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("Image encryption failed!\nCheck ERROR message.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("Image encryption failed!\nCheck ERROR message.")
                return None

            if k2 == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("Image encryption failed!\nCheck ERROR message.")
                return None

            if len(k2) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("Image encryption failed!\nCheck ERROR message.")
                return None

            self.error.grid_forget()
            self.errorMessage.set("")

            start = time.time()
            try:
                BLANK, newFilepath = multicrypt.encrypt(filename=self.filename, filepath=self.filepath,
                    passKey=(k, k2), cipher=self.cipher, dataformat=self.dataFormat)
            except Exception as ex:
                self.statusMessage.set("Image encryption failed!")
                self.status.config(fg=Colours.STATUS_ERROR)
                print(ex)
            else:
                self.statusMessage.set("Image encrypted successfully!\n\nFilepath: {}".format(newFilepath))
                self.status.config(fg=Colours.STATUS_OK)
            end = time.time()
            print(end - start)

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.imageInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()
        self.statusMessage.set('Awaiting image upload.')

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS,
            cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_imageButton = tk.Button(self.subFrame, text="UPLOAD IMAGE", compound="left", image=self.IMAGE_UPLOAD,
        command=lambda: uploadImage(), **ButtonStyle.UPLOAD_BUTTON)
        self.imageInfo = tk.Label(self.subFrame, textvariable=self.imageInfo_text, wraplength=400, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subtext2 = tk.Label(self.subFrame5, text="SECOND KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox2 = tk.Entry(self.subFrame5, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator4 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame6 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame6, text="Encrypt", command=lambda: encryptImage(),
            **ButtonStyle.ENCRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame6, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.STATUS_WAIT, font=Fonts.INFO)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_imageButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid()
        self.subtext2.grid(sticky="w", pady=(8, 0))
        self.keyBox2.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame6.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16, 50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status.grid(sticky="w", padx=10, pady=(5, 0))


class DecryptMenu(tk.Frame):
    """Creates the decryption page frame"""

    def __init__(self, master, process, dataFormat, cipher, cipherMode):
        tk.Frame.__init__(self, master)

        self.process = process
        self.dataFormat = dataFormat
        self.cipher = cipher
        self.cipherMode = cipherMode

        # Initialises the icon used for this frame
        self.icon = Image.open("Images/copyIcon.png")
        self.icon2 = Image.open("Images/imageUpload.png")

        # Makes the icon able to be used by widgets with these references
        self.COPY_ICON = ImageTk.PhotoImage(self.icon)
        self.IMAGE_UPLOAD = ImageTk.PhotoImage(self.icon2)

        self.configure(background=Colours.GREY_BACKGROUND, padx=10, pady=50)

        """
        Calls the necessary functions that create the widgets
        for the corresponding section based on the data format
        """

        if self.dataFormat == "Messages":
            # Triple DES requires a separate section
            if self.cipher == "Triple DES Cipher":
                self.messageSectionForTripleDES()
            else:
                self.messageSection()
        elif self.dataFormat == "Files":
            if self.cipher == "Triple DES Cipher":
                self.fileSectionForTripleDES()
            else:
                self.fileSection()

        elif self.dataFormat == "Images":
            if self.cipher == "Triple DES Cipher":
                self.imageSectionForTripleDES()
            else:
                self.imageSection()

    def messageSection(self):
        def updateOutputBox():
            """
            Gets the contents of the input and key boxes, then checks them for
            validation, before retrieving the plaintext from the
            multicrypt module. Lastly, the plaintext is placed in the output box.
            """

            c = self.inputBox.get()
            k = self.keyBox.get()

            self.outputBox.delete("1.0", "end")
            self.outputBox.configure(state="disabled", cursor="X_cursor")
            self.error.grid(sticky="w", pady=(5, 0))

            if c == "":
                self.errorMessage.set("The ciphertext field is empty.")
                return None
            if k == "":
                self.errorMessage.set("The key field is empty.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                return None

            # ONLY for Vigenere Cipher in CLASSIC mode
            if self.cipher == "Vigenere Cipher" and self.cipherMode == "Classic" and not(k.isalpha()):
                self.errorMessage.set("The key must not contain any ASCII characters.")
                self.guidelink.grid_forget()
                return None

            self.error.grid_forget()  # Removes the error message
            self.errorMessage.set("")

            try:
                self.guide_data, plainText = multicrypt.decrypt(ciphertext=c, passKey=k, cipher=self.cipher,
                    dataformat=self.dataFormat, cipherMode=self.cipherMode)
            except Exception as exc:
                print(exc)
                self.outputBox.configure(state="normal", cursor="xterm", fg="red")
                self.outputBox.insert("1.0", "ERROR: Decryption failed.")
                self.outputBox.configure(state="disabled", cursor="X_cursor", fg="red")
                self.copyButton2.configure(state="disabled", bg="grey", fg="#FFF")
            else:
                self.outputBox.configure(state="normal", cursor="xterm")
                self.outputBox.insert("1.0", plainText)
                self.horizontalSeparatorGuide.grid(sticky="we")
                self.guidelink.grid(sticky="w", pady=(5, 0))

        def copyInputToClipboard():
            i = self.inputBox.get()
            i = i.split("\n")[0]  # The new line character is ommited.
            self.master.clipboard_clear()
            self.master.clipboard_append(i)

        def copyOutputToClipboard():
            o = self.outputBox.get("1.0", "end")
            o = o.split("\n")[0]  # The new line character is ommited.
            self.master.clipboard_clear()
            self.master.clipboard_append(o)

        def openguide():
            # Converts guide data dictionary to url form
            url_data = urllib.parse.urlencode(self.guide_data)

            # Opens default windows browser. Without it, it opens IE.
            if self.cipher == "Caesar Cipher":
                if self.cipherMode == "ASCII":
                    url = r"http://localhost/padlock/caesar/caesar_ASCII.html?" + (url_data)
                else:
                    url = r"http://localhost/padlock/caesar/caesar_classic.html?" + (url_data)

            elif self.cipher == "Vigenere Cipher":
                if self.cipherMode == "ASCII":
                    url = r"http://localhost/padlock/vigenere/vigenere_ASCII.html?" + (url_data)
                else:
                    url = r"http://localhost/padlock/vigenere/vigenere_classic.html?" + (url_data)

            elif self.cipher == "DES Cipher":
                url = r"http://localhost/padlock/DES/DES.html?" + (url_data)

            webbrowser.get('windows-default').open_new(url)

        self.errorMessage = tk.StringVar()  # Text variable that stores the different error messages

        self.master = self.winfo_toplevel()  # Gets the top level window

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS,
            cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipherMode, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag4 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)

        # DES cipher has no modes so this won't display the mode tag
        if self.cipher == "DES Cipher":
            self.sectionTag4.grid(column=5, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)
        else:
            self.sectionTag3.grid(column=4, row=0, pady=(10, 0), padx=10)
            self.sectionTag4.grid(column=5, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))
        self.sectionTag3.bind("<Button-1>", lambda e: self.master.switch_frame(CipherModeMenu, process=self.process,
            dataFormat=self.dataFormat, cipher=self.cipher))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.title = tk.Label(self.subFrame, text="Ciphertext", bg=Colours.BACKGROUND, fg=Colours.TITLE_FG, font=Fonts.TITLE)
        self.copyButton = tk.Button(self.subFrame, text="Copy Ciphertext", compound="left", image=self.COPY_ICON,
        command=lambda: copyInputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.subFrame2 = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.inputBox = tk.Entry(self.subFrame2, width=24, font=Fonts.TEXT, relief="flat")
        self.inputScrollbar = tk.Scrollbar(self.subFrame2, orient="horizontal", command=self.inputBox.xview)
        self.inputBox['xscrollcommand'] = self.inputScrollbar.set

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)

        self.encryptButton = tk.Button(self.subFrame5, text="Decrypt", command=lambda: updateOutputBox(),
            **ButtonStyle.DECRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame5, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Output frame section"""

        self.outputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame6 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame6, text="Plaintext", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.copyButton2 = tk.Button(self.subFrame6, text="Copy Plaintext", compound="left", image=self.COPY_ICON,
        command=lambda: copyOutputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator4 = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.subFrame7 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.outputBox = tk.Text(self.subFrame7, width=26, height=5, bd=0, wrap="word", bg=Colours.BACKGROUND,
            fg=Colours.GREY_FOREGROUND, font=Fonts.TEXT, state="disabled", cursor="X_cursor")
        self.outputScrollbar = tk.Scrollbar(self.subFrame7, command=self.outputBox.yview)
        self.outputBox['yscrollcommand'] = self.outputScrollbar.set

        self.subFrameGuide = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparatorGuide = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.guidelink = tk.Label(self.outputFrame, text="Want to learn how the process is done? Click here!",
            bg=Colours.BACKGROUND, fg=Colours.GUIDE_LINK, cursor="hand2")
        self.guidelink.bind("<Button-1>", lambda e: openguide())

        self.inputFrame.grid(padx=45, sticky="n")
        self.subFrame.grid(sticky="w")
        self.title.grid(padx=16, pady=16)
        self.copyButton.grid(column=1, row=0, padx=5)
        self.horizontalSeparator.grid(sticky="we")
        self.subFrame2.grid(sticky="w")
        self.inputBox.grid(padx=16, pady=10, ipady=10)
        self.inputScrollbar.grid(row=1, column=0, sticky='we', padx=15, pady=(0, 70))

        self.controlFrame.grid(column=1, row=0, padx=45, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", padx=8, pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.outputFrame.grid(column=2, row=0, padx=45, sticky="n")
        self.subFrame6.grid(sticky="w")
        self.title2.grid(padx=(16, 50), pady=16)
        self.copyButton2.grid(column=1, row=0, padx=5)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame7.grid(sticky="w")
        self.outputBox.grid(padx=16, pady=16)
        self.outputScrollbar.grid(row=0, column=1, sticky='nsew')
        self.subFrameGuide.grid(sticky="w")

    def messageSectionForTripleDES(self):
        def updateOutputBox():
            """
            Gets the contents of the input and key boxes, then checks them for
            validation, before retrieving the plaintext from the
            multicrypt module. Lastly, the plaintext is placed in the output box
            """

            c = self.inputBox.get()
            k = self.keyBox.get()
            k2 = self.keyBox2.get()

            self.outputBox.delete("1.0", "end")
            self.outputBox.configure(state="disabled", cursor="X_cursor")
            self.error.grid(sticky="w", pady=(5, 0))

            if c == "":
                self.errorMessage.set("The ciphertext field is empty.")
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The first key must be at least 8 characters long.")
                return None

            if k2 == "":
                self.errorMessage.set("The second key field is empty.")
                return None

            if len(k2) < 8:
                self.errorMessage.set("The second key must be at least 8 characters long.")
                return None

            self.error.grid_forget()  # Removes the error message
            self.errorMessage.set("")

            try:
                self.guide_data, plainText = multicrypt.decrypt(ciphertext=c, passKey=(k, k2), cipher=self.cipher,
                    dataformat=self.dataFormat)
            except Exception as exc:
                print(exc)
                self.outputBox.configure(state="normal", cursor="xterm", fg="red")
                self.outputBox.insert("1.0", "ERROR: Decryption failed.")
                self.outputBox.configure(state="disabled", cursor="X_cursor", fg="red")
                self.copyButton2.configure(state="disabled", bg="grey", fg="#FFF")
            else:
                self.outputBox.configure(state="normal", cursor="xterm")
                self.outputBox.insert("1.0", plainText)
                self.horizontalSeparatorGuide.grid(sticky="we")
                self.guidelink.grid(sticky="w", pady=(5, 0))

        def copyInputToClipboard():
            i = self.inputBox.get()
            i = i.split("\n")[0]  # The new line character is ommited.
            self.master.clipboard_clear()
            self.master.clipboard_append(i)

        def copyOutputToClipboard():
            o = self.outputBox.get("1.0", "end")
            o = o.split("\n")[0]  # The new line character is ommited.
            self.master.clipboard_clear()
            self.master.clipboard_append(o)

        def openguide():
            # Converts guide data dictionary to url form
            url_data = urllib.parse.urlencode(self.guide_data)

            # Opens default windows browser. Without it, it opens IE.
            url = r"http://localhost/padlock/triple-DES/triple-DES.html?" + (url_data)
            webbrowser.get('windows-default').open_new(url)

        self.errorMessage = tk.StringVar()  # Text variable that stores the different error messages

        self.master = self.winfo_toplevel()  # Gets the top level window

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS,
            cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipherMode, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag4 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, pady=(10, 0), padx=10)
        self.sectionTag4.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.title = tk.Label(self.subFrame, text="Ciphertext", bg=Colours.BACKGROUND, fg=Colours.TITLE_FG, font=Fonts.TITLE)
        self.copyButton = tk.Button(self.subFrame, text="Copy Ciphertext", compound="left", image=self.COPY_ICON,
        command=lambda: copyInputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.subFrame2 = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.inputBox = tk.Entry(self.subFrame2, width=24, font=Fonts.TEXT, relief="flat")
        self.inputScrollbar = tk.Scrollbar(self.subFrame2, orient="horizontal", command=self.inputBox.xview)
        self.inputBox['xscrollcommand'] = self.inputScrollbar.set

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subtext2 = tk.Label(self.subFrame5, text="SECOND KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox2 = tk.Entry(self.subFrame5, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator4 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame6 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)

        self.encryptButton = tk.Button(self.subFrame6, text="Decrypt", command=lambda: updateOutputBox(),
            **ButtonStyle.DECRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame6, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Output frame section"""

        self.outputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Plaintext", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.copyButton2 = tk.Button(self.subFrame7, text="Copy Plaintext", compound="left", image=self.COPY_ICON,
        command=lambda: copyOutputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator5 = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.outputBox = tk.Text(self.subFrame8, width=26, height=10, bd=0, wrap="word", bg=Colours.BACKGROUND,
            fg=Colours.GREY_FOREGROUND, font=Fonts.TEXT, state="disabled", cursor="X_cursor")
        self.outputScrollbar = tk.Scrollbar(self.subFrame8, command=self.outputBox.yview)
        self.outputBox['yscrollcommand'] = self.outputScrollbar.set

        self.subFrameGuide = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparatorGuide = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.guidelink = tk.Label(self.outputFrame, text="Want to learn how the process is done? Click here!",
            bg=Colours.BACKGROUND, fg=Colours.GUIDE_LINK, cursor="hand2")
        self.guidelink.bind("<Button-1>", lambda e: openguide())

        self.inputFrame.grid(padx=50, sticky="n")
        self.subFrame.grid(sticky="w")
        self.title.grid(padx=16, pady=16)
        self.copyButton.grid(column=1, row=0, padx=5)
        self.horizontalSeparator.grid(sticky="we")
        self.subFrame2.grid(sticky="w")
        self.inputBox.grid(padx=16, pady=10, ipady=10)
        self.inputScrollbar.grid(row=1, column=0, sticky='we', padx=15, pady=(0, 155))

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid()
        self.subtext2.grid(sticky="w", pady=(8, 0))
        self.keyBox2.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame6.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.outputFrame.grid(column=2, row=0, padx=50, sticky="n")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16, 50), pady=16)
        self.copyButton2.grid(column=1, row=0, padx=5)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.outputBox.grid(padx=16, pady=20)
        self.outputScrollbar.grid(row=0, column=1, sticky='nsew')
        self.subFrameGuide.grid(sticky="w")

    def fileSection(self):
        def uploadFile():
            if self.cipherMode == "Base64":
                fileObj = tk.filedialog.askopenfile(title='Choose any file to decrypt', filetypes=[("Select files", "*.*")])
            else:
                fileObj = tk.filedialog.askopenfile(title='Choose a text file to decrypt', filetypes=[("Select files", "*.txt")])

            # An error is thrown if the dialog box is closed without an image chosen
            try:
                self.filepath = os.path.split(fileObj.name)[0]
                self.filename = os.path.basename(fileObj.name)
            except:
                return None

            self.fileInfo.grid(sticky="w", padx=10, pady=(5, 0))
            self.fileInfo.configure(fg=Colours.INFO)
            self.fileInfo_text.set("File uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(
                self.filepath, self.filename))

            self.error.grid_forget()
            self.errorMessage.set("")

            self.status.config(fg=Colours.STATUS_WAIT)
            self.statusMessage.set("Awaiting key input.")

        def decryptFile():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.config(fg=Colours.STATUS_ERROR)
            k = self.keyBox.get()

            if self.filepath is None:
                self.errorMessage.set("No file uploaded.")
                self.statusMessage.set("File decryption failed!\nCheck ERROR message.")
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("File decryption failed!\nCheck ERROR message.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("File decryption failed!\nCheck ERROR message.")
                return None

            # ONLY for Vigenere Cipher in CLASSIC mode
            if self.cipher == "Vigenere Cipher" and self.cipherMode == "Classic" and not(k.isalpha()):
                self.errorMessage.set("The key must not contain any ASCII characters.")
                self.guidelink.grid_forget()
                return None

            self.error.grid_forget()  # Removes the error message
            self.errorMessage.set("")

            try:
                BLANK, newFilepath = multicrypt.decrypt(filename=self.filename, filepath=self.filepath, passKey=k,
                    cipher=self.cipher, dataformat=self.dataFormat, cipherMode=self.cipherMode)
            except Exception as ex:
                self.statusMessage.set("File decryption failed!")
                self.status.config(fg=Colours.STATUS_ERROR)
                print(ex)
            else:
                self.statusMessage.set("File decrypted successfully!\n\nFilepath: {}".format(newFilepath))
                self.status.config(fg=Colours.STATUS_OK)

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.fileInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()
        self.statusMessage.set('Awaiting file upload.')

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS,
            cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipherMode, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag4 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, pady=(10, 0), padx=10)
        self.sectionTag4.grid(column=5, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # add_cascade an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))
        self.sectionTag3.bind("<Button-1>", lambda e: self.master.switch_frame(CipherModeMenu, process=self.process,
            dataFormat=self.dataFormat, cipher=self.cipher))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_fileButton = tk.Button(self.subFrame, text="UPLOAD TEXT FILE", compound="left", image=self.IMAGE_UPLOAD,
        command=lambda: uploadFile(), **ButtonStyle.UPLOAD_BUTTON)
        self.fileInfo = tk.Label(self.subFrame, textvariable=self.fileInfo_text, wraplength=400, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame5, text="Decrypt", command=lambda: decryptFile(),
            **ButtonStyle.ENCRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame5, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.STATUS_WAIT, font=Fonts.INFO)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_fileButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16, 50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status.grid(sticky="w", padx=10, pady=(5, 0))

    def fileSectionForTripleDES(self):
        def uploadFile():
            if self.cipherMode == "Base64":
                fileObj = tk.filedialog.askopenfile(title='Choose any file to decrypt', filetypes=[("Select files", "*.*")])
            else:
                fileObj = tk.filedialog.askopenfile(title='Choose a text file to decrypt', filetypes=[("Select files", "*.txt")])

            # An error is thrown if the dialog box is closed without an file chosen
            try:
                self.filepath = os.path.split(fileObj.name)[0]
                self.filename = os.path.basename(fileObj.name)
            except:
                return None

            self.fileInfo.grid(sticky="w", padx=10, pady=(5, 0))
            self.fileInfo.configure(fg=Colours.INFO)
            self.fileInfo_text.set("File uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(
                self.filepath, self.filename))

            self.error.grid_forget()
            self.errorMessage.set("")

            self.status.config(fg=Colours.STATUS_WAIT)
            self.statusMessage.set("Awaiting key inputs.")

        def decryptFile():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.config(fg=Colours.STATUS_ERROR)

            k = self.keyBox.get()
            k2 = self.keyBox2.get()

            if self.filepath is None:
                self.errorMessage.set("No file uploaded.")
                self.statusMessage.set("File decryption failed!\nCheck ERROR message.")
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("File decryption failed!\nCheck ERROR message.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("File decryption failed!\nCheck ERROR message.")
                return None

            if k2 == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("File decryption failed!\nCheck ERROR message.")
                return None

            if len(k2) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("File decryption failed!\nCheck ERROR message.")
                return None

            self.error.grid_forget()
            self.errorMessage.set("")

            try:
                BLANK, newFilepath = multicrypt.decrypt(filename=self.filename, filepath=self.filepath,
                    passKey=(k, k2), cipher=self.cipher, dataformat=self.dataFormat, cipherMode=self.cipherMode)
            except Exception as ex:
                self.statusMessage.set("File decryption failed!")
                self.status.config(fg=Colours.STATUS_ERROR)
                print(ex)
            else:
                self.statusMessage.set("File decrypted successfully!\n\nFilepath: {}".format(newFilepath))
                self.status.config(fg=Colours.STATUS_OK)

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.fileInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()
        self.statusMessage.set('Awaiting file upload.')

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS,
            cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipherMode, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag4 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, pady=(10, 0), padx=10)
        self.sectionTag4.grid(column=5, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))
        self.sectionTag3.bind("<Button-1>", lambda e: self.master.switch_frame(CipherModeMenu, process=self.process,
            dataFormat=self.dataFormat, cipher=self.cipher))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_fileButton = tk.Button(self.subFrame, text="UPLOAD TEXT FILE", compound="left", image=self.IMAGE_UPLOAD,
        command=lambda: uploadFile(), **ButtonStyle.UPLOAD_BUTTON)
        self.fileInfo = tk.Label(self.subFrame, textvariable=self.fileInfo_text, wraplength=400, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subtext2 = tk.Label(self.subFrame5, text="SECOND KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox2 = tk.Entry(self.subFrame5, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator4 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame6 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame6, text="Decrypt", command=lambda: decryptFile(),
            **ButtonStyle.ENCRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame6, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.STATUS_WAIT, font=Fonts.INFO)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_fileButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid()
        self.subtext2.grid(sticky="w", pady=(8, 0))
        self.keyBox2.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame6.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16, 50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status.grid(sticky="w", padx=10, pady=(5, 0))

    def imageSection(self):
        def uploadImage():
            self.imgObj = tk.filedialog.askopenfile(title='Choose an image to decrypt', filetypes=[("Select images", "*.jpg *.png")])

            # An error is thrown if the dialog box is closed without an image chosen
            try:
                self.filepath = os.path.split(self.imgObj.name)[0]
                self.filename = os.path.basename(self.imgObj.name)
            except:
                return None

            self.imageInfo.grid(sticky="w", padx=10, pady=(5, 0))
            self.imageInfo_text.set("Image uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(
                self.filepath, self.filename))

            self.error.grid_forget()
            self.errorMessage.set("")

            self.status.config(fg=Colours.STATUS_WAIT)
            self.statusMessage.set("Awaiting key input")

        def decryptImage():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.config(fg=Colours.STATUS_ERROR)
            k = self.keyBox.get()

            if self.filepath is None:
                self.errorMessage.set("No file uploaded.")
                self.statusMessage.set("Image decryption failed!\nCheck ERROR message.")
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("Image decryption failed!\nCheck ERROR message.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("Image decryption failed!\nCheck ERROR message.")
                return None

            self.error.grid_forget()
            self.errorMessage.set("")

            try:
                BLANK, newFilepath = multicrypt.decrypt(filename=self.filename, filepath=self.filepath,
                    passKey=k, cipher=self.cipher, dataformat=self.dataFormat)
            except Exception as ex:
                self.statusMessage.set("Image decryption failed!")
                self.status.config(fg=Colours.STATUS_ERROR)
                print(ex)
            else:
                self.statusMessage.set("Image decrypted successfully!\n\nFilepath: {}".format(newFilepath))
                self.status.config(fg=Colours.STATUS_OK)

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.imageInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()
        self.statusMessage.set('Awaiting image upload.')

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS,
            cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipherMode, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag4 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, pady=(10, 0), padx=10)
        self.sectionTag4.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_imageButton = tk.Button(self.subFrame, text="UPLOAD IMAGE", compound="left", image=self.IMAGE_UPLOAD,
            command=lambda: uploadImage(), **ButtonStyle.UPLOAD_BUTTON)
        self.imageInfo = tk.Label(self.subFrame, textvariable=self.imageInfo_text, wraplength=400, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame5, text="Decrypt", command=lambda: decryptImage(),
            **ButtonStyle.ENCRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame5, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.STATUS_WAIT, font=Fonts.INFO)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_imageButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16, 50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status.grid(sticky="w", padx=10, pady=(5, 0))

    def imageSectionForTripleDES(self):
        def uploadImage():
            self.imgObj = tk.filedialog.askopenfile(title='Choose an image to decrypt', filetypes=[("Select images", "*.jpg *.png")])
            # An error is thrown if the dialog box is closed without an image chosen
            try:
                self.filepath = os.path.split(self.imgObj.name)[0]
                self.filename = os.path.basename(self.imgObj.name)
            except:
                return None

            self.imageInfo.grid(sticky="w", padx=10, pady=(5, 0))
            self.imageInfo_text.set("Image uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(
                self.filepath, self.filename))

            self.error.grid_forget()
            self.errorMessage.set("")

            self.status.config(fg=Colours.STATUS_WAIT)
            self.statusMessage.set("Awaiting key input")

        def decryptImage():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.config(fg=Colours.STATUS_ERROR)
            k = self.keyBox.get()
            k2 = self.keyBox2.get()

            if self.filepath is None:
                self.errorMessage.set("No file uploaded.")
                self.statusMessage.set("Image decryption failed!\nCheck ERROR message.")
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("Image decryption failed!\nCheck ERROR message.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("Image decryption failed!\nCheck ERROR message.")
                return None

            if k2 == "":
                self.errorMessage.set("The key field is empty.")
                self.statusMessage.set("Image decryption failed!\nCheck ERROR message.")
                return None

            if len(k2) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                self.statusMessage.set("Image decryption failed!\nCheck ERROR message.")
                return None

            self.error.grid_forget()
            self.errorMessage.set("")

            start = time.time()
            try:
                BLANK, newFilepath = multicrypt.decrypt(filename=self.filename, filepath=self.filepath,
                    passKey=(k, k2), cipher=self.cipher, dataformat=self.dataFormat)
            except Exception as ex:
                self.statusMessage.set("Image decryption failed!")
                self.status.config(fg=Colours.STATUS_ERROR)
                print(ex)
            else:
                self.statusMessage.set("Image decrypted successfully!\n\nFilepath: {}".format(newFilepath))
                self.status.config(fg=Colours.STATUS_OK)

            end = time.time()
            print(end - start)

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.imageInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()
        self.statusMessage.set('Awaiting image upload.')

        """
        Creates a header:
        The header frame is placed in the main application (master frame),
        separate from the current frame.
        """

        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS,
            cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipherMode, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE,
            font=Fonts.TAGS, cursor="hand2")
        self.sectionTag4 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND,
            font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, pady=(10, 0), padx=10)
        self.sectionTag4.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Adds an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process,
            dataFormat=self.dataFormat))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_imageButton = tk.Button(self.subFrame, text="UPLOAD IMAGE", compound="left", image=self.IMAGE_UPLOAD,
        command=lambda: uploadImage(), **ButtonStyle.UPLOAD_BUTTON)
        self.imageInfo = tk.Label(self.subFrame, textvariable=self.imageInfo_text, wraplength=400, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG,
            font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subtext2 = tk.Label(self.subFrame5, text="SECOND KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE,
            font=Fonts.TITLE2)
        self.keyBox2 = tk.Entry(self.subFrame5, width=22, relief="flat", font=Fonts.KEY_TEXT, highlightthickness="1",
            highlightcolor="orange", highlightbackground="grey")
        self.horizontalSeparator4 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame6 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame6, text="Decrypt", command=lambda: decryptImage(),
            **ButtonStyle.ENCRYPT2_BUTTON)
        self.error = tk.Label(self.subFrame6, textvariable=self.errorMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left",
            bg=Colours.BACKGROUND, fg=Colours.STATUS_WAIT, font=Fonts.INFO)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_imageButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid()
        self.subtext2.grid(sticky="w", pady=(8, 0))
        self.keyBox2.grid(padx=10, pady=10, ipady=5)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame6.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16, 50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status.grid(sticky="w", padx=10, pady=(5, 0))


if __name__ == "__main__":
    app = Padlock()
    app.mainloop()
