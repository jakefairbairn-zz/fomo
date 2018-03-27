from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from formlib import Formless
from django import forms
from catalog import models as amod
import re
from django.forms.models import model_to_dict
from catalog import models as amod

@view_function
def process_request(request):
    #process the form
    form = CreateProductForm(request)

    if form.is_valid():
        #comit the form
        form.commit()
        #redirect to the product list page
        return HttpResponseRedirect('/manager/product')

    #render the template
    return request.dmp.render('create.html', {
        'form': form,
    })

class CreateProductForm(Formless):
    def init(self):
        self.fields['type'] = forms.ChoiceField(label='Type', widget=forms.Select, choices=amod.Product.TYPE_CHOICES)
        self.fields['name'] = forms.CharField(label='Name')
        self.fields['status'] = forms.ChoiceField(label='Status', widget=forms.Select, choices=amod.Product.STATUS_CHOICES)
        self.fields['description'] = forms.CharField(label='Description', widget=forms.Textarea)
        self.fields['pid'] = forms.CharField(label='PID', required=False)
        self.fields['price'] = forms.CharField(label='Price')
        self.fields['category'] = forms.ModelChoiceField(label='Category', queryset=amod.Category.objects.all(), empty_label=None)
        self.fields['quantity'] = forms.IntegerField(label='Quantity', required=False)
        self.fields['reorder_trigger'] = forms.IntegerField(label="Reorder Trigger", required=False)
        self.fields['reorder_quantity'] = forms.IntegerField(label="Reorder Quantity", required=False)
        self.fields['max_rental_days'] = forms.IntegerField(label="Max Rental Days", required=False)
        self.fields['retire_date'] = forms.DateField(label="Retire Date", required=False)

    def clean(self):
        #clean individual product
        if self.cleaned_data['type'] == "IndividualProduct":
            if self.cleaned_data['pid'] == '':
                raise forms.ValidationError('A PID is required for the product.')

        #clean bulk product
        elif self.cleaned_data['type'] == "BulkProduct":
            if self.cleaned_data['quantity'] == None:
                raise forms.ValidationError('A quantity is required for the product.')
            if self.cleaned_data['reorder_trigger'] == None:
                raise forms.ValidationError('A reorder trigger is required for the product.')
            if self.cleaned_data['reorder_quantity'] == None:
                raise forms.ValidationError('A reorder quantity is required for the product.')

        #clean rental product
        elif self.cleaned_data['type'] == "RentalProduct":
            if self.cleaned_data['pid'] == '':
                raise forms.ValidationError('A PID is required for the product.')
            if self.cleaned_data['max_rental_days'] == None:
                raise forms.ValidationError('A max rental days is required for the product.')


        #return the cleaned data
        return self.cleaned_data

    def commit(self):
        '''Process the form action'''

        #create product and set fields for individual products
        if self.cleaned_data['type'] == "IndividualProduct":
            prod = amod.IndividualProduct()
            prod.pid=self.cleaned_data['pid']

        #create product and set fields for bulk products
        elif self.cleaned_data['type'] == "BulkProduct":
            prod = amod.BulkProduct()
            prod.quantity=self.cleaned_data['quantity']
            prod.reorder_trigger=self.cleaned_data['reorder_trigger']
            prod.reorder_quantity=self.cleaned_data['reorder_quantity']

        #create product and set fields for rental products
        elif self.cleaned_data['type'] == "RentalProduct":
            prod = amod.RentalProduct()
            prod.pid=self.cleaned_data['pid']
            prod.max_rental_days=self.cleaned_data['max_rental_days']
            prod.retire_date=self.cleaned_data['retire_date']

        #set the common fields for all products
        prod.name=self.cleaned_data['name']
        prod.status=self.cleaned_data['status']
        prod.description=self.cleaned_data['description']
        prod.price=self.cleaned_data['price']
        prod.category=self.cleaned_data['category']

        #save the updated data for the objects
        prod.save()
