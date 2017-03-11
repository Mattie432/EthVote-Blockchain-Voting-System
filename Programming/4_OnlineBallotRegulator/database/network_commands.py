from twisted.protocols import amp


class Request_RegisterUser(amp.Command):
    arguments = [
        (b'user_id',            amp.Integer()),
        (b'ballot_id',          amp.Integer())
    ]
    response = [
        (b'ok', amp.Boolean())
    ]
    errors = {

    }
