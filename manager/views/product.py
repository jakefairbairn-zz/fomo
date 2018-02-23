from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as amod
import re

@view_function
def process_request(request):
    products = amod.Product.objects.filter(status='A')

    #render the template
    return request.dmp_render('product.html', {
        'products': products,
    })
