from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from account import models as amod
import re

@view_function
def process_request(request):
    # process the form
    form = SignUpForm(request)
    if form.is_valid():

        #login the user
        form.commit()
        return HttpResponseRedirect('/account/index')

    #render the template
    context= {
        'form': form,
    }

    return request.dmp_render('signup.html', context)

class SignUpForm(Formless):
    def init(self):
        self.fields['email'] = forms.CharField(label='Email Address')
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput, label='Password')
        self.fields['password2'] = forms.CharField(widget=forms.PasswordInput, label='Re-enter your password')
        self.fields['first_name'] = forms.CharField(label='First Name')
        self.fields['last_name'] = forms.CharField(label='Last Name')
        self.fields['address'] = forms.CharField(label='Street Address')
        self.fields['city'] = forms.CharField(label='City')
        self.fields['zipcode'] = forms.CharField(label='ZipCode')
        self.fields['state'] = forms.CharField(label='State')

    #Anything dealing with 2 fields (like password and password2), do it in the general clean field instead of individually
    def clean(self):
        #compare the two passwords and make sure they match
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('The passwords do not match.')

        return self.cleaned_data

    def clean_email(self):
        email_c = self.cleaned_data['email']

        if len(amod.User.objects.filter(email=email_c)) == 0:
            return email_c
        else:
            raise forms.ValidationError('This email is already in use. Please use a different one.')

    def clean_password(self):
        p1 = self.cleaned_data['password']
        #make sure the password is at least 8 characters long
        if len(p1) < 8:
            raise forms.ValidationError('The password must be at least 8 characters in length')
        else:
            #make sure that the password has a number in it
            if re.search('[0-9]', p1) is not None:
                return p1
            else:
                raise forms.ValidationError('The password must contain a number.')

    def commit(self):
        '''Process the form action'''
        #create the new user
        user = amod.User.objects.create_user(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))

        #authenticate the user
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))

        #log the user in
        login(self.request, self.user)
