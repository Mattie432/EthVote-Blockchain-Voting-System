from twisted.internet import defer
from twisted.internet import threads

from onlineballotregulator.network_commands import *
from twisted.internet.protocol import Factory
from twisted.internet.defer import inlineCallbacks, returnValue
import pickle, json
from ethereum.ethereum import Ethereum

class RequestHandler(amp.AMP):

    def __init__(self):
        super().__init__()
        self.ethereum = Ethereum()

    @OnlineBallotRegulator_RequestContractABI.responder
    def request_contract_abi(self):


        def request(param):
            interface = self.ethereum.getBallotInterface()
            dumps = pickle.dumps(interface)
            return { 'ok' : (dumps) }

        def request_errback(failure):
            raise failure.raiseException()

        d = defer.Deferred()
        d.addCallback(request).addErrback(request_errback)
        d.callback(True)
        return d


    @OnlineBallotRegulator_RegisterUserIdForBallotId.responder
    def insert_into_ballot_register_user_id_ballot_id(self, user_id, ballot_id):
        print('[RequestHandler - insert_into_ballot_register_user_id_ballot_id] Received request : user_id:%d, ballot_id:%d' % (user_id, ballot_id))

        databasequery = self.factory.get_databasequery()

        deferred = databasequery.insert_into_ballot_register_user_id_ballot_id(user_id, ballot_id)


        return deferred

    @OnlineBallotRegulator_SearchBallotRegisterForUserId.responder
    def search_ballot_register_for_user_id(self, user_id):
        print('[RequestHandler - request_retrieve_ballots] Received request : user_id:%d ' % (user_id))

        databasequery = self.factory.get_databasequery()

        deferred = databasequery.search_ballot_register_for_user_id(user_id)


        return deferred

    @OnlineBallotRegulator_RegisterBallotId.responder
    def register_ballot(self, ballot_name, ballot_options_array_pickled, ballot_end_date):

        ballot_options_array = pickle.loads(ballot_options_array_pickled)

        print('[RequestHandler - register_ballot] Received request : name:%s \n'
              '    With options: %s' % (ballot_name, ballot_options_array))

        ballot_interface = 'empty' #pickle.dumps(self.ethereum.getBallotInterface())

        ballot_address = self.ethereum.registerBallot(ballot_name, ballot_end_date, ballot_options_array)

        databasequery = self.factory.get_databasequery()

        deferred = databasequery.insert_into_ballots_available(ballot_name, ballot_address, ballot_interface, ballot_end_date )

        return deferred


    @OnlineBallotRegulator_SearchBallotsAvailableForAllBallots.responder
    def search_ballots_available_for_all_ballots(self):
        print('[RequestHandler - search_ballots_available_for_all_ballots] Received request for all ballots')

        databasequery = self.factory.get_databasequery()

        deferred = databasequery.search_ballots_available_for_all_ballots()

        return deferred

    @OnlineBallotRegulator_RegisterVoterAddressBallotId.responder
    def register_voter_address_ballot_id(self, voter_addres, ballot_id):
        databasequery = self.factory.get_databasequery()

        defered = databasequery.search_ballots_available_for_ballot_id(ballot_id)

        def search_ballot_id_errback(failure):
            raise failure.raiseException()

        def search_ballot_id_format_results(pickled_result):

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

        results = defered.addCallback(search_ballot_id_format_results).addErrback(search_ballot_id_errback)

        def blockchain_add(record_list):

            ballot_interface = self.ethereum.getBallotInterface()
            ballot_address = record_list[0]['ballot_address']

            ethererum = Ethereum()
            d = ethererum.interact_give_right_to_vote(ballot_address, voter_addres, ballot_interface)

            return d

        def blockchain_add_errback(failure):
            raise failure.raiseException()


        blockchain_add_defered = results.addCallback(blockchain_add).addErrback(blockchain_add_errback)

        def return_res(result):
            response = str(result)
            return { 'ok' : response }

        def return_res_errback(failuire):
            print("return_res_errback\n\n", failuire.getErrorMessage())
            raise failuire.raiseException()

        return_defered = blockchain_add_defered.addCallback(return_res).addErrback(return_res_errback)

        return return_defered


class MyServerFactory(Factory):
    protocol = RequestHandler

    def __init__(self, databasequery):
        self.databasequery = databasequery

    def get_databasequery(self):
        return self.databasequery
