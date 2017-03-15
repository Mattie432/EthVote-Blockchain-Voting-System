from twisted.protocols import amp
from twisted.protocols.amp import Command
import psycopg2

##########################################
#
#   NOTE
#   Changes here need to be reflected in:
#       2_ApplicationServer/website/network_commands.py
#       3_OnlineAccountVerifier/onlineaccountverifier/network_commands.py
#
##########################################

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
