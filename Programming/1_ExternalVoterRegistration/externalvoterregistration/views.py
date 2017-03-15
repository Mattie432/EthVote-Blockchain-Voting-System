from random import randint, choice

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from twisted.python import failure

import network.network_calls as NetworkRequest


def register_ballot(request):
    if 'ballot_id' in request.GET and 'ballot_name' in request.GET and 'ballot_address' in request.GET:
        ballot_id = int(request.GET['ballot_id'])
        ballot_address = request.GET['ballot_address']
        ballot_name = request.GET['ballot_name']

        try:
            result = NetworkRequest.requestRegisterNewBallot(ballot_id, ballot_name, ballot_address).wait(5)
        except Exception as e:
            result = e

        html = "<p>ballot_id = %s </p>" \
               "<p>ballot_name = %s </p>" \
               "<p>ballot_address = %s </p><br>" \
               "<p>Result = %s </p>" % (ballot_id, ballot_name, ballot_address, result)

        if result == True:
            return HttpResponseRedirect("/")
        else:
            return HttpResponse(html)
    else:
        return HttpResponseRedirect("/")



def register_user(request):
    if 'ballot_ids' in request.GET:
        ballot_ids = [int(numeric_string) for numeric_string in (request.GET['ballot_ids']).split(",")]

        result = True

        user_id = randint(0,10000)
        password = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789%^*(-_=+)') for i in range(20)])

        try:
            # Register with applicationserver
            user_success = NetworkRequest.requestRegisterNewUser(user_id, password)
            if not user_success:
                raise Exception()

            for ballot_id in ballot_ids:
                try:
                    result = NetworkRequest.requestRegisterUseridForBallotid(user_id, ballot_id).wait(5)
                except Exception as e:
                    result = e
                    break

            html = "<p>ballot_ids = %s </p>" \
                    "<p>user_id = %s </p>" \
                    "<p>password = %s </p>" \
                   "<p>Result = %s </p>" % (ballot_ids, user_id, password, result)

            return HttpResponse(html)

        except Exception as e:
            return HttpResponse("Failed application register\n\n%s" % e)
    else:
        # return HttpResponseRedirect("/")
        return HttpResponse("Failed")

class Dashboard(View):
    """
    The dashboard page visible immediately after logging in.
    """

    def get(self, request):

        #TODO catch errors http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

        username = None
        form_available_ballots_list = []
        if request.user.is_authenticated():
            username = int(request.user.username)

        try:

            # Get the list of ballots the user is eligable in
            available_ballots_list = NetworkRequest.searchAllAvailableBallots().wait(5)

        except Exception as e:
            # TODO pass err to dashboard.html
            print(e)
            registerd_ballots_list = {}

        return render(request, 'dashboard.html', { 'registerd_ballots_list' : available_ballots_list })
