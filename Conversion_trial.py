from tkinter import *
from tkinter import ttk
from functools import partial

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
                                          command=self.open_converter)
        self.to_converter_button.grid(row=2, padx=5, pady=5)

    def open_converter(self):
        self.converter = Converter()

class Converter:

    def __init__(self):

        # Initialise variables (such as the feedback variable)
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_calculations = []

# common format for all dropdown menus
        dropdown_font = ("Arial", "12")

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
                                  text="Shoe Size Converter",
                                  font=("Arial", "16", "bold")
                                  )
        self.temp_heading.grid(row=0)

        instructions = "Please select your desired size types from the drop-downs below and " \
                       "then press convert :) -luv keenan."
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wrap=250, width=40,
                                       justify="left")
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame,
                                font=("Arial", "14")
                                )
        self.temp_entry.grid(row=2, padx=10, pady=10)

        error = "Please enter a number"
        self.output_label = Label(self.temp_frame, text="",
                                  fg="#9C0000")
        self.output_label.grid(row=3)

        # Conversion dropdown menu
        self.from_units = StringVar()
        self.from_units.set("US")  # default value

        self.to_units = StringVar()
        self.to_units.set("EURO")  # default value

        self.dropdown_frame = Frame(self.temp_frame)
        self.dropdown_frame.grid(row=4)
# Updated dropdown menus
        self.from_dropdown = ttk.Combobox(self.dropdown_frame, textvariable=self.from_units, font=dropdown_font, state="readonly")
        self.from_dropdown['values'] = ("US", "EURO")
        self.from_dropdown.grid(row=0, column=0, padx=5, pady=5)

        self.to_dropdown = ttk.Combobox(self.dropdown_frame, textvariable=self.to_units, font=dropdown_font, state="readonly")
        self.to_dropdown['values'] = ("US", "EURO")
        self.to_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Convert button
        self.convert_button = Button(self.temp_frame,
                                     text="Convert",
                                     bg="#0066CC",
                                     fg="white",
                                     font=("Arial", "12", "bold"),
                                     width=12,
                                     command=self.temp_convert)
        self.convert_button.grid(row=5, columnspan=2, padx=5, pady=5)

    # checks user input and if it's valid, converts temperature
    def check_temp(self, min_value):

        has_error = "no"
        error = "Please enter a number that is more "\
                "than {}".format(min_value)

        # check that user has entered a valid number...

        response = self.temp_entry.get()

        try:
            response = float(response)

            if response < min_value:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        # Sets var_has_error so that entry box and
        # label can be correctly formatted by formatting function
        if has_error == "yes":
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"

        # If we have no errors...
        else:
            # set to 'no' in case of previous errors
            self.var_has_error.set("no")

            # return number to be
            # converted and enable history button
            return response

    @staticmethod
    def round_ans(val):
        var_rounded = (val * 2 + 1) // 2
        return "{:.0f}".format(var_rounded)

    # check temperature is valid and convert it
    def temp_convert(self):
        min_val = 30 if self.from_units.get() == "EURO" else 3
        to_convert = self.check_temp(min_val)
        set_feedback = "yes"
        answer = ""
        from_to = ""

        if to_convert == "invalid":
            set_feedback = "no"

        # convert to selected unit
        if self.from_units.get() == "US" and self.to_units.get() == "EURO":
            answer = to_convert + 32
            from_to = "{} US is {} Euro"

        elif self.from_units.get() == "EURO" and self.to_units.get() == "US":
            answer = (to_convert - 32)
            from_to = "{} Euro is {} US"

        if set_feedback == "yes":
            to_convert = self.round_ans(to_convert)
            answer = self.round_ans(answer)

            # create user output and add to calculation history
            feedback = from_to.format(to_convert,
                                      answer)
            self.var_feedback.set(feedback)
            self.all_calculations.append(feedback)

        self.output_answer()

    # shows user output and clears entry widget
    # ready for next calculation
    def output_answer(self):
        output = self.var_feedback.get()
        has_errors = self.var_has_error.get()

        if has_errors == "yes":
            # red text, pink entry box
            self.output_label.config(fg="#9C0000")
            self.temp_entry.config(bg="#F8CECC")

        else:
            self.output_label.config(fg="#004C00")
            self.temp_entry.config(bg="#FFFFFF")

        self.output_label.config(text=output)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self):
        self.converter_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Information Screen")
    DisplayHelp()
    root.mainloop()