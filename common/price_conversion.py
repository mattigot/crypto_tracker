
def truncate_float(float_number, decimal_places):
    multiplier = 10 ** decimal_places
    return int(float_number * multiplier) / multiplier

def format_float(num):
    result = 0
    i = 2

    if num == 0:
        return num

    while result == 0:
        result = truncate_float(num, i)
        i += 1

    return result