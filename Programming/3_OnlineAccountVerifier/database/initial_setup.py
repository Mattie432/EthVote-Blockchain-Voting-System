import psycopg2, os
from crochet import setup, run_in_reactor
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.amp import AMP
import pickle
from twisted.internet.defer import inlineCallbacks, returnValue
from onlineaccountverifier.network_commands import OnlineBallotRegulator_SearchBallotsAvailableForAllBallots
from subprocess import call

#Setup crochet
setup()

# Import postgres credentials from environment
postgres_database   = os.environ[ 'POSTGRES_DATABASE' ]
postgres_user       = os.environ[ 'POSTGRES_USER' ]
postgres_password   = os.environ[ 'POSTGRES_PASS' ]
postgres_host       = os.environ[ 'POSTGRES_HOST' ]
work_dir            = os.environ[ 'WORK_DIR']
twisted_ballotregulator_port = int(os.environ[ 'TWISTED_BALLOTREGULATOR_PORT'])
twisted_ballotregulator_ip = os.environ[ 'TWISTED_BALLOTREGULATOR_IP']

@run_in_reactor
@inlineCallbacks
def getAllBallots():
    """
    http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

    Blocking call to the ballot server to request all the ballots.

    :return: EventualResult
    """

    # NOTE: using inline callbacks here so we dont have to write/wait for callbacks.


    print("twisted_ballotregulator_ip:", twisted_ballotregulator_ip)


    destination_deferred = yield TCP4ClientEndpoint(reactor, twisted_ballotregulator_ip, twisted_ballotregulator_port)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(OnlineBallotRegulator_SearchBallotsAvailableForAllBallots)

    def format_results(pickled_result):

        # First unpickle the results.
        result = pickle.loads(pickled_result['ok'])

        # Transform the list results into a dictionary.
        record_list = []
        for record in result:
            mapper = {}
            mapper['ballot_id'] = record[0]
            mapper['ballot_name'] = record[1]
            mapper['ballot_address'] = record[2]
            mapper['timestamp'] = record[3]
            # Append each row's dictionary to a list
            record_list.append(mapper)

        return record_list

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))

def generate_ballot_keys():
    print ("[initialSetup] Checking we have RSA keys for each ballot.")

    # Make sure there are pub/priv keys for each ballot.
    all_ballots = getAllBallots().wait(5)

    if not os.path.exists(work_dir + "signatures/keys/"):
        os.makedirs(work_dir + "signatures/keys/")

    for row in all_ballots:
        ballot_id = row['ballot_id']
        check_path_public = work_dir + "signatures/keys/" + str(ballot_id) + "_ballot_public.pem"
        check_path_private = work_dir + "signatures/keys/" + str(ballot_id) + "_ballot_private.pem"

        if not os.path.exists(check_path_public) or not os.path.exists(check_path_private):
            # Generate ballot keys
            print("[initialSetup] Generating ballot keys for ballot_id=%s" % ballot_id)
            print("    %s\n    %s" % (check_path_public, check_path_private))

            # Genearet private key
            call(['openssl', 'genrsa', '-out', check_path_private, '2048'])

            # Generate public key - openssl rsa -in private.pem -outform PEM -pubout -out public.pem
            call(['openssl', 'rsa', '-in', check_path_private, '-outform', 'PEM', '-pubout', '-out', check_path_public])

def main():

    # print the connection string we will use to connect
    print ("[initialSetup] Connecting to database\n"
           "    -> database:'%s' user:'%s' host:'%s'" % (postgres_database, postgres_user, postgres_host) )

    # get a connection, if a connect cannot be made an exception will be raised here
    connection = psycopg2.connect(database=postgres_database, user=postgres_user, host=postgres_host, password=postgres_password)
    cursor = connection.cursor()

    print( "[initialSetup] Creating tables if they do not exist." )

    # Table to hold token request information
    cursor.execute( "CREATE TABLE IF NOT EXISTS token_request ("
                        "token_request_id serial PRIMARY KEY, "
                        "blind_token_hash varchar(1000) UNIQUE, "
                        "user_id integer NOT NULL, "
                        "ballot_id integer NOT NULL, "
                        "created_on timestamp DEFAULT CURRENT_TIMESTAMP, "
                        "UNIQUE (user_id, ballot_id)"
                    ");")

    # Table to hold token registration information
    cursor.execute( "CREATE TABLE IF NOT EXISTS register_vote ("
                        "register_vote_id serial PRIMARY KEY, "
                        "signed_token_hash varchar(1000) UNIQUE, "
                        "voter_address varchar(50) NOT NULL, "
                        "ballot_id integer NOT NULL, "
                        "created_on timestamp DEFAULT CURRENT_TIMESTAMP, "
                        "UNIQUE (voter_address, ballot_id)"
                    ");")

    connection.commit()

    generate_ballot_keys()

    #TODO remove testing data

    # try:
        # cursor.execute("INSERT INTO token_request (user_id, ballot_id, blind_token_hash) VALUES (2345, 4321, 'ThisIsABlineToken_1234_5431');")
        # cursor.execute("INSERT INTO token_request (user_id, ballot_id, blind_token_hash) VALUES (2345, 5432, 'ThisIsABlineToken_2345_5432');")

        # connection.commit()
    # except:
        # print( "[initialSetup] Error inserting test data." )


    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
