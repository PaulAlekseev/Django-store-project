import json


def envelop(value: str):
    return "('" + value + "')"

def list_to_string(list):
    string = '~'.join(list)
    return string

def JSON_to_string(json):
    string = '&'.join([
        f"{key}={list_to_string(items)}" for key, items in json.items()
    ])
    return string

def string_to_JSON(string: str):
    result = {}
    arr = [item.split('=')  for item in string.split('&')]
    for product in arr:
        result[product[0]] = product[1].split('~')
    return result
    

