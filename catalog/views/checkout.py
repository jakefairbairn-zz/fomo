from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod
from django.shortcuts import redirect
from localflavor.us.us_states import STATE_CHOICES
import re
import math

@view_function
def process_request(request):
    #process the form
    form = CheckoutForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/account/index')

    cart = ''

    #render the template
    return request.dmp.render('checkout.html', {
        'cart': cart,
        'form': form,
    })


class CheckoutForm(Formless):

    def init(self):
        '''Adds the fields for this form'''
        self.fields['ship_address'] = forms.CharField(label='Shipping Address')
        self.fields['ship_city'] = forms.CharField(label='City')
        self.fields['ship_state'] = forms.CharField(label='State')
        self.fields['ship_state'] = forms.ChoiceField(
            label='State', widget=forms.Select, choices=STATE_CHOICES)
        self.fields['ship_zip_code'] = forms.CharField(label='Zip Code')

    # def clean(self):
        # self.user = authenticate(email=self.cleaned_data.get(
        #     'email'), password=self.cleaned_data.get('password'))
        # if self.user is None:
        #     raise forms.ValidationError('Invalid email or password.')
        # return self.cleaned_data

    # def commit(self):
        '''Process the form action'''
        # login(self.request, self.user)
