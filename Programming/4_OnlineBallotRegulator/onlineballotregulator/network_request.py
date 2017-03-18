from onlineballotregulator.network_commands import *
from twisted.internet.protocol import Factory
from twisted.internet.defer import inlineCallbacks, returnValue


class RequestHandler(amp.AMP):

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
    def register_ballot(self, ballot_id, ballot_name, ballot_address, ballot_interface):
        print('[RequestHandler - register_ballot] Received request : ballot_id:%d as %s ' % (ballot_id, ballot_name))

        databasequery = self.factory.get_databasequery()

        deferred = databasequery.insert_into_ballots_available(ballot_id, ballot_name, ballot_address, ballot_interface)


        return deferred


    @OnlineBallotRegulator_SearchBallotsAvailableForAllBallots.responder
    def search_ballots_available_for_all_ballots(self):
        print('[RequestHandler - search_ballots_available_for_all_ballots] Received request for all ballots')

        databasequery = self.factory.get_databasequery()

        deferred = databasequery.search_ballots_available_for_all_ballots()

        return deferred


class MyServerFactory(Factory):
    protocol = RequestHandler

    def __init__(self, databasequery):
        self.databasequery = databasequery

    def get_databasequery(self):
        return self.databasequery
