from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as amod
import re

@view_function
def process_request(request, prod:amod.Product):
    #process the form
    form = ProductForm(request,
                        initial={
                            'name' = prod.name,
                            'price' = prod.price,
                            'status' = prod.status,
                            'category' = prod.category
                        })
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/manager/index')

    #render the template
    return request.dmp_render('edit.html', {
        'form': form,
    })


class ProductForm(Formless):

    def init(self):
        '''Adds the fields for this form'''
        self.fields['name'] = forms.CharField(label='Name')
        self.fields['price'] = forms.CharField(label='Price')
        self.fields['status'] = forms.CharField(label='Status')
        self.fields['category'] = forms.CharField(label='Category')

    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')
        return self.cleaned_data

    def commit(self):
        '''Process the form action'''
        login(self.request, self.user)
