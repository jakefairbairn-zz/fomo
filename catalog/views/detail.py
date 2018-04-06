from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod
from django.shortcuts import redirect
import re
import math


@view_function
def process_request(request, product: cmod.Product):

    if product is None:
        return redirect('/catalog/index')

    # process the form
    form = Cart(request, product=product)

    if form.is_valid():
        print(form)
        form.commit()
        return HttpResponseRedirect('/catalog/index')

    # remove the current object from the last_five list, if it exists
    # this prevents it from showing up as the current object as well as in the last_five list
    if product in request.last_five:
        request.last_five.remove(product)

    # add the current object to the front of the last_five list
    request.last_five.insert(0, cmod.Product.objects.get(id=product.id))

    return request.dmp.render('detail.html', {
        'product': product,
        'product_images': product.image_urls(),
        'form': form,
    })


class Cart(Formless):
    # Change the text of the submit button
    submit_text = 'Buy Now'
    field_css = ['form-inline']

    def init(self):
        '''Adds the fields for this form'''

        # Display the quantity input if it is a bulk product, else hide the field
        if self.product.__class__.__name__ == "BulkProduct":
            self.fields['quantity'] = forms.IntegerField(
                label='Quantity', initial=1, max_value=self.product.quantity, min_value=1)
        else:
            self.fields['quantity'] = forms.IntegerField(
                initial=1, widget=forms.HiddenInput())

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        # If the product is already in the cart, just add the new quantity to the existing quantity in the cart
        if self.cart.get_item(self.product) is not None:
            quantity += self.cart.get_item(self.product).quantity

        # If it is a bulk product, verify that the quantity is not greater than the amount available
        if self.product.__class__.__name__ == 'BulkProduct':
            if quantity > self.product.quantity:
                raise forms.ValidationError(
                    'Please choose a quantity less than ' + self.product.quantity + '.')
        # If not a bulk product, make sure that the item is not added to the cart again
        else:
            if quantity > 1:
                raise forms.ValidationError(
                    'This item is already in your cart')

        return quantity

    def commit(self):
        '''Process the form action'''
        # Create the new OrderItem with the quantity ordered
        quantity = self.cleaned_data.get('quantity')
        self.cart.get_item(self.product, quantity, create=True)
