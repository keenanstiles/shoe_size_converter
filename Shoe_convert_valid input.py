
from tkinter import *
from tkinter import ttk
from functools import partial  # To prevent unwanted windows
import re
from datetime import date


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

        instructions = "To use the program, simply enter the shoe size value " \
                    "you wish to convert and then select what shoe unit your value is " \
                    "from the 'Input Size' dropdown" \
                    "then from the 'Output Size' dropdown, select which unit you would like to convert to.  \n\n" \
                    "Note that your entered value must exceed 0 \n\n" \
                    "To see your " \
                    "calculation history and export it to a text " \
                    "file, please click the 'History / Export' button."
        self.help_instructions = Label(self.help_frame,
                                       text=instructions,
                                       wrap=250, width=40,
                                       justify="left")
        self.help_instructions.grid(row=1)

        self.to_converter_button = Button(self.help_frame,
                                          text=" Continue to Converter",
                                          bg="#CC6600",
                                          fg=button_fg,
                                          font=button_font,
                                          width=20,
                                          command=self.open_converter)
        self.to_converter_button.grid(row=2, padx=5, pady=5)

    def open_converter(self):
        self.converter = Converter()
        self.converter.converter_box.mainloop()


class Converter:

    def __init__(self):

        # Initialise variables (such as the feedback variable)
        self.all_calculations = []

        # common format for all dropdown menus
        dropdown_font = ("Arial", "12")

        # setup dialogue box and background colour
        self.converter_box = Toplevel()

        # If users press cross at top, closes help and
        # 'releases' help button
        self.converter_box.protocol('WM_DELETE_WINDOW', self.close_help)

        # set up GUI frame
        self.shoe_frame = Frame(self.converter_box, width=300, height=200)
        self.shoe_frame.grid()

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.shoe_heading = Label(self.shoe_frame,
                                  text="Shoe Size Converter",
                                  font=("Arial", "16", "bold")
                                  )
        self.shoe_heading.grid(row=0)

        instructions = "Please select your desired size types from the drop-downs below and " \
                       "then press convert :)"
        self.shoe_instructions = Label(self.shoe_frame,
                                       text=instructions,
                                       wrap=250, width=40,
                                       justify="left")
        self.shoe_instructions.grid(row=1)

        self.shoe_entry = Entry(self.shoe_frame,
                                font=("Arial", "14")
                                )
        self.shoe_entry.grid(row=2, padx=10, pady=10)

        error = "Please enter a number"
        self.output_label = Label(self.shoe_frame, text="",
                                  fg="#228b22")
        self.output_label.grid(row=3)

        # Input size label
        self.input_size_label = Label(self.shoe_frame, text="Input size:")
        self.input_size_label.grid(row=4)

        # Conversion dropdown menu
        self.from_units = StringVar()
        self.from_units.set("US")  # default value

        self.dropdown_frame = Frame(self.shoe_frame)
        self.dropdown_frame.grid(row=5)

        # Updated dropdown menus
        self.from_dropdown = ttk.Combobox(self.dropdown_frame, textvariable=self.from_units, font=dropdown_font,
                                          state="readonly")
        self.from_dropdown['values'] = ("US", "EURO", "UK")
        self.from_dropdown.grid(row=0, column=0, padx=5, pady=5)

        # Output size label
        self.output_size_label = Label(self.shoe_frame, text="Output size:")
        self.output_size_label.grid(row=6)

        # Conversion dropdown menu
        self.to_units = StringVar()
        self.to_units.set("EURO")  # default value

        self.to_dropdown = ttk.Combobox(self.shoe_frame, textvariable=self.to_units, font=dropdown_font,
                                        state="readonly")
        self.to_dropdown['values'] = ("US", "EURO", "UK")
        self.to_dropdown.grid(row=7, padx=5, pady=5)

        # Radio buttons for selecting men's or women's sizing
        self.sizing_var = StringVar()
        self.sizing_var.set("Men's")
        self.sizing_frame = Frame(self.shoe_frame)
        self.sizing_frame.grid(row=8)
        self.men_sizing = Radiobutton(self.sizing_frame, text="Men's", variable=self.sizing_var, value="Men's")
        self.men_sizing.grid(row=0, column=0, padx=5, pady=5)
        self.women_sizing = Radiobutton(self.sizing_frame, text="Women's", variable=self.sizing_var, value="Women's")
        self.women_sizing.grid(row=0, column=1, padx=5, pady=5)

        self.button_frame = Frame(self.shoe_frame)
        self.button_frame.grid(row=10)

        # Convert button
        self.convert_button = Button(self.shoe_frame,
                                     text="Convert",
                                     bg="teal",
                                     fg="white",
                                     font=("Arial", "12", "bold"),
                                     width=28,
                                     command=self.shoe_convert)
        self.convert_button.grid(row=9, padx=5, pady=5)

        self.to_history_button = Button(self.button_frame,
                                        text="History / Export",
                                        bg="black",
                                        fg="white",
                                        font=("Arial", "12", "bold"),
                                        width=12,
                                        state=DISABLED,
                                        command=lambda: self.to_history(self.all_calculations)
                                        )
        self.to_history_button.grid(row=0, column=1, padx=5, pady=5)

        self.back_to_info = Button(self.button_frame,
                                        text="Back to Help",
                                        bg="grey",
                                        fg="white",
                                        font=("Arial", "12", "bold"),
                                        width=12,
                                        command=self.close_convert)
        self.back_to_info.grid(row=0, column=0, padx=5, pady=5)

        # Conversion rates
        self.conversion_rates = {
            "US Men's": {
                "EURO Men's": 33,
                "US Men's": 0,
                "UK Men's": -0.5
            },
            "US Women's": {
                "EURO Women's": 31,
                "US Women's": 0
            },
            "EURO Men's": {
                "US Men's": -33,
                "EURO Men's": 0,
                "UK Men's": -33.5
            },
            "EURO Women's": {
                "US Women's": -31,
                "EURO Women's": 0
            },
            "UK Men's": {
                "US Men's": 0.5,
                "EURO Men's": 33.5,
                "UK Men's": 0
            }
        }

    # Opens History / Export dialogue
    def to_history(self, all_calculations):
        HistoryExport(self, all_calculations)

    def close_convert(self):
        self.converter_box.destroy()

    def check_shoe(self, min_value):

        has_errors = ""

        try:
            response = int(self.shoe_entry.get())
            if response < min_value:
                print("Invalid input")
                has_errors = "yes"
                self.var_has_error.set("yes")
                self.var_feedback.set("Please enter a number greater than {}".format(min_value))
                return None
            else:
                self.var_has_error.set("no")
                # return number to be
                # converted and enable history button
                self.to_history_button.config(state=NORMAL)
                return response
        except ValueError:
            self.var_has_error.set("yes")
            has_errors = "yes"
            self.var_feedback.set("Please enter a valid number")
            return None


    def output_answer(self):
        output = self.var_feedback.get()
        has_errors = self.var_has_error.get()


        if has_errors == "yes":
            # red text, pink entry box
            self.output_label.config(fg="#9C0000", font=("Arial", "10"))
            self.shoe_entry.config(bg="#F8CECC")

        else:
            self.output_label.config(fg="#004C00", font=("Arial", "14", "bold"))
            self.shoe_entry.config(bg="#FFFFFF")

        self.output_label.config(text=output)

        # clears entry box ready for the next calculation
        self.shoe_entry.delete(0, END)

    def shoe_convert(self):
        error = f"Please enter a valid number greater than 4"
        to_convert = self.check_shoe(4)
        if to_convert is not None:
            from_units = self.from_units.get()
            to_units = self.to_units.get()
            sizing_var = self.sizing_var.get()
            converted_size, message = self.convert_size(from_units, to_units, sizing_var, to_convert)
            self.output_label.config(text=message)
            self.all_calculations.append(message)

        else:
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            self.output_label.config(text=error)


    # pull the appropriate data from the data set, runs the conversion and then prints the
    # proper conversion

    def convert_size(self, from_units, to_units, sizing_var, to_convert):

        from_key = f"{from_units} {sizing_var}"

        to_key = f"{to_units} {sizing_var}"

        found_conversion_rate = self.conversion_rates[from_key][to_key]

        converted_size = to_convert + found_conversion_rate

        return converted_size, f"{to_convert} {from_units} {sizing_var} is {converted_size} {to_units} {sizing_var}"

    def close_help(self):
        self.converter_box.destroy()


class HistoryExport:

    def __init__(self, partner, calc_list):

        # set maximum number of calculations to 5
        # this can be changed if we want to show fewer /
        # more calculations
        max_calcs = 5
        self.var_max_calcs = IntVar()
        self.var_max_calcs.set(max_calcs)

        # Set variables to hold filename and date
        # for when writing to file
        self.var_filename = StringVar()
        self.var_todays_date = StringVar()
        self.var_calc_list = StringVar()

        # Function converts contents of calculation list
        # into a string.
        calc_string_text = self.get_calc_string(calc_list)

        # setup dialogue box and background colour
        self.history_box = Toplevel()

        # disable help button
        partner.to_history_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box, width=300,
                                   height=200
                                   )
        self.history_frame.grid()

        self.history_heading_label = Label(self.history_frame,
                                           text="History / Export",
                                           font=("Arial", "16", "bold"),
                                           width=25)
        self.history_heading_label.grid(row=0)

        # Customise text and background colour for calculation
        # area depending on whether all or only some calculations
        # are shown.
        num_calcs = len(calc_list)

        if num_calcs > max_calcs:
            calc_background = "#FFE6CC"  # peach
            showing_all = "Here are your recent calculations " \
                          "({}/{} calculations shown).  Please export" \
                          " your " \
                          "calculations to see your full calculation " \
                          "history".format(max_calcs, num_calcs)

        else:
            calc_background = "#B4FACB"  # pale green
            showing_all = "Below is your calculation history."

        # History text and label
        hist_text = "{}  \n\nAll calculations are shown to " \
                    "the nearest degree.".format(showing_all)
        self.text_instructions_label = Label(self.history_frame,
                                             text=hist_text,
                                             width=40, justify="left",
                                             wraplength=300,
                                             padx=10, pady=10,
                                             )
        self.text_instructions_label.grid(row=1)

        self.all_calcs_label = Label(self.history_frame,
                                     text=calc_string_text,
                                     padx=10, pady=10, bg=calc_background,
                                     width=40, justify="left")
        self.all_calcs_label.grid(row=2)

        # instructions for saving files
        save_text = "Either choose a custom file name (and push " \
                    "<Export>) or simply push <Export> to save your " \
                    "calculations in a text file.  If the " \
                    "filename already exists, it will be overwritten!"
        self.save_instructions_label = Label(self.history_frame,
                                             text=save_text,
                                             wraplength=300,
                                             justify="left", width=40,
                                             padx=10, pady=10)
        self.save_instructions_label.grid(row=3)

        # Filename entry widget, white background to start
        self.filename_entry = Entry(self.history_frame,
                                    font=("Arial", "14"),
                                    bg="#ffffff", width=25)
        self.filename_entry.grid(row=4, padx=10, pady=10)

        self.filename_feedback_label = Label(self.history_frame,
                                             text="",
                                             fg="#9C0000", wraplength=300,
                                             font=("Arial", "12", "bold"))
        self.filename_feedback_label.grid(row=5)

        self.button_frame = Frame(self.history_frame)
        self.button_frame.grid(row=6)

        self.export_button = Button(self.button_frame,
                                    font=("Arial", "12", "bold"),
                                    text="Export", bg="#004C99",
                                    fg="#FFFFFF", width=12,
                                    command=self.make_file)
        self.export_button.grid(row=0, column=0, padx=10, pady=10)

        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#666666",
                                     fg="#FFFFFF", width=12,
                                     command=partial(self.close_history,
                                                     partner))
        self.dismiss_button.grid(row=0, column=1, padx=10, pady=10)

    # change calculation list into a string so that it
    # can be outputted as a label.
    def get_calc_string(self, var_calculations):
        # get maximum calculations to display
        # (was set in __init__ function)
        max_calcs = self.var_max_calcs.get()
        calc_string = ""

        # generate string for writing to file
        # (the oldest calculation first)
        oldest_first = ""
        for item in var_calculations:
            oldest_first += item
            oldest_first += "\n"

        self.var_calc_list.set(oldest_first)

        # work out how many times we need to loop
        # to output either the last five calculations
        # or all the calculations
        if len(var_calculations) >= max_calcs:
            stop = max_calcs

        else:
            stop = len(var_calculations)

        # iterate to all but last item,
        # adding item and line break to calculation string
        for item in range(0, stop):
            calc_string += var_calculations[len(var_calculations)
                                            - item - 1]
            calc_string += "\n"

        calc_string = calc_string.strip()
        return calc_string

    def make_file(self):
        # retrieve filename
        filename = self.filename_entry.get()

        filename_ok = ""
        date_part = self.get_date()

        if filename == "":
            # get date and create default filename
            filename = "{}_temperature_calculations".format(date_part)

        else:
            # check that filename is valid
            filename_ok = self.check_filename(filename)

        if filename_ok == "":
            filename += ".txt"
            success = "Your calculations have  " \
                      "been saved (filename: {})".format(filename)
            self.var_filename.set(filename)
            self.filename_feedback_label.config(text=success,
                                                fg="dark green")
            self.filename_entry.config(bg="#FFFFFF")

            # Write content to file!
            self.write_to_file()

        else:
            self.filename_feedback_label.config(text=filename_ok,
                                                fg="dark red")
            self.filename_entry.config(bg="#F8CECC")

    # retrieves date and creates YYYY_MM_DD string
    def get_date(self):
        today = date.today()

        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        todays_date = "{}/{}/{}".format(day, month, year)
        self.var_todays_date.set(todays_date)

        return "{}_{}_{}".format(year, month, day)

    # checks filename only has letters, numbers
    # and underscores
    @staticmethod
    def check_filename(filename):
        problem = ""

        # Regular expression to check filname is valid
        valid_char = "[A-Za-z0-9_]"

        # iterates through filename and checks each letter.
        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "Sorry, no spaces allowed"

            else:
                problem = ("Sorry, no {}'s allowed".format(letter))
            break

        if problem != "":
            problem = "{}.  Use letters / numbers / " \
                      "underscores only.".format(problem)

        return problem

    # write history to text file
    def write_to_file(self):
        # retrieve date, filename and calculation history...
        filename = self.var_filename.get()
        generated_date = self.var_todays_date.get()

        # set up strings to be written to file
        heading = "**** Shoe Calculations ****\n"
        generated = "Generated: {}\n".format(generated_date)
        sub_heading = "Here is your calculation history " \
                      "(oldest to newest)...\n"
        all_calculations = self.var_calc_list.get()

        to_output_list = [heading, generated,
                          sub_heading, all_calculations]

        # write to file
        # write output to file
        text_file = open(filename, "w+")

        for item in to_output_list:
            text_file.write(item)
            text_file.write("\n")

        # close file
        text_file.close()

    # closes history dialogue (used by button and x at top of dialogue)
    def close_history(self, partner):
        # Put help button back to normal...
        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()
# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Shoe Size Converter")
    DisplayHelp()
    root.mainloop()
