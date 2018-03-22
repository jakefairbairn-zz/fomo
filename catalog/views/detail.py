from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from formlib import Formless
from django import forms
from catalog import models as cmod
from django.shortcuts import redirect
from collections import deque
from pprint import pprint
import re
import math

@view_function
def process_request(request, product:cmod.Product):

    if product is None:
        return redirect('/catalog/index')

    #remove the current object from the last_five list, if it exists
    #this prevents it from showing up as the current object as well as in the last_five list
    for last_product in request.last_five:
        if last_product.id == product.id:
            request.last_five.remove(last_product)

    #add the current object to the front of the last_five list
    request.last_five.insert(0, cmod.Product.objects.get(id = product.id))

    return request.dmp.render('detail.html', {
        'product': product,
        'product_images': product.image_urls()
    })
