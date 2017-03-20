from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

import network.network_calls as NetworkRequest
from user_ballot_registration.models import RegisterAddress


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

    def get(self, request):

        #TODO catch errors http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

        username = None
        form_available_ballots_list = []
        if request.user.is_authenticated():
            username = int(request.user.username)

        try:
            # Get the list of ballots the user is eligable in
            available_ballots_list = NetworkRequest.searchUserAvailableBallots(username).wait(5)

            # Get our voter adddress for this ballot.

            for available_ballot in available_ballots_list:
                temp = available_ballot

                database_results = RegisterAddress.objects.filter(
                    user=request.user,
                    ballot_id=available_ballot['ballot_id']
                )

                if(len(database_results) > 0):
                    registerd_ballots_list = NetworkRequest.searchUserAddressRegisterVote(database_results[0].voter_address).wait(5)
                else:
                    registerd_ballots_list = []

                local_registered_address = True if len(database_results) else False

                remote_registered_userid = local_registered_address and  True if \
                                                len([item for item in registerd_ballots_list if item['ballot_id'] == available_ballot['ballot_id']]) else False

                # First check we havent already recieved a signed token

                temp['registered'] = remote_registered_userid and local_registered_address
                try: #See if we have a requested cookie
                    temp['requested'] = request.session['register_ballot_' + str(temp['ballot_id'])]
                except:
                    temp['requested'] = None
                form_available_ballots_list.append(temp)

        except Exception as e:
            # TODO pass err to dashboard.html
            print(e)
            registerd_ballots_list = {}

        return render(request, 'dashboard.html', { 'registerd_ballots_list' : form_available_ballots_list })

