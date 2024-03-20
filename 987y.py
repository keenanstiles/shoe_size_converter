from tkinter import *
from functools import partial  # To prevent unwanted windows
from datetime import date
import re


class Converter:

    def __init__(self):

        # Initialise variables (such as the feedback variable)
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        def on_option_select(event):
            selected_option.set(event)

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_calculations = []

        # common format for all buttons
        # Arial size 14 bold, with white text
        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"

if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
