import os

from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template.defaultfilters import register
from django.views import View
import random
from Crypto.PublicKey import RSA
from random import SystemRandom
from Crypto.Hash import SHA256
from user_ballot_registration.models import *
from network import network_exceptions as NetworkExceptions
from ecdsa import SigningKey, SECP256k1
import hashlib
import sha3
from web3 import Web3, KeepAliveRPCProvider, IPCProvider
import datetime
from ethereum.ethereum import Ethereum

import network.network_calls as NetworkRequest

@register.filter()
def return_item(l, i):
    try:
        return l[i]
    except:
        return None

@register.filter
def running_total(role_total):
     return sum(role_total)

@register.filter
def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)

class RegisterForBallot(LoginRequiredMixin, View):

    def __init__(self):
        super().__init__()
        self.ethereum = Ethereum()

    def post(self, request, param_ballot_id):
        try:
            ballot_id = int(param_ballot_id)
            username = int(request.user.username)
            password = request.POST['register_password']
        except ValueError:
            raise Http404("Couldn't cast ballot_id or username to int")

        (token, signed_token) = self.request_token_sign(ballot_id, request.user, username)

        (voter_address, voter_private_key, voter_public_key) = self.request_address_register(request.user, ballot_id, token, signed_token, password)

        request.session['register_ballot_' + str(ballot_id)] = datetime.datetime.now().strftime('%s') # Save our request time to the session.

        return HttpResponseRedirect('/register_for_ballot/' + str(ballot_id))



    def get(self, request, param_ballot_id):
        try:
            ballot_id = int(param_ballot_id)
            username = int(request.user.username)
        except ValueError:
            raise Http404("Couldn't cast ballot_id or username to int")

        (token, signed_token) = request_token_sign_check_local(ballot_id, request.user)

        (voter_address, voter_private_key, voter_public_key) = request_address_register_check_local(request.user, ballot_id)

        html = "<h1>DEMO PURPOSE ONLY - remove this in prod</h1>" \
               "<div>Token:" \
               "<p style='word-wrap: break-word'>%s</p>" \
               "Signed token:" \
               "<p style='word-wrap: break-word'>%s</p>" \
               "voter_address:" \
               "<p style='word-wrap: break-word'>%s</p>" \
               "voter_private_key:" \
               "<p style='word-wrap: break-word'>%s</p>" \
               "voter_public_key:" \
               "<p style='word-wrap: break-word'>%s</p></div>" \
               "" % (token, signed_token, voter_address, voter_private_key, voter_public_key)

        return HttpResponse(html)


    def generateEthereumAddress(self):

        # Generate address
        keccak = sha3.keccak_256()

        priv = SigningKey.generate(curve=SECP256k1)
        pub = priv.get_verifying_key().to_string()

        keccak.update(pub)
        hex_address = keccak.hexdigest()[24:]

        private_key = priv.to_string().hex()
        public_key = pub.hex()
        address = "0x" + hex_address

        return (private_key, public_key, address)


    def request_address_register(self, user_object, ballot_id, token, signed_token, password):

        local_address_register = request_address_register_check_local(user_object, ballot_id)
        if not None in local_address_register:
            return local_address_register

        (private_key, public_key, address) = self.generateEthereumAddress()

        assert address == self.ethereum.registerPrivateKey(private_key, password)

        # Throws if there's a problem
        NetworkRequest.requestRegisterBallotidVoteraddress(ballot_id, signed_token, token, address)#.wait(5)

        # Save our address & keys
        request_register_address = RegisterAddress(
            user=user_object,
            ballot_id=ballot_id,
            voter_address=address,
            voter_private_key=private_key,
            voter_public_key=public_key
        )
        request_register_address.save()

        return (address, private_key, public_key )


    def request_token_sign(self, ballot_id, user_object, username):

        local_token_sign = request_token_sign_check_local(ballot_id, user_object)
        if not None in local_token_sign:
            return local_token_sign

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

        # Unblind the token & check the signiture
        signed_token = public_key.unblind(signed_blind_token, random_number)

        sig_check = public_key.verify(token, (signed_token, ""))
        if not sig_check:
            raise NetworkExceptions.BadSignitureFromSignedToken(signed_token, token, ballot_id)

        # Save our request progress.
        request_signiture_model = RequestSigniture(
            user=user_object,
            ballot_id=ballot_id,
            token=str(token.decode()),
            token_signed=str(signed_token)
        )
        request_signiture_model.save()

        return (token, signed_token)


class Vote(LoginRequiredMixin, View):

    def __init__(self):
        super().__init__()
        self.ethereum = Ethereum()

    def post(self, request, _ballot_id):
        try:
            ballot_id = int(_ballot_id)
            print(ballot_id)
            (voter_address, voter_private_key, voter_public_key) = request_address_register_check_local( request.user, ballot_id )
            voted_index = int(request.POST['voted_index'])
            ballot_address = (request.POST['ballot_address'])
            voter_password = (request.POST['voter_password'])
        except:
            raise Http404("Error setting initial values.")


        tx_hash = self.ethereum.vote(ballot_address, voted_index, voter_address, voter_password)

        request.session['vote_transaction'] = tx_hash


        return HttpResponseRedirect("/vote/" + str(ballot_id))

    def get(self, request, _ballot_id):
        try:
            username = int(request.user.username)
            ballot_id = int(_ballot_id)
            vote_transaction = request.session.get('vote_transaction', None)
            (voter_address, voter_private_key, voter_public_key) = request_address_register_check_local( request.user, ballot_id )
            if vote_transaction is not None:
                del request.session['vote_transaction']
                request.session.modified = True
        except:
            return Http404("Error setting initial values.")

        # Get the list of ballots the user is eligable in
        available_ballots_list = NetworkRequest.searchUserAvailableBallots(username).wait(5)

        ballot_info = available_ballots_list[next(index for (index, d) in enumerate(available_ballots_list) if d["ballot_id"] == ballot_id)]

        ballot_address = ballot_info['ballot_address']

        return render(request, 'vote.html', {
            'ballot_info' : self.ethereum.ballotInfo(ballot_address),
            'user_info' : self.ethereum.userInfo(ballot_address, voter_address),
            'ballot_id' : ballot_id,
            'ballot_address' : ballot_address,
            'vote_transaction' : vote_transaction })



def request_token_sign_check_local(ballot_id, user_object):
     # First check we havent already recieved a signed token
    database_results = RequestSigniture.objects.filter(
        user=user_object,
        ballot_id=ballot_id
    )

    if len(database_results):
        return ((database_results[0].token).encode(), database_results[0].token_signed )
    else:
        return (None, None)

def request_address_register_check_local(user_object, ballot_id):
    # Check if we have already registered an address for this ballot.
    database_results = RegisterAddress.objects.filter(
                user=user_object,
                ballot_id=ballot_id
            )

    if len(database_results):
        return ( database_results[0].voter_address, database_results[0].voter_private_key, database_results[0].voter_public_key )
    else:
        return (None, None, None)
