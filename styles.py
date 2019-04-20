# Stylesheet

"""
Padlock Encryption Software
Copyright 2019

Created by: Suraj Kothari
For A-level Computer Science
at Woodhouse College.
"""


class Colours:
    """ Set of colours to use in the application """

    MAIN = "#455A64"
    FOOTER = "#37474F"
    LOGO = "#F9A825"
    TAGS_NOT_ACTIVE = "#E6E6E6"
    BACKGROUND = "#FFF"
    GREY_BACKGROUND = "#F2F4F6"
    FOREGROUND = "#000"
    GREY_FOREGROUND = "#90999E"
    TITLE_FG = "#4CAF50"
    TITLE2_FG = "#F44336"
    SMALL_TITLE = "#90999E"
    CIPHER_FG = "#FF5722"
    ERROR = "#F44336"
    INFO = "#555"
    STATUS_OK = "#4CAF50"
    STATUS_WAIT = "#FF5722"
    GUIDE_LINK = "#00BCD4"


class Fonts:
    """ Set of fonts to use in the application """

    LOGO = ('Century Gothic Bold', '18')
    SMALL_PRINT = ('Arial', '8')
    TAGS = ('Calibri', '14')
    TITLE = ('Arial Bold', '14')
    TITLE2 = ('Arial Bold', '10')
    TEXT = ('Courier', '12')
    KEY_TEXT = ('Arial Bold', '12')
    ERROR = ('Arial Bold', '10')
    INFO = ('Arial Bold', '10')


class ButtonStyle:
    """ Styles used for the buttons in the application """

    ENCRYPT_BUTTON = {
        "bg": "#4CAF50",
        "activebackground": "#58CE5D",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 150,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    # Used in the encryption menu
    ENCRYPT2_BUTTON = {
        "bg": "#4CAF50",
        "activebackground": "#58CE5D",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 20,
        "relief": "flat",
        "font": ("Arial", 12),
        "cursor": "hand2"
    }

    DECRYPT_BUTTON = {
        "bg": "#F44336",
        "activebackground": "#F96854",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 150,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    # Used in the decryption menu
    DECRYPT2_BUTTON = {
        "bg": "#F44336",
        "activebackground": "#F96854",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 20,
        "relief": "flat",
        "font": ("Arial", 12),
        "cursor": "hand2"
    }

    MESSAGE_BUTTON = {
        "bg": "#4CAF50",
        "activebackground": "#58CE5D",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 150,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    FILE_BUTTON = {
        "bg": "#FF5722",
        "activebackground": "#fc683a",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 150,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    IMAGE_BUTTON = {
        "bg": "#F44336",
        "activebackground": "#F96854",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 150,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    CLASSIC_BUTTON = {
        "bg": "#FFC107",
        "activebackground": "#ffd044",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 10,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    ASCII_BUTTON = {
        "bg": "#034C9D",
        "activebackground": "#0559B7",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 10,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    BASE64_BUTTON = {
        "bg": "#8BC34A",
        "activebackground": "#9AD852",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 10,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    CAESAR_BUTTON = {
        "bg": "#F0D347",
        "activebackground": "#FCDD49",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 10,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    VIGENERE_BUTTON = {
        "bg": "#F0D347",
        "activebackground": "#FCDD49",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 10,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    DES_BUTTON = {
        "bg": "#FF5722",
        "activebackground": "#FF7347",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 10,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2",
    }

    TRIPLE_DES_BUTTON = {
        "bg": "#FF5722",
        "activebackground": "#FF7347",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 10,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    AES_BUTTON = {
        "bg": "#F44336",
        "activebackground": "#f96854",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 10,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2",
    }

    COPY_BUTTON = {
        "bg": "#2196F3",
        "activebackground": "#3DA5f7",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 1,
        "padx": 10,
        "width": 120,
        "relief": "flat",
        "font": ("Arial Bold", 10),
        "cursor": "hand2"
    }

    UPLOAD_BUTTON = {
        "bg": "#2196F3",
        "activebackground": "#3DA5f7",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 1,
        "padx": 10,
        "width": 200,
        "relief": "flat",
        "font": ("Arial Bold", 10),
        "cursor": "hand2"
    }
