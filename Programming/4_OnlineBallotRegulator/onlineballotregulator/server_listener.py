import psycopg2, os, socket
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Factory
# noinspection PyUnresolvedReferences
from database.query import DatabaseQuery
# from .network_request import MyServerFactory
from onlineballotregulator.network_request import MyServerFactory

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


    class Listener(protocol.Protocol):

        def __init__(self):
            print("[ServerListener - Listener] Connection established")

        def connectionMade(self):
            print("[ServerListener - Listener] Connection made")

        def connectionLost(self, reason="connectionDone"):
            print("[ServerListener - Listener] Connection Lost : %s" % reason)

        def dataReceived(self, data):
            "As soon as any data is received, write it back."
            print( "[ServerListener - Listener] Data received '%s'" % data )
            self.transport.write(data)
