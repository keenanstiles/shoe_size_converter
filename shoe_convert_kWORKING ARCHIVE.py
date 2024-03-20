
from tkinter import *
from tkinter import ttk


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
        self.temp_frame = Frame(self.converter_box, width=300, height=200)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Shoe Size Converter",
                                  font=("Arial", "16", "bold")
                                  )
        self.temp_heading.grid(row=0)

        instructions = "Please select your desired size types from the drop-downs below and " \
                       "then press convert :)"
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
                                  fg="#228b22")
        self.output_label.grid(row=3)

        # Input size label
        self.input_size_label = Label(self.temp_frame, text="Input size:")
        self.input_size_label.grid(row=4)

        # Conversion dropdown menu
        self.from_units = StringVar()
        self.from_units.set("US")  # default value

        self.dropdown_frame = Frame(self.temp_frame)
        self.dropdown_frame.grid(row=5)

        # Updated dropdown menus
        self.from_dropdown = ttk.Combobox(self.dropdown_frame, textvariable=self.from_units, font=dropdown_font,
                                          state="readonly")
        self.from_dropdown['values'] = ("US", "EURO")
        self.from_dropdown.grid(row=0, column=0, padx=5, pady=5)

        # Output size label
        self.output_size_label = Label(self.temp_frame, text="Output size:")
        self.output_size_label.grid(row=6)

        # Conversion dropdown menu
        self.to_units = StringVar()
        self.to_units.set("EURO")  # default value

        self.to_dropdown = ttk.Combobox(self.temp_frame, textvariable=self.to_units, font=dropdown_font,
                                        state="readonly")
        self.to_dropdown['values'] = ("US", "EURO")
        self.to_dropdown.grid(row=7, padx=5, pady=5)

        # Radio buttons for selecting men's or women's sizing
        self.sizing_var = StringVar()
        self.sizing_var.set("Men's")
        self.sizing_frame = Frame(self.temp_frame)
        self.sizing_frame.grid(row=8)
        self.men_sizing = Radiobutton(self.sizing_frame, text="Men's", variable=self.sizing_var, value="Men's")
        self.men_sizing.grid(row=0, column=0, padx=5, pady=5)
        self.women_sizing = Radiobutton(self.sizing_frame, text="Women's", variable=self.sizing_var, value="Women's")
        self.women_sizing.grid(row=0, column=1, padx=5, pady=5)

        # Convert button
        self.convert_button = Button(self.temp_frame,
                                     text="Convert",
                                     bg="#0066CC",
                                     fg="white",
                                     font=("Arial", "12", "bold"),
                                     width=12,
                                     command=self.temp_convert)
        self.convert_button.grid(row=9, columnspan=2, padx=5, pady=5)

        # Conversion rates
        self.conversion_rates = {
            "US Men's": {
                "EURO Men's": 33,
                "US Men's": 0
            },
            "US Women's": {
                "EURO Women's": 31,
                "US Women's": 0
            },
            "EURO Men's": {
                "US Men's": -33,
                "EURO Men's": 0
            },
            "EURO Women's": {
                "US Women's": -31,
                "EURO Women's": 0
            },
            "CENTIMETERS": {
                "US Men's": 8,
                "US Women's": 8
            }
        }

    def temp_convert(self):
        to_convert = self.check_temp(0)
        if to_convert is not None:
            from_units = self.from_units.get()
            to_units = self.to_units.get()
            sizing_var = self.sizing_var.get()
            converted_size, message = self.convert_size(from_units, to_units, sizing_var, to_convert)
            self.output_label.config(text=message)
            self.all_calculations.append(message)

    def check_temp(self, min_value):
        try:
            response = float(self.temp_entry.get())
            if response < min_value:
                raise ValueError
            return response
        except ValueError:
            error = "Please enter a number greater than {}".format(min_value)
            self.output_label.config(text=error, fg="#9C0000")
            return None

    def convert_size(self, from_units, to_units, sizing_var, to_convert):

        from_key = f"{from_units} {sizing_var}"

        to_key = f"{to_units} {sizing_var}"

        found_conversion_rate = self.conversion_rates[from_key][to_key]

        converted_size = to_convert + found_conversion_rate

        return converted_size, f"{to_convert} {from_units} {sizing_var} is {converted_size} {to_units} {sizing_var}"

    def close_help(self):
        self.converter_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Information Screen")
    DisplayHelp()
    root.mainloop()
