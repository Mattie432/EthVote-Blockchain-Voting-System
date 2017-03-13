

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
            msg = "User '%s' already requested a signiture for ballot '%s' with token '%s'" % (user_id, ballot_id, blind_token)
        super(UserAlreadySubmittedTokenForThisBallot, self).__init__(msg)
        self.user_id=user_id
        self.ballot_id=ballot_id
        self.blind_token=blind_token
