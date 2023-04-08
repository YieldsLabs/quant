def determine_type(value):
    try:
        int_value = int(value)
        if str(int_value) == value:
            return int_value
    except ValueError:
        pass

    return float(value)
