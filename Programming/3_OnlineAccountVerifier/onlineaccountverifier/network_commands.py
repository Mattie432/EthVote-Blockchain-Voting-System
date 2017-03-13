from twisted.protocols import amp
from twisted.protocols.amp import Command
from onlineaccountverifier.network_exceptions import *
import psycopg2

##########################################
#
#   NOTE
#   Changes here need to be reflected in:
#       2_ApplicationServer/website/network_commands.py
#       3_OnlineAccountVerifier/onlineaccountverifier/network_commands.py
#       4_OnlineBallotRegulator
#
##########################################

class Request_SignBlindToken(Command):
    arguments = [
        (b'user_id',            amp.Integer()),
        (b'ballot_id',          amp.Integer()),
        (b'blind_token',        amp.Unicode())
    ]
    response = [
        (b'ok', amp.Boolean())
    ]
    errors = {
        # psycopg2.IntegrityError : b'IntegrityError',
        # psycopg2.ProgrammingError : b'ProgrammingError'
        # Exception : b'Exc'
        # Exception : b'UserBallotError'
    }


class Request_RetrieveBallots(Command):
    arguments = [
        (b'user_id',    amp.Integer())
    ]
    response = [
        (b'ok',         amp.String())
    ]
    errors = {
        psycopg2.ProgrammingError : b'ProgrammingError'
    }


# class Request_RetrieveBallots(Command):
#     arguments = [
#         (b'user_id',    amp.Integer())
#     ]
#     response = [
#         (b'ok',         amp.String())
#     ]
#     errors = {
#         psycopg2.ProgrammingError : b'ProgrammingError'
#     }
