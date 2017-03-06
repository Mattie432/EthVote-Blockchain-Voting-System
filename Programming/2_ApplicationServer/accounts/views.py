from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from accounts.forms import InitialLogin


def custom_login(request, template_name, authentication_form ):
    """
    Custom login view that redirects to the dashboard iff the
    user is already authenticated.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return login(request, template_name, authentication_form)

def initial_login(request):
    """
    Initial login view shown when the user still needs to enter more
    details about thir account.
    """
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = InitialLogin(request.user, request.POST)

            if form.is_valid():

                new_password=form.cleaned_data['password1']
                email=form.cleaned_data['email']
                first_name=form.cleaned_data['first_name']
                last_name=form.cleaned_data['last_name']

                request.user.set_password(new_password)
                request.user.email=email
                request.user.first_name=first_name
                request.user.last_name=last_name
                request.user.force_enterDetails=False   # No longer force details to be entered
                request.user.save()

                return HttpResponseRedirect('/')
        else:
            form = InitialLogin(request.user)

        return render(request, 'initial_login.html', {'form' : form})
    else:
        return HttpResponseRedirect('login/')
