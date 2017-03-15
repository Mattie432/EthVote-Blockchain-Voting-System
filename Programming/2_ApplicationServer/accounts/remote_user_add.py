import os, socket
from random import randint

from twisted.internet.protocol import Factory
from twisted.internet import reactor, defer
from twisted.protocols.amp import AMP
from crochet import setup, run_in_reactor
from network.network_commands import *

# if __name__ != "__main__":
from accounts.models import User

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

setup()

class RequestHandler(AMP):

    @ApplicationServer_RegisterNewUser.responder
    def register_new_user(self, user_id, password):
        d = defer.Deferred()

        def request(ignored):

            user = User.objects.create_user(int(user_id), email='', password=password)
            print( "[remote_user_add - register_new_user] Sucsessfully registered user '%s'" % user_id  )
            return { 'ok' : True }

        def request_errback(failure):
            print( "[remote_user_add - register_new_user] Failed to register user '%s'" % user_id  )
            raise failure.raiseException()

        d.addCallback(request).addErrback(request_errback)
        d.callback(None)

        return d

class MyServerFactory(Factory):
    protocol = RequestHandler

class ServerListener():

    def __init__(self):
        # Import twisted credentials from environment. Throws if does not exist.
        self.twisted_port = int(os.environ[ 'TWISTED_PORT' ])

    def shutdown(self):
        print ("[ServerListener] Shutting down.")

    def start(self):
        protocol_factory = MyServerFactory()

        print("[ServerListener] Starting server : port=%s, ip=%s" % (self.twisted_port, socket.gethostbyname(socket.gethostname())))

        reactor.listenTCP(self.twisted_port, protocol_factory)

@run_in_reactor
@inlineCallbacks
def testAddUser(user_id, password):
    destination_deferred = yield TCP4ClientEndpoint(reactor, '127.0.0.1', 5436)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(ApplicationServer_RegisterNewUser, user_id=int(user_id), password=password)

    def format_results(result):
        return result['ok']

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))

if __name__ == "__main__":
    print("Starting remote add")
    # server = ServerListener()
    # server.start()
    # reactor.run()
    user_id = randint(0,10000)
    result = testAddUser(user_id, 'password').wait(5)
    print("Test user '%s' result : %s" % (user_id, result))
