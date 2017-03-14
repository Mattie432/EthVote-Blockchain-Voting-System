import os
import pickle

from Crypto.PublicKey import RSA
from onlineaccountverifier.network_exceptions import *

def sign_blind_token(blind_token, ballot_id):
    """
    Called to sign a blind token recieved from a client. First fetches
    the apropriate key (ascociated with a ballot_id)

    :param blind_token:
    :param ballot_id:
    :return:
    """
    try:
        # Find the apropriate keys for the ballot
        work_dir = os.environ[ 'WORK_DIR']
        path_public = work_dir + "signatures/keys/" + str(ballot_id) + "_ballot_public.pem"
        path_private = work_dir + "signatures/keys/" + str(ballot_id) + "_ballot_private.pem"

        # Get the KEY object
        private_key_string = open(str(path_private), "r").read()
        private_key = RSA.importKey(private_key_string)

        # Sign our blind message
        signed_blinded_token = private_key.sign(blind_token, 0)[0]

        return signed_blinded_token

    except Exception as e:
        print(e)
        raise CannotSigningBlindToken(ballot_id, blind_token)


def check_token_signed_for_ballot(signed_token, token, ballot_id):

    try:
        work_dir = os.environ[ 'WORK_DIR']
        path_public = work_dir + "signatures/keys/" + str(ballot_id) + "_ballot_public.pem"
        path_private = work_dir + "signatures/keys/" + str(ballot_id) + "_ballot_private.pem"

        # Get the RSA key object
        public_key_string = open(str(path_public), "r").read()
        public_key = RSA.importKey(public_key_string)

        # private_key_string = open(str(path_private), "r").read()
        # private_key = RSA.importKey(private_key_string)

        sig_check = public_key.verify(token, (signed_token, 0))

        if not sig_check:
            # Throw if we cannot verif the signiture.
            raise BadSignitureFromSignedToken(signed_token, token, ballot_id)

        return sig_check


    except Exception as e:
        print(e)
        #TODO custom exception
        raise Exception()

    pass
