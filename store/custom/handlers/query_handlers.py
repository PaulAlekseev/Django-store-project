

def query_to_json(query):
    response = {}
    for product in query:
        response[product.name] = {
            'name': product.name,
            'number': product.number_of_shops,
            'url': product.get_absolute_url(),
            'id': product.id,
        }
    return response
