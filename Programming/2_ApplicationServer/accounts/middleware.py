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
            re.match(r'^/?', request.path) and \
            not re.match(r'^/password_change/?', request.path) and \
            not re.match(r'^/logout/?', request.path) and \
            not re.match(r'^/login/?', request.path):

            # Retrieve whether the user has entered the extended details.
            requireMoreDetails = request.user.getForceEnterDetails()
            if requireMoreDetails == False:
                # Redirect to the page to enter more details
                return HttpResponseRedirect('/password_change/')

        # Call the view

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
