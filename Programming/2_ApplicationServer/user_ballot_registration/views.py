from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import random
from Crypto.PublicKey import RSA
from random import SystemRandom
from Crypto.Hash import SHA256


import network.network_calls as NetworkRequest

class RegisterForBallot(LoginRequiredMixin, View):

    def get(self, request, param_ballot_id):
        try:
            ballot_id = int(param_ballot_id)
            username = int(request.user.username)
        except ValueError:
            raise Http404("Couldnt cast ballot_id or username to int")

        # Get public key ascociated with this ballot
        ballot_publicKey = NetworkRequest.getBallotPublicKey(ballot_id).wait(5)

        # Create our RSA key object
        public_key = RSA.importKey(ballot_publicKey)

        # Generate our token
        token = str(random.getrandbits(128)).encode()

        # Blind our token
        random_number = SystemRandom().randrange(public_key.n >> 10, public_key.n)
        blinded_token = public_key.blind(token, random_number)

        # Request the OnlineAccountVerifier to sign this token
        signed_blind_token = NetworkRequest.requestSignOfToken(username, ballot_id, blinded_token).wait(5)

        return HttpResponse(signed_blind_token)


