from django.http import HttpResponseRedirect
import re


class InitialLoginChangeMiddleware(object):
    """
    This class intercepts page requests and determines if an authenticated
    user is requied to enter more details about themselves. This should be
    so that we force a password change and personal detail entering when
    a registered voter first logs into the webapp.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        """
        If a user is authenticated check if they need to enter more details. Ignore
        certain urls so that a user who has not entered these details can only access
        a subset of the pages.
        """
        if request.user.is_authenticated() and \
            request.user.getForceEnterDetails() and \
            re.match(r'^/?', request.path) and \
            not re.match(r'^/initial_login/?', request.path) and \
            not re.match(r'^/logout/?', request.path) and \
            not re.match(r'^/login/?', request.path):

                # Redirect to the page to enter more details
                return HttpResponseRedirect('/initial_login/')

        """
        If the user does not have the force_enterDetails flag set,
        then dont allow access to the initial login page.
        """
        if request.user.is_authenticated() and \
            not request.user.getForceEnterDetails() and \
            re.match(r'^/initial_login/?', request.path):

                # Redirect to the page to enter more details
                return HttpResponseRedirect('/')


        # Call the view

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
