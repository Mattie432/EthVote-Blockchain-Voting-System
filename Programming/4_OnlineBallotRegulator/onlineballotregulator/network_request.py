from onlineballotregulator.network_commands import *
from twisted.internet.protocol import Factory
from twisted.internet.defer import inlineCallbacks, returnValue


class RequestHandler(amp.AMP):

    @Request_RegisterUser.responder
    def request_register_user(self, user_id, ballot_id):
        print('[RequestHandler - request_register_user] Received request : %d, %d' % (user_id, ballot_id))

        databasequery = self.factory.get_databasequery()

        deferred = databasequery.search_userid(user_id)
        # print("ENd")
        # test = Request_RegisterUser.makeResponse({'ok' : True}, None)
        # print(test)
        # print( " --------------------------------------------------------- \n\n\n\n\n")


        return deferred



class MyServerFactory(Factory):
    protocol = RequestHandler

    def __init__(self, databasequery):
        self.databasequery = databasequery

    def get_databasequery(self):
        return self.databasequery
