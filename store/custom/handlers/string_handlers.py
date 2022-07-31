

def string_to_dictionary(string: str):
    """
    Converts filters from query string to dictionary
    """
    result = {}
    arr = [item.split('%') for item in string.split('@')]
    for product in arr:
        result[product[0]] = product[1].split('~')
    return result
