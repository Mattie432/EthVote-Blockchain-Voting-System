from twisted.protocols import amp
from .network_commands import *


class NetworkRequest:

    def __init__(self, connection):
        print("[NetworkRequest] instantiated.", connection)

    class RequestHandler(amp.AMP):

        def request_blindtoken_sign(self, user_id, ballot_id, blind_token):

            print('Received request_blindtoken_sign request : %d, %d, %s' % (user_id, ballot_id, blind_token))
            value = str.encode("response = " + str(user_id) + str(ballot_id) + str(blind_token))
            return {'signed_blind_token': value }
        RequestBlindtokenSign.responder(request_blindtoken_sign)

