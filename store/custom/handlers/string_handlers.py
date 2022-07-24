

def envelop(value: str):
    return "('" + value + "')"

def list_to_string(list):
    string = '~'.join(list)
    return string

def string_to_JSON(string: str):
    result = {}
    arr = [item.split('%')  for item in string.split('@')]
    for product in arr:
        result[product[0]] = product[1].split('~')
    return result
    