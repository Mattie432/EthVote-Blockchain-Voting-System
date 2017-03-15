##########################################
#
#   NOTE
#   Changes here need to be reflected in:
#       2_ApplicationServer/website/network_exceptions.py
#       3_OnlineAccountVerifier/onlineaccountverifier/network_exceptions.py
#       4_OnlineBallotRegulator/onlineaballotregulator/network_exceptions.py
#
##########################################


class UserNotRegisterdForBallot(Exception):
    '''Raised when requesting token signiture and the user cannot register for a ballot'''
    def __init__(self, user_id, ballot_id, msg=None):
        if msg is None:
            msg = "User '%s' is not registered for ballot '%s'" % (user_id, ballot_id)
        super(UserNotRegisterdForBallot, self).__init__(msg)
        self.user_id=user_id
        self.ballot_id=ballot_id


class UserAlreadySubmittedTokenForThisBallot(Exception):
    '''Raised when requesting token signiture and the user cannot register for a ballot'''
    def __init__(self, user_id, ballot_id, blind_token, msg=None):
        if msg is None:
            msg = "User '%s' already requested a signiture for ballot '%s' with token hash '%s'" % (user_id, ballot_id, blind_token)
        super(UserAlreadySubmittedTokenForThisBallot, self).__init__(msg)
        self.user_id=user_id
        self.ballot_id=ballot_id
        self.blind_token=blind_token


class CannotSigningBlindToken(Exception):
    '''Raised when requesting token signiture and the user cannot register for a ballot'''
    def __init__(self, ballot_id, blind_token, msg=None):
        if msg is None:
            msg = "Error signing token '%s' for ballot '%s'" % (blind_token, ballot_id)
        super(CannotSigningBlindToken, self).__init__(msg)
        self.ballot_id=ballot_id
        self.blind_token=blind_token


class BadSignitureFromSignedToken(Exception):
    def __init__(self, signed_token, token, ballot_id, msg=None):
        if msg is None:
            msg = "Error checking signiture for token '%s' for ballot '%s'" % (token, ballot_id)
        super(BadSignitureFromSignedToken, self).__init__(msg)
        self.ballot_id=ballot_id
        self.signed_token=signed_token
        self.token=token


class BallotNotAvailable(Exception):
    def __init__(self, ballot_id, msg=None):
        if msg is None:
            msg = "Requested ballot '%s' was not available on the 'onlineballotregulator' host." % (ballot_id)
        super(BallotNotAvailable, self).__init__(msg)
        self.ballot_id=ballot_id


class BallotVoteraddressAlreadyRegistered(Exception):
    def __init__(self, ballot_id, voter_address, signed_token, msg=None):
        if msg is None:
            msg = "The address '%s' is already registered with ballot '%s'." % (voter_address, ballot_id)
        super(BallotVoteraddressAlreadyRegistered, self).__init__(msg)
        self.ballot_id=ballot_id
        self.voter_address=voter_address
        self.signed_token=signed_token

