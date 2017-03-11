from twisted.protocols import amp
from .network_commands import *
from twisted.internet.protocol import ServerFactory


# class NetworkRequest:
#
#     def __init__(self):
#         print("[NetworkRequest] instantiated.")
#         # self.cursor = cursor
#
#     class RequestHandler(amp.AMP):
#
#         def request_register_user(self, user_id, ballot_id):
#
#             print('[RequestHandler - request_register_user] Received request : %d, %d' % (user_id, ballot_id))
#
#             self.cursor.execute("SELECT *;")
#             return { 'ok' : True }
#
#         Request_RegisterUser.responder(request_register_user)




class RequestHandler(amp.AMP):

    def request_register_user(self, user_id, ballot_id):

        print('[RequestHandler - request_register_user] Received request : %d, %d' % (user_id, ballot_id))


        cursor = self.factory.get_cursor()
        cursor.execute("SELECT * FROM ballot_register;")

        return { 'ok' : True }

    Request_RegisterUser.responder(request_register_user)


class MyServerFactory(ServerFactory):
    protocol = RequestHandler

    def __init__(self, cursor):
        self.cursor = cursor

    def get_cursor(self):
        return self.cursor
