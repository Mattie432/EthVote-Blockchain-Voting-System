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
        (b'blind_token',        amp.String())
    ]
    response = [
        (b'ok', amp.String())
    ]
    errors = {
        psycopg2.IntegrityError : b'IntegrityError',
        psycopg2.ProgrammingError : b'ProgrammingError',
        UserNotRegisterdForBallot : b'NotRegistered',
        Exception : b'Request_SignBlindToken'
    }


class Request_RetrieveSignBlindTokenForUser(Command):
    arguments = [
        (b'user_id',            amp.Integer())
    ]
    response = [
        (b'ok', amp.String())
    ]
    errors = {
        #TODO add errors
    }

class Request_RegisterAddressToBallot(Command):
    arguments = [
        (b'ballot_id',              amp.Integer()),
        (b'pickled_signed_token',   amp.String()),
        (b'pickled_token',          amp.String()),
        (b'pickled_voter_address',  amp.String())
    ]
    response = [
        (b'ok',                 amp.Boolean())
    ]
    errors = {
        #TODO add errors
    }


class Request_PublicKeyForBallot(Command):
    arguments = [
        (b'ballot_id',              amp.Integer())
    ]
    response = [
        (b'ok',                 amp.String())
    ]
    errors = {
        Exception : b'RequestPublicSigningKeyError'
    }



# Other Classes

class Request_RetrieveRegisteredUserBallots(Command):
    arguments = [
        (b'user_id',    amp.Integer())
    ]
    response = [
        (b'ok',         amp.String())
    ]
    errors = {
        psycopg2.ProgrammingError : b'ProgrammingError'
    }


class Request_RetrieveAllBallots(Command):
    arguments = [
    ]
    response = [
        (b'ok',         amp.String())
    ]
    errors = {
        psycopg2.ProgrammingError : b'ProgrammingError'
    }
