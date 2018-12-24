#!/usr/bin/env python3

import multicrypt

"""
Padlock Encryption Software
Copyright 2018
Created by: Suraj Kothari
"""

import tkinter as tk
import tkinter.ttk
import tkinter.filedialog
import os
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

        self.configure(background="white")  # Background colour

        """Creates a footer"""
        footer = tk.Frame(self, bg=Colours.SECONDARY)
        copyrightText = tk.Label(footer, text="Padlock Encryption Software | Copyright 2018 - Suraj Kothari", bg=Colours.SECONDARY, fg="white", font=Fonts.SMALL_PRINT)

        footer.grid(row=2, sticky="ew")
        copyrightText.grid()

        """Creates a toplevel menu"""
        menubar = tk.Menu(self)

        # File section of the menubar
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.config(menu=menubar)  # Displays the menu

        self._frame = None  # Clears the current frame

        # Sets the current frame to the home page
        self.switch_frame(HomePage)
        #self.switch_frame(EncryptMenu, process="Encrypt", dataFormat="Images", cipher="Triple DES Cipher")

    def switch_frame(self, frame_class, process=None, dataFormat=None, cipher=None):
        """Destroys current frame and replaces it with a new one."""

        """
        By default pass all extra necessary arguments to all classes,
        even if they don't require it. This removes the need to check
        which class needs individual extra arguments
        """
        new_frame = frame_class(self, process, dataFormat, cipher)

        # Check if the current frame exists, then destroy it
        if self._frame is not None:
            self._frame.destroy()

        self._frame = new_frame

        # Position the individual frames on the first row (above the footer)
        self._frame.grid(row=1, sticky="n")


class HomePage(tk.Frame):
    """Creates the home page frame"""

    def __init__(self, master, process, dataFormat, cipher):
        tk.Frame.__init__(self, master)

        self.configure(background=Colours.BACKGROUND)  # Background colour

        # Initialise the icons used for this frame
        self.icon = Image.open("Images/encryptIcon.png")
        self.icon2 = Image.open("Images/decryptIcon.png")

        # Make the icon able to be used by widgets by these references
        self.ENCRYPT_ICON = ImageTk.PhotoImage(self.icon)
        self.DECRYPT_ICON = ImageTk.PhotoImage(self.icon2)

        self.createWidgets()

    def createWidgets(self):
        self.master = self.winfo_toplevel()  # Gets the top level window

        """Creates a header"""

        # The header frame is placed in the main application (master frame)
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, sticky="ns", ipadx=40, pady=(10, 0))

        # Create the widgets for the home section
        self.encryptButton = tk.Button(self, text="Encrypt", compound="left", image=self.ENCRYPT_ICON,
        command=lambda: self.master.switch_frame(FormatSelctionMenu, process="Encrypt"), **ButtonStyle.ENCRYPT)
        self.verticalSeparator = tk.ttk.Separator(self, orient="vertical")
        self.decryptButton = tk.Button(self, text="Decrypt", compound="left", image=self.DECRYPT_ICON,
        command=lambda: self.master.switch_frame(FormatSelctionMenu, process="Decrypt"), **ButtonStyle.DECRYPT)

        # Keep an extra reference to the image objects
        self.encryptButton.image = self.ENCRYPT_ICON
        self.decryptButton.image = self.DECRYPT_ICON

        # Place the widgets in the grid layout
        self.encryptButton.grid(padx=26)
        self.verticalSeparator.grid(column=1, row=0, rowspan=1, sticky="ns")
        self.decryptButton.grid(column=2, row=0, padx=26)

        # Create hover listeners for the buttons to change colour when hovered
        self.encryptButton.bind("<Enter>", lambda e: self.encryptButton.configure(bg=ButtonStyle.ENCRYPT["activebackground"]))
        self.encryptButton.bind("<Leave>", lambda e: self.encryptButton.configure(bg=ButtonStyle.ENCRYPT["bg"]))
        self.decryptButton.bind("<Enter>", lambda e: self.decryptButton.configure(bg=ButtonStyle.DECRYPT["activebackground"]))
        self.decryptButton.bind("<Leave>", lambda e: self.decryptButton.configure(bg=ButtonStyle.DECRYPT["bg"]))


class FormatSelctionMenu(tk.Frame):
    """Creates the data format selection page frame"""

    def __init__(self, master, process, dataFormat, cipher):
        tk.Frame.__init__(self, master)

        self.process = process

        # Initialise the icons used in this frame
        self.icon = Image.open("Images/messageIcon.png")
        self.icon2 = Image.open("Images/fileIcon.png")
        self.icon3 = Image.open("Images/imageIcon.png")

        # Make the icon able to be used by widgets by these references
        self.MESSAGE_ICON = ImageTk.PhotoImage(self.icon)
        self.FILE_ICON = ImageTk.PhotoImage(self.icon2)
        self.IMAGE_ICON = ImageTk.PhotoImage(self.icon3)

        self.configure(background=Colours.BACKGROUND)  # Background

        self.createWidgets()

    def createWidgets(self):
        self.master = self.winfo_toplevel()  # Gets the top level window

        """Creates a header"""
        # The header frame is placed in the main application (master frame)
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        # Place the widgets in the grid layout
        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, sticky="ns", ipadx=40, padx=10, pady=(10, 0))

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))

        # Create the widgets for the encrypt section
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

        # Place the widgets in the grid layout
        self.messageButton.grid(padx=26)
        self.verticalSeparator.grid(column=1, row=0, rowspan=1, sticky="ns")
        self.fileButton.grid(column=2, row=0, padx=26)
        self.verticalSeparator2.grid(column=3, row=0, rowspan=1, sticky="ns")
        self.imageButton.grid(column=4, row=0, padx=26)

        # Create hover listeners for the buttons to change colour when hovered
        self.messageButton.bind("<Enter>", lambda e: self.messageButton.configure(bg=ButtonStyle.MESSAGE_BUTTON["activebackground"]))
        self.messageButton.bind("<Leave>", lambda e: self.messageButton.configure(bg=ButtonStyle.MESSAGE_BUTTON["bg"]))
        self.fileButton.bind("<Enter>", lambda e: self.fileButton.configure(bg=ButtonStyle.FILE_BUTTON["activebackground"]))
        self.fileButton.bind("<Leave>", lambda e: self.fileButton.configure(bg=ButtonStyle.FILE_BUTTON["bg"]))
        self.imageButton.bind("<Enter>", lambda e: self.imageButton.configure(bg=ButtonStyle.IMAGE_BUTTON["activebackground"]))
        self.imageButton.bind("<Leave>", lambda e: self.imageButton.configure(bg=ButtonStyle.IMAGE_BUTTON["bg"]))


class CipherMenu(tk.Frame):
    """Creates the cipher selection page frame"""
    def __init__(self, master, process, dataFormat, cipher):
        tk.Frame.__init__(self, master)

        self.process = process
        self.dataFormat = dataFormat

        # Background
        self.configure(background=Colours.BACKGROUND)

        self.createWidgets()

    def createWidgets(self):
        # Gets the top level window
        self.master = self.winfo_toplevel()

        # Create a header
        # The header frame is placed in the main application,
        # separate from the current frame
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        # Place the widgets in the grid layout
        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))

        # Create the widgets for the encrypt section
        self.caesarButton = tk.Button(self, text="Caesar",
        command=lambda: self.master.switch_frame(EncryptMenu, process=self.process, dataFormat=self.dataFormat, cipher="Caesar Cipher") if self.process == "Encrypt" else self.master.switch_frame(DecryptMenu, process=self.process, dataFormat=self.dataFormat, cipher="Caesar Cipher"), **ButtonStyle.CAESAR_BUTTON)

        self.vigenereButton = tk.Button(self, text="Vigenere",
        command=lambda: self.master.switch_frame(EncryptMenu, process=self.process, dataFormat=self.dataFormat, cipher="Vigenere Cipher") if self.process == "Encrypt" else self.master.switch_frame(DecryptMenu, process=self.process, dataFormat=self.dataFormat, cipher="Vigenere Cipher"), **ButtonStyle.VIGENERE_BUTTON)

        self.verticalSeparator = tk.ttk.Separator(self, orient="vertical")

        self.DES_Button = tk.Button(self, text="DES",
        command=lambda: self.master.switch_frame(EncryptMenu, process=self.process, dataFormat=self.dataFormat, cipher="DES Cipher") if self.process == "Encrypt" else self.master.switch_frame(DecryptMenu, process=self.process, dataFormat=self.dataFormat, cipher="DES Cipher"), **ButtonStyle.DES_BUTTON)

        self.triple_DES_Button = tk.Button(self, text="Triple DES",
        command=lambda: self.master.switch_frame(EncryptMenu, process=self.process, dataFormat=self.dataFormat, cipher="Triple DES Cipher") if self.process == "Encrypt" else self.master.switch_frame(DecryptMenu, process=self.process, dataFormat=self.dataFormat, cipher="Triple DES Cipher"), **ButtonStyle.TRIPLE_DES_BUTTON)

        # Place the widgets in the grid layout
        self.caesarButton.grid(padx=26, pady=(0, 10))
        self.vigenereButton.grid(padx=26, pady=(10, 0))
        self.verticalSeparator.grid(column=1, row=0, rowspan=2, sticky="ns")
        self.DES_Button.grid(column=2, row=0, padx=26, pady=(0, 10))
        self.triple_DES_Button.grid(column=2, row=1, padx=26, pady=(10, 0))

        # Create hover listeners for the buttons to change colour when hovered
        self.caesarButton.bind("<Enter>", lambda e: self.caesarButton.configure(bg=ButtonStyle.CAESAR_BUTTON["activebackground"]))
        self.caesarButton.bind("<Leave>", lambda e: self.caesarButton.configure(bg=ButtonStyle.CAESAR_BUTTON["bg"]))
        self.vigenereButton.bind("<Enter>", lambda e: self.vigenereButton.configure(bg=ButtonStyle.VIGENERE_BUTTON["activebackground"]))
        self.vigenereButton.bind("<Leave>", lambda e: self.vigenereButton.configure(bg=ButtonStyle.VIGENERE_BUTTON["bg"]))
        self.DES_Button.bind("<Enter>", lambda e: self.DES_Button.configure(bg=ButtonStyle.DES_BUTTON["activebackground"]))
        self.DES_Button.bind("<Leave>", lambda e: self.DES_Button.configure(bg=ButtonStyle.DES_BUTTON["bg"]))
        self.triple_DES_Button.bind("<Enter>", lambda e: self.triple_DES_Button.configure(bg=ButtonStyle.TRIPLE_DES_BUTTON["activebackground"]))
        self.triple_DES_Button.bind("<Leave>", lambda e: self.triple_DES_Button.configure(bg=ButtonStyle.TRIPLE_DES_BUTTON["bg"]))


class EncryptMenu(tk.Frame):
    """Creates the encryption page frame"""

    def __init__(self, master, process, dataFormat, cipher):
        tk.Frame.__init__(self, master)

        self.process = process
        self.dataFormat = dataFormat
        self.cipher = cipher

        self.configure(background=Colours.GREY_BACKGROUND, padx=10, pady=50)

        # Initialise the icon used for this frame
        self.icon = Image.open("Images/copyIcon.png")
        self.icon2 = Image.open("Images/imageUpload.png")

        # Make the icon able to be used by widgets by these references
        self.COPY_ICON = ImageTk.PhotoImage(self.icon)
        self.IMAGE_UPLOAD = ImageTk.PhotoImage(self.icon2)

        # Call the necessary function that creates the widgets
        # for the releveant section based on the data format
        if self.dataFormat == "Messages":
            # Triple DES requires a separate section
            if self.cipher == "Triple DES Cipher":
                self.messageSectionForTripleDES()
            else:
                self.messageSection()
        elif self.dataFormat == "Files":
            self.fileSection()
        elif self.dataFormat == "Images":
            if self.cipher == "Triple DES Cipher":
                self.imageSectionForTripleDES()
            else:
                self.imageSection()

    def messageSection(self):
        def updateOutputBox():
            p = self.inputBox.get()
            k = self.keyBox.get()
            self.outputBox.delete("1.0", "end")
            self.error.grid(sticky="w", pady=(5, 0))

            if p == "":
                self.errorMessage.set("The plaintext field is empty.")
                return None
            if k == "":
                self.errorMessage.set("The key field is empty.")
                return None
            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                return None

            self.error.grid_forget()
            self.errorMessage.set("")

            cipherText = multicrypt.encrypt(plaintext=p, passKey=k, cipher=self.cipher, dataformat=self.dataFormat)
            self.outputBox.insert("1.0", cipherText)

        def copyInputToClipboard():
            i = self.inputBox.get()
            # The new line character must be ommited.
            i = i.split("\n")[0]
            self.master.clipboard_clear()
            self.master.clipboard_append(i)

        def copyOutputToClipboard():
            o = self.outputBox.get("1.0", "end")
            # The new line character must be ommited.
            o = o.split("\n")[0]
            self.master.clipboard_clear()
            self.master.clipboard_append(o)

        self.errorMessage = tk.StringVar()  # Text variable that stores the different error messages

        self.master = self.winfo_toplevel()  # Gets the top level window

        """Creates a header"""

        # The header frame is placed in the main application,
        # separate from the current frame
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        # Place the widgets in the grid layout
        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process, dataFormat=self.dataFormat))

        # Create the widgets for the encrypt section

        # Input frame section
        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.title = tk.Label(self.subFrame, text="Plaintext", bg=Colours.BACKGROUND, fg=Colours.TITLE_FG, font=Fonts.TITLE)
        self.copyButton = tk.Button(self.subFrame, text="Copy Plaintext", compound="left", image=self.COPY_ICON,
        command=lambda: copyInputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.subFrame2 = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.inputBox = tk.Entry(self.subFrame2, width=20, font=Fonts.TEXT, relief="flat")

        # Control frame section
        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG, font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=20, relief="flat", font=Fonts.KEY_TEXT)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame5, text="Encrypt", command=lambda: updateOutputBox(), **ButtonStyle.ENCRYPT2)
        self.error = tk.Label(self.subFrame5, textvariable=self.errorMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        # Output frame section
        self.outputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame6 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame6, text="Ciphertext", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.copyButton2 = tk.Button(self.subFrame6, text="Copy Ciphertext", compound="left", image=self.COPY_ICON,
        command=lambda: copyOutputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator4 = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.subFrame7 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.outputBox = tk.Text(self.subFrame7, width=20, height=5, bd=0, wrap="word", bg=Colours.BACKGROUND, fg=Colours.GREY_FOREGROUND, font=Fonts.TEXT)

        # Place the widgets in the grid layout
        self.inputFrame.grid(padx=50, sticky="n")
        self.subFrame.grid(sticky="w")
        self.title.grid(padx=16, pady=16)
        self.copyButton.grid(column=1, row=0, padx=5)
        self.horizontalSeparator.grid(sticky="we")
        self.subFrame2.grid(sticky="w")
        self.inputBox.grid(padx=16, ipady=16, pady=(0, 90))

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, ipady=10)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.outputFrame.grid(column=2, row=0, padx=50, sticky="n")
        self.subFrame6.grid(sticky="w")
        self.title2.grid(padx=16, pady=16)
        self.copyButton2.grid(column=1, row=0, padx=5)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame7.grid(sticky="w")
        self.outputBox.grid(padx=16, pady=16)

    def messageSectionForTripleDES(self):
        def updateOutputBox():
            p = self.inputBox.get()
            k = self.keyBox.get()
            k2 = self.keyBox2.get()

            self.outputBox.delete("1.0", "end")
            self.error.grid(sticky="w", pady=(5, 0))

            if p == "":
                self.errorMessage.set("The plaintext field is empty.")
                return None

            if k == "":
                self.errorMessage.set("The key field is empty.")
                return None

            if len(k) < 8:
                self.errorMessage.set("The key must be at least 8 characters long.")
                return None

            if k2 == "":
                self.errorMessage.set("The second key field is empty.")
                return None

            if len(k2) < 8:
                self.errorMessage.set("The second key must be at least 8 characters long.")
                return None

            self.error.grid_forget()  # Remove the error message
            self.errorMessage.set("")


            cipherText = multicrypt.encrypt(plaintext=p, passKey=(k, k2), cipher=self.cipher, dataformat=self.dataFormat)

            self.outputBox.insert("1.0", cipherText)

        def copyInputToClipboard():
            i = self.inputBox.get()
            # The new line character must be ommited.
            i = i.split("\n")[0]
            self.master.clipboard_clear()
            self.master.clipboard_append(i)

        def copyOutputToClipboard():
            o = self.outputBox.get("1.0", "end")
            # The new line character must be ommited.
            o = o.split("\n")[0]
            self.master.clipboard_clear()
            self.master.clipboard_append(o)

        self.errorMessage = tk.StringVar()

        # Gets the top level window
        self.master = self.winfo_toplevel()

        # Create a header
        # The header frame is placed in the main application,
        # separate from the current frame
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        # Place the widgets in the grid layout
        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process, dataFormat=self.dataFormat))

        # Creates the widgets for the encrypt section

        # Input frame section
        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.title = tk.Label(self.subFrame, text="Plaintext", bg=Colours.BACKGROUND, fg=Colours.TITLE_FG, font=Fonts.TITLE)
        self.copyButton = tk.Button(self.subFrame, text="Copy Plaintext", compound="left", image=self.COPY_ICON,
        command=lambda: copyInputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.subFrame2 = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.inputBox = tk.Entry(self.subFrame2, width=20, font=Fonts.TEXT, relief="flat")

        # Control frame section
        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG, font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=20, relief="flat", font=Fonts.KEY_TEXT)

        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subtext2 = tk.Label(self.subFrame5, text="SECOND KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox2 = tk.Entry(self.subFrame5, width=20, relief="flat", font=Fonts.KEY_TEXT)
        self.horizontalSeparator4 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame6 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame6, text="Encrypt", command=lambda: updateOutputBox(), **ButtonStyle.ENCRYPT2)
        self.error = tk.Label(self.subFrame6, textvariable=self.errorMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        # Output frame section
        self.outputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Ciphertext", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.copyButton2 = tk.Button(self.subFrame7, text="Copy Ciphertext", compound="left", image=self.COPY_ICON,
        command=lambda: copyOutputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator5 = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.outputBox = tk.Text(self.subFrame8, width=20, height=10, bd=0, wrap="word", bg=Colours.BACKGROUND, fg=Colours.GREY_FOREGROUND, font=Fonts.TEXT)

        # Places the widgets in the grid layout
        self.inputFrame.grid(padx=50, sticky="n")
        self.subFrame.grid(sticky="w")
        self.title.grid(padx=16, pady=16)
        self.copyButton.grid(column=1, row=0, padx=5)
        self.horizontalSeparator.grid(sticky="we")
        self.subFrame2.grid(sticky="w")
        self.inputBox.grid(padx=16, ipady=16, pady=(0, 155))

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, ipady=10)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid()
        self.subtext2.grid(sticky="w", pady=(8, 0))
        self.keyBox2.grid(padx=10, ipady=10)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame6.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.outputFrame.grid(column=2, row=0, padx=50, sticky="n")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=16, pady=16)
        self.copyButton2.grid(column=1, row=0, padx=5)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.outputBox.grid(padx=16, pady=16)


    def fileSection(self):
        # Gets the top level window
        self.master = self.winfo_toplevel()

        # Create a header
        # The header frame is placed in the main application,
        # separate from the current frame
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        # Place the widgets in the grid layout
        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process, dataFormat=self.dataFormat))

        # Create the widgets for the encrypt section
        self.t = tk.Label(self, text=self.cipher)
        self.t2 = tk.Label(self, text="Plaintext")
        self.t3 = tk.Label(self, text="Files")

        # Place the widgets in the grid layout
        self.t.grid(padx=26, pady=(0, 10))
        self.t2.grid(padx=26, pady=(0, 10))
        self.t3.grid(padx=26, pady=(0, 10))


    def imageSection(self):
        def uploadImage():
            fileObj = tk.filedialog.askopenfile(title='Choose an image to encrypt', filetypes=[("Select images", "*.jpg *.png")])

            # An error is thrown if the dialog box is closed without an image chosen
            try:
                self.filepath = os.path.split(fileObj.name)[0]
                self.filename = os.path.basename(fileObj.name)
            except:
                return None

            self.imageInfo.grid(sticky="w", padx=10, pady=(5, 0))
            self.imageInfo_text.set("Image uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(self.filepath, self.filename))

            self.error.grid_forget()
            self.errorMessage.set("")

            self.status.grid_forget()
            self.statusMessage.set("")

        def encryptImage():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.grid(sticky="w", padx=10, pady=(5, 0))
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
                newFilepath = multicrypt.encrypt(filename=self.filename, filepath=self.filepath, passKey=k, cipher=self.cipher, dataformat=self.dataFormat)
            except:
                self.statusMessage.set("Image encryption failed!")
            else:
                self.statusMessage.set("Image encrypted successfully!\n\nFilepath: {}".format(newFilepath))

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.imageInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()

        """Creates a header"""

        # The header frame is placed in the main application
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process, dataFormat=self.dataFormat))


        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_imageButton = tk.Button(self.subFrame, text="UPLOAD IMAGE", compound="left", image=self.IMAGE_UPLOAD,
        command=lambda: uploadImage(), **ButtonStyle.UPLOAD_BUTTON)
        self.imageInfo = tk.Label(self.subFrame, textvariable=self.imageInfo_text, wraplength=400, justify="left", bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG, font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=20, relief="flat", font=Fonts.KEY_TEXT)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame5, text="Encrypt", command=lambda: encryptImage(), **ButtonStyle.ENCRYPT2)
        self.error = tk.Label(self.subFrame5, textvariable=self.errorMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_imageButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, ipady=10)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16,50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.STATUS, font=Fonts.INFO)

    def imageSectionForTripleDES(self):
        def uploadImage():
            fileObj = tk.filedialog.askopenfile(title='Choose an image to encrypt', filetypes=[("Select images", "*.jpg *.png")])

            # An error is thrown if the dialog box is closed without an image chosen
            try:
                self.filepath = os.path.split(fileObj.name)[0]
                self.filename = os.path.basename(fileObj.name)
            except:
                return None

            self.imageInfo.grid(sticky="w", padx=10, pady=(5, 0))
            self.imageInfo_text.set("Image uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(self.filepath, self.filename))

            self.error.grid_forget()
            self.errorMessage.set("")

            self.status.grid_forget()
            self.statusMessage.set("")


        def encryptImage():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.grid(sticky="w", padx=10, pady=(5, 0))
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

            try:
                newFilepath = multicrypt.encrypt(filename=self.filename, filepath=self.filepath, passKey=(k, k2), cipher=self.cipher, dataformat=self.dataFormat)
            except:
                self.statusMessage.set("Image encryption failed!")
            else:
                self.statusMessage.set("Image encrypted successfully!\n\nFilepath: {}".format(newFilepath))

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.imageInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()

        """Creates a header"""

        # The header frame is placed in the main application
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process, dataFormat=self.dataFormat))


        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_imageButton = tk.Button(self.subFrame, text="UPLOAD IMAGE", compound="left", image=self.IMAGE_UPLOAD,
        command=lambda: uploadImage(), **ButtonStyle.UPLOAD_BUTTON)
        self.imageInfo = tk.Label(self.subFrame, textvariable=self.imageInfo_text, wraplength=400, justify="left", bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG, font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=20, relief="flat", font=Fonts.KEY_TEXT)

        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subtext2 = tk.Label(self.subFrame5, text="SECOND KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox2 = tk.Entry(self.subFrame5, width=20, relief="flat", font=Fonts.KEY_TEXT)
        self.horizontalSeparator4 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame6 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame6, text="Encrypt", command=lambda: encryptImage(), **ButtonStyle.ENCRYPT2)
        self.error = tk.Label(self.subFrame6, textvariable=self.errorMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_imageButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, ipady=10)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid()
        self.subtext2.grid(sticky="w", pady=(8, 0))
        self.keyBox2.grid(padx=10, ipady=10)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame6.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16,50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.STATUS, font=Fonts.INFO)


class DecryptMenu(tk.Frame):
    """Creates the decryption page frame"""

    def __init__(self, master, process, dataFormat, cipher):
        tk.Frame.__init__(self, master)

        self.process = process
        self.dataFormat = dataFormat
        self.cipher = cipher

        # Initialise the icon used for this frame
        self.icon = Image.open("Images/copyIcon.png")
        self.icon2 = Image.open("Images/imageUpload.png")

        # Make the icon able to be used by widgets by these references
        self.COPY_ICON = ImageTk.PhotoImage(self.icon)
        self.IMAGE_UPLOAD = ImageTk.PhotoImage(self.icon2)

        self.configure(background=Colours.GREY_BACKGROUND, padx=10, pady=50)

        # Call the necessary function that creates the widgets
        # for the releveant section based on the data format
        if self.dataFormat == "Messages":
            # Triple DES requires a separate section
            if self.cipher == "Triple DES Cipher":
                self.messageSectionForTripleDES()
            else:
                self.messageSection()
        elif self.dataFormat == "Files":
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
            multicrypt module. Lastly, the ciphertext is placed in the output box
            """
            c = self.inputBox.get()
            k = self.keyBox.get()

            self.outputBox.delete("1.0", "end")
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

            self.error.grid_forget()
            self.errorMessage.set("")
            plainText = multicrypt.decrypt(ciphertext=c, passKey=k, cipher=self.cipher, dataformat=self.dataFormat)
            self.outputBox.insert("1.0", plainText)

        def copyInputToClipboard():
            i = self.inputBox.get()
            # The new line character must be ommited.
            i = i.split("\n")[0]
            self.master.clipboard_clear()
            self.master.clipboard_append(i)

        def copyOutputToClipboard():
            o = self.outputBox.get("1.0", "end")
            # The new line character must be ommited.
            o = o.split("\n")[0]
            self.master.clipboard_clear()
            self.master.clipboard_append(o)

        self.errorMessage = tk.StringVar()

        # Gets the top level window
        self.master = self.winfo_toplevel()

        # Create a header
        # The header frame is placed in the main application,
        # separate from the current frame
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        # Place the widgets in the grid layout
        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process, dataFormat=self.dataFormat))

        # Create the widgets for the encrypt section

        # Input frame section
        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.title = tk.Label(self.subFrame, text="Ciphertext", bg=Colours.BACKGROUND, fg=Colours.TITLE_FG, font=Fonts.TITLE)
        self.copyButton = tk.Button(self.subFrame, text="Copy Ciphertext", compound="left", image=self.COPY_ICON,
        command=lambda: copyInputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.subFrame2 = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.inputBox = tk.Entry(self.subFrame2, width=20, font=Fonts.TEXT, relief="flat")

        # Control frame section
        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG, font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=20, relief="flat", font=Fonts.KEY_TEXT)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)

        self.encryptButton = tk.Button(self.subFrame5, text="Decrypt", command=lambda: updateOutputBox(), **ButtonStyle.DECRYPT2)
        self.error = tk.Label(self.subFrame5, textvariable=self.errorMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        # Output frame section
        self.outputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame6 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame6, text="Plaintext", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.copyButton2 = tk.Button(self.subFrame6, text="Copy Plaintext", compound="left", image=self.COPY_ICON,
        command=lambda: copyOutputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator4 = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.subFrame7 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.outputBox = tk.Text(self.subFrame7, width=20, height=5, bd=0, wrap="word", bg=Colours.BACKGROUND, fg=Colours.GREY_FOREGROUND, font=Fonts.TEXT)

        # Place the widgets in the grid layout
        self.inputFrame.grid(padx=50, sticky="n")
        self.subFrame.grid(sticky="w")
        self.title.grid(padx=16, pady=16)
        self.copyButton.grid(column=1, row=0, padx=5)
        self.horizontalSeparator.grid(sticky="we")
        self.subFrame2.grid(sticky="w")
        self.inputBox.grid(padx=16, ipady=16, pady=(0, 90))

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", padx=8, pady=(8, 0))
        self.keyBox.grid(padx=10, ipady=10)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.outputFrame.grid(column=2, row=0, padx=50, sticky="n")
        self.subFrame6.grid(sticky="w")
        self.title2.grid(padx=(16,50), pady=16)
        self.copyButton2.grid(column=1, row=0, padx=5)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame7.grid(sticky="w")
        self.outputBox.grid(padx=16, pady=16)

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

            if k2 == "":
                self.errorMessage.set("The second key field is empty.")
                return None

            if len(k2) < 8:
                self.errorMessage.set("The second key must be at least 8 characters long.")
                return None

            self.error.grid_forget()
            self.errorMessage.set("")

            plainText = multicrypt.decrypt(ciphertext=c, passKey=(k, k2), cipher=self.cipher, dataformat=self.dataFormat)

            self.outputBox.insert("1.0", plainText)

        def copyInputToClipboard():
            i = self.inputBox.get()
            # The new line character must be ommited.
            i = i.split("\n")[0]
            self.master.clipboard_clear()
            self.master.clipboard_append(i)

        def copyOutputToClipboard():
            o = self.outputBox.get("1.0", "end")
            # The new line character must be ommited.
            o = o.split("\n")[0]
            self.master.clipboard_clear()
            self.master.clipboard_append(o)

        self.errorMessage = tk.StringVar()

        # Gets the top level window
        self.master = self.winfo_toplevel()

        # Create a header
        # The header frame is placed in the main application,
        # separate from the current frame
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        # Place the widgets in the grid layout
        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process, dataFormat=self.dataFormat))

        # Create the widgets for the encrypt section

        # Input frame section
        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.title = tk.Label(self.subFrame, text="Ciphertext", bg=Colours.BACKGROUND, fg=Colours.TITLE_FG, font=Fonts.TITLE)
        self.copyButton = tk.Button(self.subFrame, text="Copy Ciphertext", compound="left", image=self.COPY_ICON,
        command=lambda: copyInputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.subFrame2 = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.inputBox = tk.Entry(self.subFrame2, width=20, font=Fonts.TEXT, relief="flat")

        # Control frame section
        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG, font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=20, relief="flat", font=Fonts.KEY_TEXT)
        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subtext2 = tk.Label(self.subFrame5, text="SECOND KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox2 = tk.Entry(self.subFrame5, width=20, relief="flat", font=Fonts.KEY_TEXT)
        self.horizontalSeparator4 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subFrame6 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)

        self.encryptButton = tk.Button(self.subFrame6, text="Decrypt", command=lambda: updateOutputBox(), **ButtonStyle.DECRYPT2)
        self.error = tk.Label(self.subFrame6, textvariable=self.errorMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        # Output frame section
        self.outputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Plaintext", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.copyButton2 = tk.Button(self.subFrame7, text="Copy Plaintext", compound="left", image=self.COPY_ICON,
        command=lambda: copyOutputToClipboard(), **ButtonStyle.COPY_BUTTON)
        self.horizontalSeparator5 = tk.ttk.Separator(self.outputFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.outputFrame, bg=Colours.BACKGROUND)
        self.outputBox = tk.Text(self.subFrame8, width=20, height=10, bd=0, wrap="word", bg=Colours.BACKGROUND, fg=Colours.GREY_FOREGROUND, font=Fonts.TEXT)

        # Place the widgets in the grid layout
        self.inputFrame.grid(padx=50, sticky="n")
        self.subFrame.grid(sticky="w")
        self.title.grid(padx=16, pady=16)
        self.copyButton.grid(column=1, row=0, padx=5)
        self.horizontalSeparator.grid(sticky="we")
        self.subFrame2.grid(sticky="w")
        self.inputBox.grid(padx=16, ipady=16, pady=(0, 155))

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, ipady=10)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid()
        self.subtext2.grid(sticky="w", pady=(8, 0))
        self.keyBox2.grid(padx=10, ipady=10)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame6.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.outputFrame.grid(column=2, row=0, padx=50, sticky="n")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16,50), pady=16)
        self.copyButton2.grid(column=1, row=0, padx=5)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.outputBox.grid(padx=16, pady=16)

    def fileSection(self):
        # Gets the top level window
        self.master = self.winfo_toplevel()

        # Create a header
        # The header frame is placed in the main application,
        # separate from the current frame
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        # Place the widgets in the grid layout
        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process, dataFormat=self.dataFormat))

        # Create the widgets for the encrypt section
        self.t = tk.Label(self, text=self.cipher)
        self.t2 = tk.Label(self, text="Ciphertext")
        self.t3 = tk.Label(self, text="Files")

        # Place the widgets in the grid layout
        self.t.grid(padx=26, pady=(0, 10))
        self.t2.grid(padx=26, pady=(0, 10))
        self.t3.grid(padx=26, pady=(0, 10))

    def imageSection(self):
        def uploadImage():
            fileObj = tk.filedialog.askopenfile(title='Choose an image to decrypt', filetypes=[("Select images", "*.jpg *.png")])

            # An error is thrown if the dialog box is closed without an image chosen
            try:
                self.filepath = os.path.split(fileObj.name)[0]
                self.filename = os.path.basename(fileObj.name)
            except:
                return None

            self.imageInfo.grid(sticky="w", padx=10, pady=(5, 0))
            self.imageInfo_text.set("Image uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(self.filepath, self.filename))

            self.error.grid_forget()
            self.errorMessage.set("")

            self.status.grid_forget()
            self.statusMessage.set("")


        def decryptImage():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.grid(sticky="w", padx=10, pady=(5, 0))
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
                newFilepath = multicrypt.decrypt(filename=self.filename, filepath=self.filepath, passKey=k, cipher=self.cipher, dataformat=self.dataFormat)
            except:
                self.statusMessage.set("Image decryption failed!")
            else:
                self.statusMessage.set("Image decrypted successfully!\n\nFilepath: {}".format(newFilepath))

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.imageInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()

        """Creates a header"""

        # The header frame is placed in the main application
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process, dataFormat=self.dataFormat))


        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_imageButton = tk.Button(self.subFrame, text="UPLOAD IMAGE", compound="left", image=self.IMAGE_UPLOAD,
        command=lambda: uploadImage(), **ButtonStyle.UPLOAD_BUTTON)
        self.imageInfo = tk.Label(self.subFrame, textvariable=self.imageInfo_text, wraplength=400, justify="left", bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG, font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=20, relief="flat", font=Fonts.KEY_TEXT)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame5, text="Decrypt", command=lambda: decryptImage(), **ButtonStyle.ENCRYPT2)
        self.error = tk.Label(self.subFrame5, textvariable=self.errorMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_imageButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, ipady=10)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16,50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.STATUS, font=Fonts.INFO)

    def imageSectionForTripleDES(self):
        def uploadImage():
            fileObj = tk.filedialog.askopenfile(title='Choose an image to decrypt', filetypes=[("Select images", "*.jpg *.png")])
            # An error is thrown if the dialog box is closed without an image chosen
            try:
                self.filepath = os.path.split(fileObj.name)[0]
                self.filename = os.path.basename(fileObj.name)
            except:
                return None

            self.imageInfo.grid(sticky="w", padx=10, pady=(5, 0))
            self.imageInfo_text.set("Image uploaded successfully!\n\nFilepath: {}\nFilename: {}".format(self.filepath, self.filename))

            self.error.grid_forget()
            self.errorMessage.set("")

            self.status.grid_forget()
            self.statusMessage.set("")


        def decryptImage():
            self.error.grid(sticky="w", pady=(5, 0))
            self.status.grid(sticky="w", padx=10, pady=(5, 0))
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

            try:
                newFilepath = multicrypt.decrypt(filename=self.filename, filepath=self.filepath, passKey=(k, k2), cipher=self.cipher, dataformat=self.dataFormat)
            except:
                self.statusMessage.set("Image decryption failed!")
            else:
                self.statusMessage.set("Image decrypted successfully!\n\nFilepath: {}".format(newFilepath))

        self.filepath = None
        self.filename = None

        self.master = self.winfo_toplevel()  # Gets the top level window

        # Text variables that store messages
        self.imageInfo_text = tk.StringVar()
        self.errorMessage = tk.StringVar()
        self.statusMessage = tk.StringVar()

        """Creates a header"""

        # The header frame is placed in the main application
        self.header = tk.Frame(self.master, bg=Colours.MAIN)
        self.Logo = tk.Label(self.header, text="Padlock", bg=Colours.MAIN, fg=Colours.LOGO, font=Fonts.LOGO)
        self.homeTag = tk.Label(self.header, text="Home", bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag = tk.Label(self.header, text=self.process, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag2 = tk.Label(self.header, text=self.dataFormat, bg=Colours.MAIN, fg=Colours.TAGS_NOT_ACTIVE, font=Fonts.TAGS, cursor="hand2")
        self.sectionTag3 = tk.Label(self.header, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.FOREGROUND, font=Fonts.TAGS)

        self.header.grid(row=0, sticky="new")
        self.Logo.grid(padx=20, pady=20)
        self.homeTag.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.sectionTag.grid(column=2, row=0, pady=(10, 0), padx=10)
        self.sectionTag2.grid(column=3, row=0, pady=(10, 0), padx=10)
        self.sectionTag3.grid(column=4, row=0, sticky="ns", ipadx=40, pady=(10, 0), padx=10)

        # Add an event handler for the tag to act like a link when clicked
        self.homeTag.bind("<Button-1>", lambda e: self.master.switch_frame(HomePage))
        self.sectionTag.bind("<Button-1>", lambda e: self.master.switch_frame(FormatSelctionMenu, process=self.process))
        self.sectionTag2.bind("<Button-1>", lambda e: self.master.switch_frame(CipherMenu, process=self.process, dataFormat=self.dataFormat))

        """Input frame section"""

        self.inputFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame = tk.Frame(self.inputFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator = tk.ttk.Separator(self.inputFrame, orient="horizontal")
        self.upload_imageButton = tk.Button(self.subFrame, text="UPLOAD IMAGE", compound="left", image=self.IMAGE_UPLOAD,
        command=lambda: uploadImage(), **ButtonStyle.UPLOAD_BUTTON)
        self.imageInfo = tk.Label(self.subFrame, textvariable=self.imageInfo_text, wraplength=400, justify="left", bg=Colours.BACKGROUND, fg=Colours.INFO, font=Fonts.INFO)

        """Control frame section"""

        self.controlFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame3 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.cipherLabel = tk.Label(self.subFrame3, text=self.cipher, bg=Colours.BACKGROUND, fg=Colours.CIPHER_FG, font=Fonts.TITLE)
        self.horizontalSeparator2 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame4 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.subtext = tk.Label(self.subFrame4, text="KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox = tk.Entry(self.subFrame4, width=20, relief="flat", font=Fonts.KEY_TEXT)

        self.subFrame5 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.horizontalSeparator3 = tk.ttk.Separator(self.controlFrame, orient="horizontal")
        self.subtext2 = tk.Label(self.subFrame5, text="SECOND KEY", bg=Colours.BACKGROUND, fg=Colours.SMALL_TITLE, font=Fonts.TITLE2)
        self.keyBox2 = tk.Entry(self.subFrame5, width=20, relief="flat", font=Fonts.KEY_TEXT)
        self.horizontalSeparator4 = tk.ttk.Separator(self.controlFrame, orient="horizontal")

        self.subFrame6 = tk.Frame(self.controlFrame, bg=Colours.BACKGROUND)
        self.encryptButton = tk.Button(self.subFrame6, text="Decrypt", command=lambda: decryptImage(), **ButtonStyle.ENCRYPT2)
        self.error = tk.Label(self.subFrame6, textvariable=self.errorMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.ERROR, font=Fonts.ERROR)

        """Status frame section"""

        self.statusFrame = tk.Frame(self, bg=Colours.BACKGROUND)
        self.subFrame7 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)
        self.title2 = tk.Label(self.subFrame7, text="Status", bg=Colours.BACKGROUND, fg=Colours.TITLE2_FG, font=Fonts.TITLE)
        self.horizontalSeparator5 = tk.ttk.Separator(self.statusFrame, orient="horizontal")
        self.subFrame8 = tk.Frame(self.statusFrame, bg=Colours.BACKGROUND)

        self.inputFrame.grid(padx=50, sticky="ns")
        self.subFrame.grid(sticky="w")
        self.upload_imageButton.grid(padx=10, pady=10)

        self.controlFrame.grid(column=1, row=0, padx=50, sticky="n")
        self.subFrame3.grid(sticky="w")
        self.cipherLabel.grid(padx=16, pady=16)
        self.horizontalSeparator2.grid(sticky="we")
        self.subFrame4.grid()
        self.subtext.grid(sticky="w", pady=(8, 0))
        self.keyBox.grid(padx=10, ipady=10)
        self.horizontalSeparator3.grid(sticky="we")
        self.subFrame5.grid()
        self.subtext2.grid(sticky="w", pady=(8, 0))
        self.keyBox2.grid(padx=10, ipady=10)
        self.horizontalSeparator4.grid(sticky="we")
        self.subFrame6.grid(sticky="w", padx=10, pady=10)
        self.encryptButton.grid()

        self.statusFrame.grid(column=2, row=0, padx=50, sticky="ns")
        self.subFrame7.grid(sticky="w")
        self.title2.grid(padx=(16, 50), pady=16)
        self.horizontalSeparator5.grid(sticky="we")
        self.subFrame8.grid(sticky="w")
        self.status = tk.Label(self.subFrame8, textvariable=self.statusMessage, wraplength=200, justify="left", bg=Colours.BACKGROUND, fg=Colours.STATUS, font=Fonts.INFO)

if __name__ == "__main__":
    app = Padlock()
    app.mainloop()
