from twisted.protocols import amp


class RequestBlindtokenSign(amp.Command):
    arguments = [
        (b'user_id',            amp.Integer()),
        (b'ballot_id',          amp.Integer()),
        (b'blind_token',        amp.String())
    ]
    response = [
        (b'signed_blind_token', amp.String())
    ]
    errors = {}
