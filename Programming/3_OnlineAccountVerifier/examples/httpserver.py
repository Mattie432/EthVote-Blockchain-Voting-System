from twisted.protocols import basic
from twisted.internet import protocol, reactor
from twisted.application import service, internet
import os

class HTTPEchoProtocol(basic.LineReceiver):
	def __init__(self):
		self.lines = []

	def lineReceived(self, line):
		self.lines.append(line)
		if not line:
			self.sendResponse()

	def sendResponse(self):
		self.sendLine('HTTP/1.1 200 OK')
		self.sendLine('')
		responseBody = "You said:\r\n\r\n" + "\r\n".join(self.lines)
		self.transport.write(responseBody)
		self.transport.loseConnection()

class HTTPEchoFactory(protocol.ServerFactory):
	def buildProtocol(self, addr):
		return HTTPEchoProtocol()

# default port in case of the env var not was properly set.
ECHO_SERVER_PORT = 8000

proxy_port = int(os.environ.get('ECHO_SERVER_PORT', ECHO_SERVER_PORT))

application = service.Application('TwistedDockerized')
factory = HTTPEchoFactory()
server = internet.TCPServer(proxy_port, factory)
server.setServiceParent(application)
