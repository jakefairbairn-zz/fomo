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
    #process the form
    form = LoginForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/account/index')

    #render the template
    return request.dmp.render('login.html', {
        'form': form,
    })


class LoginForm(Formless):

    def init(self):
        '''Adds the fields for this form'''
        self.fields['email'] = forms.CharField(label='Email Address')
        self.fields['password'] = forms.CharField(label='Password', widget=forms.PasswordInput)
        self.user = None

    #Anything dealing with 2 fields (like password and password2), do it in the general clean field instead of individually
    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')
        return self.cleaned_data

    def commit(self):
        '''Process the form action'''
        login(self.request, self.user)
