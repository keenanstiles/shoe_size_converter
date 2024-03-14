from tkinter import *
from functools import partial  # To prevent unwanted windows


class DisplayHelp:

    def __init__(self):

        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"

        # set up GUI frame
        self.help_frame = Frame()
        self.help_frame.grid()

        self.help_heading = Label(self.help_frame,
                                  text="Help/Instructions",
                                  font=("Arial", "16", "bold")
                                  )
        self.help_heading.grid(row=0)

        instructions = "Here's what to do with my awesome shoe size" \
                       " converter"
        self.help_instructions = Label(self.help_frame,
                                       text=instructions,
                                       wrap=250, width=40,
                                       justify="left")
        self.help_instructions.grid(row=1)

        self.to_converter_button = Button(self.help_frame,
                                     text="Converter",
                                     bg="#CC6600",
                                     fg=button_fg,
                                     font=button_font,
                                     width=12,
                                     command=self.to_converter)
        self.to_converter_button.grid(row=2, padx=5, pady=5)

    def to_converter(self):
        Converter()


class Converter:

    def __init__(self):

        # Initialise variables (such as the feedback variable)
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_calculations = []

        # common format for all buttons
        # Arial size 14 bold, with white text
        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"

        # setup dialogue box and background colour
        self.converter_box = Toplevel()

        # If users press cross at top, closes help and
        # 'releases' help button
        self.converter_box.protocol('WM_DELETE_WINDOW',
                                        partial(self.close_help))

        # set up GUI frame
        self.temp_frame = Frame(self.converter_box, width=300, height=200)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Temperature Converter",
                                  font=("Arial", "16", "bold")
                                  )
        self.temp_heading.grid(row=0)

        instructions = "Please select a variable for conversion from the dropdown menus below."
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wrap=250, width=40,
                                       justify="left")
        self.temp_instructions.grid(row=1)

        # Dropdown menu for variable selection
        self.variable_a_label = Label(self.temp_frame, text="Variable A:")
        self.variable_a_label.grid(row=2, column=0, padx=5, pady=5)
        self.variable_a_menu = OptionMenu(self.temp_frame, StringVar(), "a", "b", "c", "d", "e")
        self.variable_a_menu.grid(row=2, column=1, padx=5, pady=5)

        self.variable_b_label = Label(self.temp_frame, text="Variable B:")
        self.variable_b_label.grid(row=3, column=0, padx=5, pady=5)
        self.variable_b_menu = OptionMenu(self.temp_frame, StringVar(), "a", "b", "c", "d", "e")
        self.variable_b_menu.grid(row=3, column=1, padx=5, pady=5)

        # Conversion and close buttons
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        self.convert_button = Button(self.button_frame,
                                     text="Convert",
                                     bg="#336699",
                                     fg=button_fg,
                                     font=button_font,
                                     width=12,
                                     command=self.convert)
        self.convert_button.grid(row=0, column=0, padx=5, pady=5)

        self.close_button = Button(self.button_frame,
                                   text="Close",
                                   bg="#CC3300",
                                   fg=button_fg,
                                   font=button_font,
                                   width=12,
                                   command=self.close_help)
        self.close_button.grid(row=0, column=1, padx=5, pady=5)

    def convert(self):
        variable_a = self.variable_a_menu["text"]
        variable_b = self.variable_b_menu["text"]
        # Conversion logic here
        print("Converting {} to {}".format(variable_a, variable_b))

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self):
        self.converter_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    DisplayHelp()
    root.mainloop()
