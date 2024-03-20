from tkinter import *
from functools import partial


class DisplayHelp:
    def close_help(self, partner):
        # put help button back to normal
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()

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
        self.help_frame.destroy()
        Converter()


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
                                    partial(self.close_help, partner=None))

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

        self.from_dropdown = OptionMenu(self.dropdown_frame, self.from_units, "US", "EURO")
        self.from_dropdown.config(font=dropdown_font)
        self.from_dropdown.grid(row=0, column=0, padx=5, pady=5)

        self.to_dropdown = OptionMenu(self.dropdown_frame, self.to_units, "US", "EURO")
        self.to_dropdown.config(font=dropdown_font)
        self.to_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Toggle switch for men's and women's sizes
        self.gender_var = StringVar()
        self.gender_var.set("men")

        self.gender_frame = Frame(self.temp_frame)
        self.gender_frame.grid(row=5, pady=10)

        self.men_radio = Radiobutton(self.gender_frame, text="Men's Sizes", variable=self.gender_var, value="men")
        self.men_radio.grid(row=0, column=0, padx=5)

        self.women_radio = Radiobutton(self.gender_frame, text="Women's Sizes", variable=self.gender_var, value="women")
        self.women_radio.grid(row=0, column=1, padx=5)

        # Convert button
        self.convert_button = Button(self.temp_frame,
                                     text="Convert",
                                     bg="#0066CC",
                                     fg="white",
                                     font=("Arial", "12", "bold"),
                                     width=12,
                                     command=self.temp_convert)
        self.convert_button.grid(row=6, columnspan=2, padx=5, pady=5)

    # checks user input and if it's valid, converts temperature
    # closes help dialouge
    def check_temp(self, min_value):

        has_error = "no"
        error = "Please enter a number that is more " \
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
        min_val = -459 if self.from_units.get() == "EURO" else -273
        to_convert = self.check_temp(min_val)
        deg_sign = u'\N{DEGREE SIGN}'
        set_feedback = "yes"
        answer = ""
        from_to = ""

        if to_convert == "invalid":
            set_feedback = "no"

        # convert to selected unit
        if self.from_units.get() == "US" and self.to_units.get() == "EURO":
            answer = to_convert * 1.8 + 32
            from_to = "{} US{} is {} F{}"

        elif self.from_units.get() == "EURO" and self.to_units.get() == "US":
            answer = (to_convert - 32) * 5 / 9
            from_to = "{} F{} is {} US{}"

        if set_feedback == "yes":
            to_convert = self.round_ans(to_convert)
            answer = self.round_ans(answer)

            # create user output and add to calculation history
            feedback = from_to.format(to_convert, deg_sign,
                                      answer, deg_sign)
            self.var_feedback.set(feedback)

            self.all_calculations.append(feedback)

    # shows user output and clears entry widget
    # ready for

    def output_answer(self):
        output = self.var_feedback.get()
        has_errors = self.var_has_error.get()

        if has_errors == "yes":
            self.output_label.config(fg="#9C0000")
            self.temp_entry.config(bg="#F8CECC")

        else:
            self.output_label.config(fg="#004C00")
            self.temp_entry.config(bg="#FFFFFF")

        self.output_label.config(text=output)

    def to_help(self):
        DisplayHelp(self)


class DisplayHelp:

    def __init__(self, partner):
        background = "#ffe6cc"
        self.help_box = Toplevel()

        partner.to_help_button.config(state=DISABLED)

        # yadda yadda more stuf to make help button active again if no
        # window present
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, bg=background,
                                        text="help / info",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "To use the program, simply enter the temperature " \
                    "you wish to convert and then choose to convert " \
                    "to either degrees celsius or " \
                    "fahrenheit.. \n\n" \
                    "Note that -237 degrees C " \
                    "(-459 F) is absolute zero (the coldest possible " \
                    "temperature), try no convert less then this and youll get an error message \n\n " \
                    "go to the history tab to download recent calculations into a text file"
        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="dismiss", bg="#CC6600",
                                     fg="#ffffff",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperture Convertor")
    Converter()
    root.mainloop()