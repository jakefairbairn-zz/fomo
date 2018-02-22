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
    print(product)
    product.status = 'I'
    product.save()
    products = amod.Product.objects.filter(status='A')

    #render the template
    return request.dmp_render('list.html', {
        'products': products,
    })
