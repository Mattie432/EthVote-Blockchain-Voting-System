from twisted.protocols import amp
from twisted.protocols.amp import Command


class Request_RegisterUser(Command):
    arguments = [
        (b'user_id',            amp.Integer()),
        (b'ballot_id',          amp.Integer())
    ]
    response = [
        (b'ok', amp.String())
    ]
    errors = {

    }
