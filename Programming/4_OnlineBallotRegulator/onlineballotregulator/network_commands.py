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

class Request_RegisterUser(Command):
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

class Request_RetrieveRegisteredUserBallots(Command):
    arguments = [
        (b'user_id',            amp.Integer())
    ]
    response = [
        (b'ok',         amp.String())
    ]
    errors = {
        psycopg2.IntegrityError : b'IntegrityError',
        psycopg2.ProgrammingError : b'ProgrammingError'
    }

class Request_RetrieveUserBallots(Command):
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
