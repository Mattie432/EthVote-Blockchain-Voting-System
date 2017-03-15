from twisted.protocols import amp
from twisted.protocols.amp import Command
import psycopg2


class OnlineBallotRegulator_RegisterUserIdForBallotId(Command):
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

class OnlineBallotRegulator_SearchBallotRegisterForUserId(Command):
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


class OnlineAccountVerifier_SearchTokenRequestForUserId(Command):
    arguments = [
        (b'user_id',            amp.Integer())
    ]
    response = [
        (b'ok', amp.String())
    ]
    errors = {
        #TODO add errors
    }






class OnlineAccountVerifier_GetPublicKeyForBallot(Command):
    arguments = [
        (b'ballot_id',              amp.Integer())
    ]
    response = [
        (b'ok',                 amp.String())
    ]
    errors = {
        Exception : b'RequestPublicSigningKeyError'
    }
