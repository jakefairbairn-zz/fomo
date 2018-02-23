from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as amod
from pprint import pprint
import re

@view_function
def process_request(request, product:amod.Product):
    #set the product status to Inactive
    product.status = 'I'
    #save the status change
    product.save()

    #get all active products
    products = amod.Product.objects.filter(status='A')

    #render the product list template
    return request.dmp_render('product.html', {
        'products': products,
    })
