import os
import pickle

from crochet import setup, run_in_reactor
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.amp import AMP

from network.network_commands import *

setup()

ballotregulator_ip       = os.environ[ 'TWISTED_BALLOTREGULATOR_IP' ]
ballotregulator_port       = int(os.environ[ 'TWISTED_BALLOTREGULATOR_PORT' ])
accountverifier_ip       = os.environ[ 'TWISTED_ACCOUNTVERIFIER_IP' ]
accountverifier_port       = int(os.environ[ 'TWISTED_ACCOUNTVERIFIER_PORT' ])
applicationserver_ip       = os.environ[ 'TWISTED_APPLICATIONSERVER_IP' ]
applicationserver_port       = int(os.environ[ 'TWISTED_APPLICATIONSERVER_PORT' ])

@run_in_reactor
@inlineCallbacks
def getBallotPublicKey(ballot_id):
    destination_deferred = yield TCP4ClientEndpoint(reactor, accountverifier_ip, accountverifier_port)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(OnlineAccountVerifier_GetPublicKeyForBallot, ballot_id=int(ballot_id))

    def format_results(pickled_result):
        ballot_public_key = pickle.loads(pickled_result['ok'])
        return ballot_public_key

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))

@run_in_reactor
@inlineCallbacks
def requestRegisterUseridForBallotid(user_id, ballot_id):

    destination_deferred = yield TCP4ClientEndpoint(reactor, ballotregulator_ip, ballotregulator_port)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(OnlineBallotRegulator_RegisterUserIdForBallotId, user_id=int(user_id), ballot_id=int(ballot_id) )

    def format_results(result):
        return result['ok']

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))

@run_in_reactor
@inlineCallbacks
def requestRegisterBallotidVoteraddress(ballot_id, signed_token, token, voter_address):

    pickled_signed_token = pickle.dumps(int(signed_token))
    pickled_token = pickle.dumps(token)
    pickled_voter_address = pickle.dumps(voter_address)

    destination_deferred = yield TCP4ClientEndpoint(reactor, accountverifier_ip, accountverifier_port)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(OnlineAccountVerifier_RegisterAddressToBallot, ballot_id=int(ballot_id), pickled_signed_token=pickled_signed_token, pickled_token=pickled_token, pickled_voter_address=pickled_voter_address)

    def format_results(result):
        return result['ok']

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))

@run_in_reactor
@inlineCallbacks
def requestSignOfToken(user_id, ballot_id, blind_token):

    destination_deferred = yield TCP4ClientEndpoint(reactor, accountverifier_ip, accountverifier_port)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(OnlineAccountVerifier_SignBlindToken, user_id=user_id, ballot_id=ballot_id, blind_token=blind_token)

    def format_results(pickled_result):
        signed_blind_token = pickle.loads(pickled_result['ok'])
        return signed_blind_token

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))

@run_in_reactor
@inlineCallbacks
def requestRegisterNewBallot(ballot_name, ballot_options_array, ballot_end_date):


    ballot_options_array_pickled = pickle.dumps(ballot_options_array)

    destination_deferred = yield TCP4ClientEndpoint(reactor, ballotregulator_ip, ballotregulator_port)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(OnlineBallotRegulator_RegisterBallotId, ballot_name=ballot_name, ballot_options_array_pickled=ballot_options_array_pickled, ballot_end_date=ballot_end_date)

    def format_results(result):
        return result['ballot_address']

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))

@run_in_reactor
@inlineCallbacks
def searchUserAvailableBallots(user_id):
    """
    http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

    Blocking call to the ballot server to request the ballots for a particular user.

    :return: EventualResult
    """

    # NOTE: using inline callbacks here so we dont have to write/wait for callbacks.
    destination_deferred = yield TCP4ClientEndpoint(reactor, ballotregulator_ip, ballotregulator_port)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(OnlineBallotRegulator_SearchBallotRegisterForUserId, user_id=user_id)

    def format_results(pickled_result):

        # First unpickle the results.
        result = pickle.loads(pickled_result['ok'])

        # Transform the list results into a dictionary.
        record_list = []
        for record in result:
            mapper = {}
            mapper['user_id'] = record[0]
            mapper['ballot_id'] = record[1]
            mapper['timestamp'] = record[2]
            mapper['ballot_name'] = record[3]
            mapper['ballot_address'] = record[4]
            # Append each row's dictionary to a list
            record_list.append(mapper)

        return record_list

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))

@run_in_reactor
@inlineCallbacks
def searchAllAvailableBallots():
    """
    http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

    Blocking call to the ballot server to request the ballots for a particular user.

    :return: EventualResult
    """

    # NOTE: using inline callbacks here so we dont have to write/wait for callbacks.
    destination_deferred = yield TCP4ClientEndpoint(reactor, ballotregulator_ip, ballotregulator_port)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(OnlineBallotRegulator_SearchBallotsAvailableForAllBallots)

    def format_results(pickled_result):

        # First unpickle the results.
        result = pickle.loads(pickled_result['ok'])

        # Transform the list results into a dictionary.
        record_list = []
        for record in result:
            mapper = {}
            mapper['ballot_id'] = record[0]
            mapper['ballot_name'] = record[1]
            mapper['ballot_address'] = record[2]
            mapper['timestamp'] = record[3]
            mapper['ballot_interface'] = record[4]
            mapper['ballot_end_date'] = record[5]
            # Append each row's dictionary to a list
            record_list.append(mapper)

        return record_list

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))

@run_in_reactor
@inlineCallbacks
def searchUserRegisteredBallots(user_id):
    """
    http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

    Blocking call to the acountverifier server to request the ballots for a particular user has already registered for..

    :return: EventualResult
    """

    # NOTE: using inline callbacks here so we dont have to write/wait for callbacks.
    destination_deferred = yield TCP4ClientEndpoint(reactor, accountverifier_ip, accountverifier_port)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(OnlineAccountVerifier_SearchTokenRequestForUserId, user_id=user_id)

    def format_results(pickled_result):

        # First unpickle the results.
        result = pickle.loads(pickled_result['ok'])

        # Transform the list results into a dictionary.
        record_list = []
        for record in result:
            mapper = {}
            mapper['token_request_id'] = record[0]
            mapper['blind_token_hash'] = record[1]
            mapper['user_id'] = record[2]
            mapper['ballot_id'] = record[3]
            mapper['timestamp'] = record[4]
            # Append each row's dictionary to a list
            record_list.append(mapper)

        return record_list

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))

@run_in_reactor
@inlineCallbacks
def requestRegisterNewUser(user_id, password):
    destination_deferred = yield TCP4ClientEndpoint(reactor, applicationserver_ip, applicationserver_port)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(ApplicationServer_RegisterNewUser, user_id=int(user_id), password=password)

    def format_results(result):
        return result['ok']

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))
