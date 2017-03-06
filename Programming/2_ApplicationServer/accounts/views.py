from django.contrib.auth.views import login
from django.http import HttpResponseRedirect

"""
Custom login view that redirects to the dashboard iff the
user is already authenticated.
"""
def custom_login(request, template_name, authentication_form ):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return login(request, template_name, authentication_form)
