from onlineballotregulator.network_commands import *
from twisted.internet.protocol import Factory
from twisted.internet.defer import inlineCallbacks, returnValue


class RequestHandler(amp.AMP):

    @Request_RegisterUser.responder
    def request_register_user(self, user_id, ballot_id):
        print('[RequestHandler - request_register_user] Received request : user_id:%d, ballot_id:%d' % (user_id, ballot_id))

        databasequery = self.factory.get_databasequery()

        deferred = databasequery.register_userid_ballotid(user_id, ballot_id)


        return deferred

    @Request_RetrieveBallots.responder
    def request_retrieve_ballots(self, user_id):
        print('[RequestHandler - request_retrieve_ballots] Received request : user_id:%d ' % (user_id))

        databasequery = self.factory.get_databasequery()

        deferred = databasequery.retrieve_ballots(user_id)


        return deferred


    @Request_RetrieveAllBallots.responder
    def request_retrieve_all_ballots(self):
        print('[RequestHandler - request_retrieve_all_ballots] Received request for all ballots')

        databasequery = self.factory.get_databasequery()

        deferred = databasequery.retrieve_all_ballots()

        return deferred



class MyServerFactory(Factory):
    protocol = RequestHandler

    def __init__(self, databasequery):
        self.databasequery = databasequery

    def get_databasequery(self):
        return self.databasequery
