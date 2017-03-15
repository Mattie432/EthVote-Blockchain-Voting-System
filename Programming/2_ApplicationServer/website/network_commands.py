from twisted.protocols import amp
from twisted.protocols.amp import Command
from .network_exceptions import *
import psycopg2

##########################################
#
#   NOTE
#   Changes here need to be reflected in:
#       2_ApplicationServer/website/network_commands.py
#       3_OnlineAccountVerifier/onlineaccountverifier/network_commands.py
#       4_OnlineBallotRegulator/onlineaballotregulator/network_commands.py
#
##########################################


class OnlineAccountVerifier_SignBlindToken(Command):
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
        Exception : b'OnlineAccountVerifier_SignBlindToken'
    }


class OnlineAccountVerifier_SearchTokenRequestForUserId(Command):
    arguments = [
        (b'user_id',            amp.Integer())
    ]
    response = [
        (b'ok', amp.String())
    ]
    errors = {
        #TODO add errors
        Exception : b'OnlineAccountVerifier_SearchTokenRequestForUserId'
    }


class OnlineAccountVerifier_RegisterAddressToBallot(Command):
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
        Exception : b'OnlineAccountVerifier_RegisterAddressToBallot'
    }


class OnlineAccountVerifier_GetPublicKeyForBallot(Command):
    arguments = [
        (b'ballot_id',          amp.Integer())
    ]
    response = [
        (b'ok',                 amp.String())
    ]
    errors = {
        Exception : b'OnlineAccountVerifier_GetPublicKeyForBallot'
    }


class OnlineBallotRegulator_RegisterUserIdForBallotId(Command):
    arguments = [
        (b'user_id',            amp.Integer()),
        (b'ballot_id',          amp.Integer())
    ]
    response = [
        (b'ok', amp.Boolean())
    ]
    errors = {
        psycopg2.IntegrityError : b'IntegrityError',
        psycopg2.ProgrammingError : b'ProgrammingError'
    }


class OnlineBallotRegulator_SearchBallotRegisterForUserId(Command):
    arguments = [
        (b'user_id',            amp.Integer())
    ]
    response = [
        (b'ok',         amp.String())
    ]
    errors = {
        psycopg2.IntegrityError : b'IntegrityError'
    }


class OnlineBallotRegulator_SearchBallotsAvailableForAllBallots(Command):
    arguments = [
    ]
    response = [
        (b'ok',         amp.String())
    ]
    errors = {
        psycopg2.ProgrammingError : b'ProgrammingError'
    }
