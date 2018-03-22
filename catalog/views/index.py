from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from formlib import Formless
from django import forms
from catalog import models as cmod
import re
import math

@view_function
def process_request(request, category_id = 0):

    #get products based on the category select (if any)
    if str(category_id) == '0' or category_id == None:
        active_category = "Products"
        num_pages = math.ceil(len(cmod.Product.objects.all())/6)
    else:
        active_category = cmod.Category.objects.get(id=category_id)
        num_pages = math.ceil(len(cmod.Product.objects.filter(category=active_category))/6)

    #load the template
    return request.dmp.render('index.html', {
        'active_category': active_category,
        jscontext('category_id'): category_id,
        jscontext('num_pages'): num_pages
    })

@view_function
def inner(request, category_id = 0, page_number = 1):

    if str(category_id) == '0' or category_id == None:
        products = cmod.Product.objects.all()[(int(page_number)*6)-6:int(page_number)*6]
    else:
        category_name = cmod.Category.objects.get(id = category_id)
        products = cmod.Product.objects.filter(category=category_name)[(int(page_number)*6)-6:int(page_number)*6]


    #load the template
    return request.dmp.render('index.inner.html', {
        'products': products,
    })
