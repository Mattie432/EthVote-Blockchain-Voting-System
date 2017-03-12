import time
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
from website.network_commands import Request_RetrieveBallots


from crochet import setup, run_in_reactor
setup()

class HomepageRedirect(View):
    """
    Redirects the site root to the dashboard page.
    """
    def get(self, request):
        return HttpResponseRedirect('/dashboard/')

class Dashboard(LoginRequiredMixin, View):
    """
    The dashboard page visible immediately after logging in.
    """

    def __init__(self):
        super().__init__()
        self.ballotregulator_ip       = os.environ[ 'TWISTED_BALLOTREGULATOR_IP' ]
        self.ballotregulator_port       = int(os.environ[ 'TWISTED_BALLOTREGULATOR_PORT' ])


    @run_in_reactor
    @inlineCallbacks
    def searchUser(self, user_id):
        """
        http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

        Blocking call to the ballot server to request the ballots for a particular user.

        :return: EventualResult
        """

        # NOTE: using inline callbacks here so we dont have to write/wait for callbacks.
        destination_deferred = yield TCP4ClientEndpoint(reactor, '172.17.0.2', self.ballotregulator_port)
        connection_deferred = yield connectProtocol(destination_deferred, AMP())
        result_deferred = yield connection_deferred.callRemote(Request_RetrieveBallots, user_id=user_id)

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


    def get(self, request):

        #TODO catch errors http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results
        registerd_ballots_list = self.searchUser(1234).wait(5)

        return render(request, 'dashboard.html', { 'registerd_ballots_list' : registerd_ballots_list })

