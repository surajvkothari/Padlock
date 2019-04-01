# Stylesheet

"""
Padlock Encryption Software
Copyright 2019

Created by: Suraj Kothari
For A-level Computer Science
at Woodhouse College.
"""

class Colours:
    """Set of colours to use in the application"""
    MAIN = "#344955"
    SECONDARY = "#232F34"
    LOGO = "#F9AA33"
    TAGS_NOT_ACTIVE = "#E6E6E6"
    BACKGROUND = "#FFF"
    GREY_BACKGROUND = "#F2F4F6"
    FOREGROUND = "#000"
    GREY_FOREGROUND = "#90999E"
    TITLE_FG = "#2ECC71"
    TITLE2_FG = "#E74C3C"
    SMALL_TITLE = "#90999E"
    CIPHER_FG = "#F9AA33"
    ERROR = "#E30425"
    INFO = "#555"
    STATUS_OK = "#609F74"
    STATUS_ERROR = "#E30425"
    STATUS_WAIT = "#F9AA33"
    GUIDE_LINK = "#3D9ADB"


class Fonts:
    """Set of fonts to use in the application"""
    LOGO = ('Broadway', '18')
    SMALL_PRINT = ('Arial', '8')
    TAGS = ('Calibri', '14')
    TITLE = ('Arial Bold', '14')
    TITLE2 = ('Arial Bold', '10')
    TEXT = ('Courier', '12')
    KEY_TEXT = ('Arial Bold', '12')
    ERROR = ('Arial Bold', '10')
    INFO = ('Arial Bold', '10')


class ButtonStyle:
    """Styles used for the buttons in the application"""
    ENCRYPT_BUTTON = {
        "bg": "#2ECC71",
        "activebackground": "#48E68B",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 150,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    ENCRYPT2_BUTTON = {
        "bg": "#2ECC71",
        "activebackground": "#48E68B",
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
        "bg": "#E74C3C",
        "activebackground": "#FF6656",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 5,
        "padx": 10,
        "width": 150,
        "relief": "flat",
        "font": ("Arial", 16),
        "cursor": "hand2"
    }

    DECRYPT2_BUTTON = {
        "bg": "#E74C3C",
        "activebackground": "#FF6656",
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
        "bg": "#4CB050",
        "activebackground": "#66BB6A",
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
        "bg": "#E67E22",
        "activebackground": "#E09655",
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
        "bg": "#E74C3C",
        "activebackground": "#FF6656",
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
        "bg": "#5FA926",
        "activebackground": "#439A00",
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

    COPY_BUTTON = {
        "bg": "#3f9ADB",
        "activebackground": "#5981CC",
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
        "bg": "#3f9ADB",
        "activebackground": "#5981CC",
        "fg": "#FFF",
        "activeforeground": "#FFF",
        "pady": 1,
        "padx": 10,
        "width": 200,
        "relief": "flat",
        "font": ("Arial Bold", 10),
        "cursor": "hand2"
    }
