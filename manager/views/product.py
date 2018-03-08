from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod
import re

@view_function
def process_request(request):
    products = cmod.Product.objects.filter(status='A')

    #render the template
    return request.dmp.render('product.html', {
        'products': products,
    })
