from tkinter import *


class Converter:

    def __init__(self):

        #initialise variables (such as the feedback variables)
        self.var_feedback = StringVar()
        self.var_feedback.set("no")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        # common format for all buttons

        button_font = ("Arial", "14", "bold")
        button_fg = "#FFFFFF"

        # Set up GUI Frame
        self.temp_frame = Frame()
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Temperature Convertor",
                                  font=("Arial", "16", "bold")
                                  )
        self.temp_heading.grid(row=0)

        instructions = "Please enter a temperature below and" \
                       "then press one of the buttons to convert" \
                       "it from centigrade to Fahrenheit."
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

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        self.to_celsius_button = Button(self.button_frame,
                                        text="To Celsius",
                                        bg="#990099",
                                        fg=button_fg,
                                        font=button_font, width=12,
                                        command=self.to_celsius)
        self.to_celsius_button.grid(row=0, column=0, padx=5, pady=5)

        self.to_fahrenheit_button = Button(self.button_frame,
                                        text="To Fahrenheit",
                                        bg="#009900",
                                        fg=button_fg,
                                        font=button_font, width=12,
                                        command=self.to_fahrenheit)
        self.to_fahrenheit_button.grid(row=0, column=1, padx=5, pady=5)

        self.to_help_button = Button(self.button_frame,
                                        text="Help / Info",
                                        bg="#CC6600",
                                        fg=button_fg,
                                        font=button_font, width=12)
        self.to_help_button.grid(row=1, column=0, padx=5, pady=5)

        self.to_history_button = Button(self.button_frame,
                                           text="History / Export",
                                           bg="#004C99",
                                           fg=button_fg,
                                           font=button_font, width=12,
                                        state=DISABLED)
        self.to_history_button.grid(row=1, column=1, padx=5, pady=5)

  #just giving it a little peek to be sure its valid prior to conversion

    def check_temp(self, min_value):

        has_error = "no"
        error = ("ENTER AN INTEGER GREATER " \
                 "THAN {}".format(min_value))
        # check the number is valid

        response = self.temp_entry.get()

        try:

            response = float(response)

            if response < min_value:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        #sets var has error blah blah
        #formatting stuff yedda yadda
        if has_error == "yes":
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"

        #if no errors (woop woop!)
        else:
            self.var_has_error.set("no")

            #return the number
            #converted and enable history button


            self.to_history_button.config(state=NORMAL)
            return response


    # check temperature is more than -459 before converting it
    def to_celsius(self):
        to_convert = self.check_temp(-459)

        if to_convert != "invalid":
            self.var_feedback.set("Converting {} to"
                                  " C :)".format(to_convert))

        self.output_answer()



    def to_fahrenheit(self):
        to_convert = self.check_temp(-273)

        if to_convert != "invalid":
            # do calculation
            self.var_feedback.set("converting {} to "
                                      " F :)".format(to_convert))

        self.output_answer()

    # shows user output and clears entry widget
    # ready for next calculation

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




# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperture Convertor")
    Converter()
    root.mainloop()