from django import forms
from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone

@view_function
def process_request(request):
    #process the form
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            #do the work of the form
            #make the payment
            #create the user
            return HttpResponseRedirect('/')
    else:
        print("ELSE")
        form = TestForm()
        print(form)

    context = {
        'form': form,
    }
    print(form)
    print(context)
    return request.dmp_render('testform.html', context)


class TestForm(forms.Form):
    def init(self):
        self.fields['favorite_ice_cream'] = forms.CharField(label='Favorite Ice Cream')
        self.fields['renewal_date'] = forms.DateField(label='Renewal')
        self.fields['age'] = forms.IntegerField(label='Age')


    # All clean_ functions are called by is_valid
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            print("Age is less than 18: " + age)
        # MUST RETURN, OTHERWISE DATA IS SET TO 'NONE'
        return age

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if password.length < 8:
    #         etc.

    #Anything dealing with 2 fields (like password and password2), do it in the general clean field instead of individually
    def clean(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('Please ensure the passwords match.')
