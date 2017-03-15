from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
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

import network.network_calls as NetworkRequest

class RegisterForBallot(LoginRequiredMixin, View):

    def get(self, request, param_ballot_id):
        try:
            ballot_id = int(param_ballot_id)
            username = int(request.user.username)
        except ValueError:
            raise Http404("Couldn't cast ballot_id or username to int")

        (token, signed_token) = self.request_token_sign(ballot_id, request.user, username)

        (voter_address, voter_private_key, voter_public_key) = self.request_address_register(request.user, ballot_id, token, signed_token)

        html = "Token:" \
               "<p style='word-wrap: break-word'>%s</p>" \
               "Signed token:" \
               "<p style='word-wrap: break-word'>%s</p>" \
               "voter_address:" \
               "<p style='word-wrap: break-word'>%s</p>" \
               "voter_private_key:" \
               "<p style='word-wrap: break-word'>%s</p>" \
               "voter_public_key:" \
               "<p style='word-wrap: break-word'>%s</p>" \
               "" % (token, signed_token, voter_address, voter_private_key, voter_public_key)

        return HttpResponse(html)


    def generateEthereumAddress(self):

        # Generate address
        keccak = sha3.keccak_256()

        priv = SigningKey.generate(curve=SECP256k1)
        pub = priv.get_verifying_key().to_string()

        keccak.update(pub)
        hex_address = keccak.hexdigest()[24:]

        # print("priv.to_string()", priv.to_string().hex())

        print("Private key:", priv.to_string().hex())
        print("Public key: ", pub.hex())
        print("Address:     0x" + hex_address)

        private_key = priv.to_string().hex()
        public_key = pub.hex()
        address = "0x" + hex_address

        return (private_key, public_key, address)

    def request_address_register(self, user_object, ballot_id, token, signed_token):

        # Check if we have already registered an address for this ballot.
        database_results = RegisterAddress.objects.filter(
                    user=user_object,
                    ballot_id=ballot_id
                )

        if len(database_results):
            return ( database_results[0].voter_address, database_results[0].voter_private_key, database_results[0].voter_public_key )

        (private_key, public_key, address) = self.generateEthereumAddress()


        return ("test","test","test")

    def request_token_sign(self, ballot_id, user_object, username):

         # First check we havent already recieved a signed token
        database_results = RequestSigniture.objects.filter(
            user=user_object,
            ballot_id=ballot_id
        )

        if len(database_results):
            return ((database_results[0].token).encode(), database_results[0].token_signed )

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


