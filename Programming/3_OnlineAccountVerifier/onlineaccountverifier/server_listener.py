import psycopg2, os, socket
from twisted.internet import reactor, protocol
from onlineaccountverifier.network_request import MyServerFactory
from twisted.internet.protocol import Factory
# noinspection PyUnresolvedReferences
from database.query import DatabaseQuery
# from .network_request import MyServerFactory

class ServerListener():

    def __init__(self):
        # Import twisted credentials from environment. Throws if does not exist.
        self.twisted_port = int(os.environ[ 'TWISTED_PORT' ])

    def shutdown(self):
        print ("[ServerListener] Shutting down.")

    def start(self):

        self.databasequery = DatabaseQuery()
        self.databasequery.connect()

        protocol_factory = MyServerFactory(self.databasequery)

        print("[ServerListener] Starting server : port=%s, ip=%s" % (self.twisted_port, socket.gethostbyname(socket.gethostname())))

        reactor.listenTCP(self.twisted_port, protocol_factory)
        reactor.run()
