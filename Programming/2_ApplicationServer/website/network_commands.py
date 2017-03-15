from twisted.protocols import amp
from twisted.protocols.amp import Command
import psycopg2


class Request_RegisterUser(Command):
    arguments = [
        (b'user_id',            amp.Integer()),
        (b'ballot_id',          amp.Integer())
    ]
    response = [
        (b'ok', amp.Boolean())
    ]
    errors = {
        # psycopg2.ProgrammingError : b'ProgrammingError'
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
