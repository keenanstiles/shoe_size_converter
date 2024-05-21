def check_shoe():

    try:

        response = "x"
        min_value = 4
        # checks if entered integer is above 4 US, if not, then runs error response

        if response < min_value:
            # self.var_has_error.set("yes")
            print(" ERROR: Number entered is smaller than 4 US")
            print("FEEDBACK: Enter a number greater than 4 US")
            # self.output_answer()
            # return None
        else:
            # if all is well ten no errors and conversion is set to run
            print("ERROR: No errors")
            # return number to be
            # converted and enable history button
            print("BUTTON: Enable history")
            # self.output_answer()
            return response
    except ValueError:
        # ValueError checks for alphabetical inputs, if present, runs error response
        print("ERROR: code has value error")
        print("FEEDBACK: enter a valid number")
        # return None


check_shoe()