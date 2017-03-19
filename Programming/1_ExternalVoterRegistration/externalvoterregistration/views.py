from random import randint, choice

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from twisted.python import failure
import datetime

import network.network_calls as NetworkRequest


def register_ballot(request):
    if 'ballot_name' in request.GET and 'ballot_options' and 'ballot_end_date' in request.GET:
        ballot_name = (request.GET['ballot_name'])
        ballot_end_date = request.GET['ballot_end_date']
        ballot_end_date_epoch = int(datetime.datetime.strptime(ballot_end_date,'%Y-%m-%d').strftime('%s')) # Convert to sec since epoc
        ballot_options = str(request.GET['ballot_options']).split(",")

        try:
            ballot_address = NetworkRequest.requestRegisterNewBallot(ballot_name, ballot_options, ballot_end_date_epoch).wait(300)
        except Exception as e:
            ballot_address = e

        html = "<p>ballot_name = %s </p>" \
               "<p>ballot_end_date = %s / %s</p>" \
               "<p>ballot_address = %s </p><br>"  % (ballot_name, ballot_end_date, ballot_end_date_epoch, ballot_address)

        if ballot_address is not None:
            return HttpResponseRedirect("/")
        else:
            return HttpResponse(html)
    else:
        return HttpResponseRedirect("/")



def register_user(request):
    if 'ballot_ids' in request.GET:

        ballot_ids_string = request.GET['ballot_ids']
        ballot_ids = [] if len(ballot_ids_string) == 0 else [ int(numeric_string) for numeric_string in (ballot_ids_string).split(",")]

        result = True

        user_id = randint(10000,99999)
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
