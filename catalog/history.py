from catalog import models as cmod
from pprint import pprint
from collections import OrderedDict

class LastFiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        #get all of the product ids that have been viewed in the session (set to None if empty)
        session_product_ids = list(dict.fromkeys(request.session.get('session_product_ids', [])))

        #convert the product ids to product objects
        last_five_list = []
        for product_id in session_product_ids:
            last_five_list.append(cmod.Product.objects.get(id = product_id))

        #store the product objects in the last_five session variable
        request.last_five = last_five_list

        #load the view
        response = self.get_response(request)

        #reset the session_product_ids list
        session_product_ids = []

        #recreate the session_product_ids list with the new objects
        for product in request.last_five[:6]:
            session_product_ids.append(product.id)

        #set the session session_product_ids list
        request.session['session_product_ids'] = session_product_ids

        return response
