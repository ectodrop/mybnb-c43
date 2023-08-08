import re

# sets the "err" attribute of a function to some message
def attr(err :str):
    def wrapper(func):
        func.err = err
        def or_blank(x):
            return func(x) or x == "" 
        func.or_blank = or_blank
        func.or_blank.err = err + " (or blank)"
        return func
    
    return wrapper

def is_string(x :str):
    return True

@attr("Must be an integer")
def is_int(x :str):
    return x.isdigit()

@attr("Must be a float")
def is_float(x: str):
    try:
        float(x)
        return True
    except:
        return False

"""
string must be non empty
"""
@attr("Must be a non empty string")
def non_empty(x: str):
    return x != ""

"""
Follows A#B#C# format
"""
@attr("Must be of the format A#A#A#")
def is_zipcode(x :str):
    is_zipcode.err = "Must enter a string in A#A#A# format"
    return bool(re.search("[A-Z]\d[A-Z]\d[A-Z]\d", x))

"""
check if input var is in container
"""
def is_contained(container):
    container = {str(elem) for elem in container}
    err = f"Answer must be one of [{', '.join(container)}]"
    @attr(err)
    def func(x :str):
        if len(container) == 0:
            return True
        return x in container
    return func

"""
return if input is a digit between 1 and 5
"""
@attr("Must be an integer between 1 and 5")
def is_rating(x: str):
    return is_int(x) and 1 <= int(x) <= 5


"""
must be in y-m-d format
"""
@attr("Must be a date in YYYY-mm-dd format")
def is_date(x : str):
    return bool(re.search("\d\d\d\d-\d\d-\d\d", x))

@attr("Must be y or n")
def yes_or_no(x :str):
    return x.lower() in ["y","n"]

def in_range(lower:float, upper:float):
    @attr(f"Must be a number between {lower} and {upper}")
    def _in_range(x :str):
        return is_float(x) and lower <= float(x) <= upper
    return _in_range

@attr("Must be a 16-digit number")
def is_valid_cc(cc: str):
    return cc.isnumeric() and len(cc) == 16