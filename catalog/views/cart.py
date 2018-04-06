from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod
from django.shortcuts import redirect
import re
import math


@view_function
def process_request(request):
    #render the template

    shopping_cart = ''

    return request.dmp.render('cart.html', {
        'shopping_cart': shopping_cart,
    })
