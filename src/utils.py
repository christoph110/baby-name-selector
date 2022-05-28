"""module with utility functions"""
import sys
import tkinter.messagebox as msgbox


def error_message(title: str, msg: str) -> None:
    """shows a message box and raises an error"""
    msgbox.showerror(title=title,
                     message=msg)
    sys.exit()
