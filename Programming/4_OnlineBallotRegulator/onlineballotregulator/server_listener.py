import psycopg2, os
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Factory
# noinspection PyUnresolvedReferences
from database.network_request import MyServerFactory


class ServerListener():

    def __init__(self):
        print ("Init")
        # Import postgres & twisted credentials from environment. Throws if does not exist.
        self.postgres_database   = os.environ[ 'POSTGRES_DATABASE' ]
        self.postgres_user       = os.environ[ 'POSTGRES_USER' ]
        self.postgres_password   = os.environ[ 'POSTGRES_PASS' ]
        self.postgres_host       = os.environ[ 'POSTGRES_HOST' ]
        self.twisted_port        = int(os.environ[ 'TWISTED_PORT' ])


        print ("[ServerListener] Connecting to database\n"
           "    -> database:'%s' user:'%s' host:'%s'" % (self.postgres_database, self.postgres_user, self.postgres_host) )

        # get a connection, if a connect cannot be made an exception will be raised here
        self.connection = psycopg2.connect(database=self.postgres_database, user=self.postgres_user, host=self.postgres_host, password=self.postgres_password)
        self.cursor = self.connection.cursor()

        print("[ServerListener] Database connection sucsessful")

    def shutdown(self):
        print ("[ServerListener] Shutting down.")
        self.cursor.close()
        self.connection.close()

    def start(self):
        protocol_factory = MyServerFactory(self.cursor)

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
