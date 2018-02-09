from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django_mako_plus import view_function

@view_function
def process_request(request):
    #perform the logout
    logout(request)
    #redirect to the index homepage
    return HttpResponseRedirect('/homepage/index')
