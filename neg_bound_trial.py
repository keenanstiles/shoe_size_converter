def neg_bound():
    to_units = "UK"
    converted_size = 3

    if (to_units == "US" and converted_size < 3) or \
            (to_units == "EURO" and converted_size < 34) or \
            (to_units == "UK" and converted_size < 3.5):
        error_message = f"Converted size is less than 4 US, \n" \
                        " or equivalent value"

        print(error_message)
        print("shoe_entry.config")
        print("feedback.set")
    else:
        print("Condition not met")


neg_bound()
