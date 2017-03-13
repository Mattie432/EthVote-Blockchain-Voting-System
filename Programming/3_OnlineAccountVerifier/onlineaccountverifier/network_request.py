from onlineaccountverifier.network_commands import *
from onlineaccountverifier.network_exceptions import *
from twisted.internet.protocol import Factory
from twisted.python.failure import Failure
import os
from twisted.internet import reactor, defer, endpoints
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.amp import AMP
import pickle, pprint


class RequestHandler(amp.AMP):

    def __init__(self):
        super().__init__()
        self.twisted_ballotregulator_port = int(os.environ['TWISTED_BALLOTREGULATOR_PORT'])
        self.twisted_ballotregulator_ip = str(os.environ['TWISTED_BALLOTREGULATOR_IP'])

    @Request_SignBlindToken.responder
    def request_sign_blind_token(self, user_id, ballot_id, blind_token):

        """
        http://twistedmatrix.com/documents/12.1.0/core/howto/defer.html#class

        :param user_id:
        :param ballot_id:
        :param blind_token:
        :return:
        """
        print('[RequestHandler - request_sign_blind_token] Received request : user_id:%d, ballot_id:%d, blind_token:%s' % (user_id, ballot_id, blind_token))

        databasequery = self.factory.get_databasequery()

        # First we need to query the OnlineBallotRegulator for the 'user_id'

        def searchuser_onconected(ampProto):
            return ampProto.callRemote(Request_RetrieveBallots, user_id=user_id)

        def searchuser_callremote_errback(failure):
            print("There was an error in the remote call", type(failure))
            raise failure.raiseException()

        print('[RequestHandler - request_sign_blind_token] Connecting to ballotregulator - port=%s, ip=%s'
              % (self.twisted_ballotregulator_ip, self.twisted_ballotregulator_port))

        searchuser_destination      = TCP4ClientEndpoint(reactor, self.twisted_ballotregulator_ip, self.twisted_ballotregulator_port)
        searchuser_connectcall      = connectProtocol(searchuser_destination, AMP())
        searchuser_results          = searchuser_connectcall.addCallback(searchuser_onconected).addErrback(searchuser_callremote_errback)

        # Now we need to format the returned results.

        def format_searchuser_results(pickled_result):

            # First unpickle the results.
            result = pickle.loads(pickled_result['ok'])

            # Transform the list results into a dictionary.
            record_list = []
            for record in result:
                mapper = {
                    'user_id': record[0],
                    'ballot_id': record[1],
                    'timestamp': record[2],
                    'ballot_name': record[3],
                    'ballot_address': record[4]
                }
                # Append each row's dictionary to a list
                record_list.append(mapper)

            # return record_list
            return record_list

        def format_searchuser_results_errback(failure):
            print("[RequestHandler - request_sign_blind_token - format_searchuser_results_errback] There was an error formatting the results", type(failure))
            raise failure.raiseException()

        searchuser_results_format_result  = searchuser_results.addCallback(format_searchuser_results).addErrback(format_searchuser_results_errback)

        # Now, lets check that the voter_id is registered for the ballot_id

        def checkvalid_userid_ballotid(results_list):
            found = False
            for record in results_list:
                if record['ballot_id'] == ballot_id:
                    found = True
                    print("[RequestHandler - request_sign_blind_token - checkvalid_userid_ballotid] user_id=%s is registered for ballot_id=%s"
                          % (user_id, ballot_id))
                    break

            if not found:
                raise UserNotRegisterdForBallot(user_id,ballot_id)

            return found # Return something though we dont need to.

        def checkvalid_userid_ballotid_errback(failure):
            print("[RequestHandler - request_sign_blind_token - checkvalid_userid_ballotid_errback] There was an error when checking the ballot & user id's")
            raise failure.raiseException()


        checkvalid_userid_ballotid_result = searchuser_results_format_result.addCallback(checkvalid_userid_ballotid).addErrback(checkvalid_userid_ballotid_errback)


        # Okay thats good, is this the first time the onlineaccountverifier is seeing this combination of user_id & ballot_id?

        def checkfirsttime_userid_ballotid(userid_found_in_onlineballotregulator):

            query = databasequery.retrieve_request_sign(user_id)

            def checkReturnedQuery(pickled_result):
                # First unpickle the results.
                results_list = pickle.loads(pickled_result['ok'])

                 # Transform the list results into a dictionary.
                record_list = []
                for record in results_list:
                    mapper = {
                        'blind_token': record[0],
                        'user_id': record[1],
                        'ballot_id': record[2],
                        'timestamp': record[3]
                    }
                    # Append each row's dictionary to a list
                    record_list.append(mapper)


                for record in record_list:
                    if record['ballot_id'] == ballot_id:
                        print("[RequestHandler - request_sign_blind_token - checkfirsttime_userid_ballotid] user_id='%s' is registered for ballot_id='%s'"
                              % (user_id, ballot_id))
                        raise UserAlreadySubmittedTokenForThisBallot(user_id,ballot_id, record['blind_token'] )

                return True # Return something though we dont need to.

            return query.addCallback(checkReturnedQuery)

        def checkfirsttime_userid_ballotid_errback(failure):
            print("[RequestHandler - request_sign_blind_token - checkvalid_userid_ballotid_errback] There was an error checking the ballot & user id's")
            raise failure.raiseException()

        checkfirsttime_userid_ballotid_result   = checkvalid_userid_ballotid_result.addCallback(checkfirsttime_userid_ballotid).addErrback(checkfirsttime_userid_ballotid_errback)

        # All of our checks are complete, lets sign the token.

        def sign_blindtoken(checkfirsttime_userid_ballotid):
            pass

        def sign_blindtoken_errback(failure):
            print("[RequestHandler - request_sign_blind_token - sign_blindtoken_errback] There was an error signing the token.")
            raise failure.raiseException()

        sign_blindtoken_result = checkfirsttime_userid_ballotid_result.addCallback(sign_blindtoken).addErrback(sign_blindtoken_errback)

        def print_results(results_list):
            pprint.pprint(results_list)
            return { 'ok' : True}

        final_defer = sign_blindtoken_result.addCallback(print_results)


        return final_defer


class MyServerFactory(Factory):
    protocol = RequestHandler

    def __init__(self, databasequery):
        self.databasequery = databasequery

    def get_databasequery(self):
        return self.databasequery
