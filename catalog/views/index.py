from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod
import re

@view_function
def process_request(request, category_id = 0):

    #get the categories for the sidebar
    categories = cmod.Category.objects.all()
    print("category_id")
    print(category_id)

    #get products based on the category select (if any)
    if str(category_id) == '0' or category_id == None:
        active_category = "Products"
    else:
        active_category = cmod.Category.objects.get(id=category_id)

    #load the template
    return request.dmp.render('index.html', {
        'categories': categories,
        'active_category': active_category
    })
