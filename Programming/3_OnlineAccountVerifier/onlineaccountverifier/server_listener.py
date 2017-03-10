import psycopg2, os
from twisted.internet import reactor, protocol


class ServerListener():

    def __init__(self):
        print ("Init")
        # Import postgres & twisted credentials from environment. Throws if dont exist.
        self.postgres_database   = os.environ[ 'POSTGRES_DATABASE' ]
        self.postgres_user       = os.environ[ 'POSTGRES_USER' ]
        self.postgres_password   = os.environ[ 'POSTGRES_PASS' ]
        self.postgres_host       = os.environ[ 'POSTGRES_HOST' ]
        self.twisted_port        = int(os.environ[ 'TWISTED_PORT' ])


        print ("[main] Connecting to database\n"
           "    -> database:'%s' user:'%s' host:'%s'" % (self.postgres_database, self.postgres_user, self.postgres_host) )

        # get a connection, if a connect cannot be made an exception will be raised here
        self.connection = psycopg2.connect(database=self.postgres_database, user=self.postgres_user, host=self.postgres_host, password=self.postgres_password)
        self.cursor = self.connection.cursor()

    def database_shutdown(self):
        print ("[main] Shutting down database connection.")
        self.cursor.close()
        self.connection.close()

    def start(self):
        factory = protocol.ServerFactory()
        factory.protocol = self.Listener
        reactor.listenTCP(self.twisted_port, factory)
        reactor.run()

    class Listener(protocol.Protocol):

        def __init__(self):
            print("[Listener] Connection established")

        def connectionMade(self):
            print("[Listener] Connection made")

        def connectionLost(self, reason="connectionDone"):
            print("[Listener] Connection Lost : %s" % reason)

        def dataReceived(self, data):
            "As soon as any data is received, write it back."
            print( "[Listener] Data received '%s'" % data )
            self.transport.write(data)
