from catalog import models as cmod
from pprint import pprint
from collections import OrderedDict

class LastFiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        #get all of the product ids that have been viewed in the session (set to None if empty)
        session_product_ids = list(dict.fromkeys(request.session.get('session_product_ids', [])))
        print("START IDS")
        print(session_product_ids)

        #determine the number of objects to add to the last_five_list
        if not session_product_ids:
            list_size = 0
        elif len(session_product_ids) > 6:
            list_size = 6
        else:
            list_size = len(session_product_ids)

        #convert the product ids to product objects
        last_five_list = []
        for i in range(list_size):
            last_five_list.append(cmod.Product.objects.get(id = session_product_ids[i]))

        #store the product objects in the last_five session variable
        request.last_five = last_five_list
        print("PRODUCTS BEFORE RESPONSE")
        for product in request.last_five:
            pprint(product.id)

        #load the view
        response = self.get_response(request)

        #reset the session_product_ids list
        session_product_ids = []

        #recreate the session_product_ids list with the new objects
        for product in request.last_five:
            session_product_ids.append(product.id)

        #set the session session_product_ids list
        request.session['session_product_ids'] = session_product_ids

        return response
