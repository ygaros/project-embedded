def add_or_sub(number, going_down):
    if going_down:
        return round(number - 0.0001, 6)
    else:
        result = round(number + 0.0001, 6)
        return result


def check_counter(number, going_down):
    edited_counter = number
    edited_going_down = going_down
    if number >= 0.96:
        edited_going_down = True
        edited_counter = 0.96
    if number <= 0:
        edited_going_down = False
        edited_counter = 0

    return edited_counter, edited_going_down
