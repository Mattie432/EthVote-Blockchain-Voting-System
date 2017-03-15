import time

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from twisted.internet import reactor, defer
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.protocols.amp import AMP
import pickle, os
from website.network_commands import Request_RetrieveSignBlindTokenForUser, Request_RetrieveRegisteredUserBallots


from crochet import setup, run_in_reactor
setup()

class HomepageRedirect(View):
    """
    Redirects the site root to the dashboard page.
    """
    def get(self, request):
        return HttpResponseRedirect('/dashboard/')


class RegisterForBallot(LoginRequiredMixin, View):

    def get(self, request, ballot_id):
        try:
            offset = int(ballot_id)
        except ValueError:
            raise Http404("Coudnt cast ballot_id to int")






        html = "Request for ballot id='%s'" % ballot_id
        return HttpResponse(html)



class Dashboard(LoginRequiredMixin, View):
    """
    The dashboard page visible immediately after logging in.
    """

    def __init__(self):
        super().__init__()
        self.ballotregulator_ip       = os.environ[ 'TWISTED_BALLOTREGULATOR_IP' ]
        self.ballotregulator_port       = int(os.environ[ 'TWISTED_BALLOTREGULATOR_PORT' ])
        self.accountverifier_ip       = os.environ[ 'TWISTED_ACCOUNTVERIFIER_IP' ]
        self.accountverifier_port       = int(os.environ[ 'TWISTED_ACCOUNTVERIFIER_PORT' ])


    @run_in_reactor
    @inlineCallbacks
    def searchUserAvailableBallots(self, user_id):
        """
        http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

        Blocking call to the ballot server to request the ballots for a particular user.

        :return: EventualResult
        """

        # NOTE: using inline callbacks here so we dont have to write/wait for callbacks.
        destination_deferred = yield TCP4ClientEndpoint(reactor, self.ballotregulator_ip, self.ballotregulator_port)
        connection_deferred = yield connectProtocol(destination_deferred, AMP())
        result_deferred = yield connection_deferred.callRemote(Request_RetrieveRegisteredUserBallots, user_id=user_id)

        def format_results(pickled_result):

            # First unpickle the results.
            result = pickle.loads(pickled_result['ok'])

            # Transform the list results into a dictionary.
            record_list = []
            for record in result:
                mapper = {}
                mapper['user_id'] = record[0]
                mapper['ballot_id'] = record[1]
                mapper['timestamp'] = record[2]
                mapper['ballot_name'] = record[3]
                mapper['ballot_address'] = record[4]
                # Append each row's dictionary to a list
                record_list.append(mapper)

            return record_list

        # Inlinecallback return value.
        returnValue(format_results(result_deferred))

    @run_in_reactor
    @inlineCallbacks
    def searchUserRegisteredBallots(self, user_id):
        """
        http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

        Blocking call to the acountverifier server to request the ballots for a particular user has already registered for..

        :return: EventualResult
        """

        # NOTE: using inline callbacks here so we dont have to write/wait for callbacks.
        destination_deferred = yield TCP4ClientEndpoint(reactor, self.accountverifier_ip, self.accountverifier_port)
        connection_deferred = yield connectProtocol(destination_deferred, AMP())
        result_deferred = yield connection_deferred.callRemote(Request_RetrieveSignBlindTokenForUser, user_id=user_id)

        def format_results(pickled_result):

            # First unpickle the results.
            result = pickle.loads(pickled_result['ok'])

            # Transform the list results into a dictionary.
            record_list = []
            for record in result:
                mapper = {}
                mapper['token_request_id'] = record[0]
                mapper['blind_token_hash'] = record[1]
                mapper['user_id'] = record[2]
                mapper['ballot_id'] = record[3]
                mapper['timestamp'] = record[4]
                # Append each row's dictionary to a list
                record_list.append(mapper)

            return record_list

        # Inlinecallback return value.
        returnValue(format_results(result_deferred))

    def get(self, request):

        #TODO catch errors http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

        username = None
        if request.user.is_authenticated():
            username = int(request.user.username)
            print("Username : %s" % username)
        try:
            form_available_ballots_list = []

            # Get the list of ballots the user is eligable in
            available_ballots_list = self.searchUserAvailableBallots(username).wait(5)

            # Get list of ballots the user is already registered for.
            registerd_ballots_list = self.searchUserRegisteredBallots(username).wait(5)

            for available_ballot in available_ballots_list:
                temp = available_ballot
                test = [item for item in registerd_ballots_list if (item["user_id"] == username and item['ballot_id'] == available_ballot['ballot_id'])]
                temp['registered'] = True if len(test) else False
                form_available_ballots_list.append(temp)


        except Exception as e:
            # TODO pass err to dashboard.html
            print(e)
            registerd_ballots_list = {}

        return render(request, 'dashboard.html', { 'registerd_ballots_list' : form_available_ballots_list })

