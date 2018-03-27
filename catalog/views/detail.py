from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod
from django.shortcuts import redirect
import re
import math

@view_function
def process_request(request, product:cmod.Product):

    if product is None:
        return redirect('/catalog/index')

    #remove the current object from the last_five list, if it exists
    #this prevents it from showing up as the current object as well as in the last_five list
    if product in request.last_five:
        request.last_five.remove(product)

    #add the current object to the front of the last_five list
    request.last_five.insert(0, cmod.Product.objects.get(id = product.id))

    return request.dmp.render('detail.html', {
        'product': product,
        'product_images': product.image_urls(),
    })
