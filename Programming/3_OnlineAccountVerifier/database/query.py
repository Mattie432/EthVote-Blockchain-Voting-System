import os, pprint, pickle, datetime
from twisted.enterprise.adbapi import ConnectionPool


class DatabaseQuery:

    def __init__(self):
        # Import postgres & twisted credentials from environment. Throws if does not exist.
        self.postgres_database   = os.environ[ 'POSTGRES_DATABASE' ]
        self.postgres_user       = os.environ[ 'POSTGRES_USER' ]
        self.postgres_password   = os.environ[ 'POSTGRES_PASS' ]
        self.postgres_host       = os.environ[ 'POSTGRES_HOST' ]

    def connect(self):

        """
        Setup our database connection. Throws if cannot connect.
        """
        print ("[DatabaseQuery] Connecting to database"
           "\n    -> database:'%s' user:'%s' host:'%s'" % (self.postgres_database, self.postgres_user, self.postgres_host) )

        # get a connection, if a connect cannot be made an exception will be raised here
        self.dbConnection = ConnectionPool(
            'psycopg2',
            database=self.postgres_database,
            user=self.postgres_user,
            host=self.postgres_host,
            password=self.postgres_password
        )

        print("[DatabaseQuery] Database connection sucsessful")

    def get_connection(self):
        """
        Returns the database connection so we can access it from an AMP responder
        :return:
        """
        if 'dbConnection' in dir(self):
            return self.dbConnection
        else:
            raise ConnectionError

    def register_token_request(self, blind_token, user_id, ballot_id):

        """
        Register a token signiture request in the database.
        :return:
        """

        def onSuccess(result):
            print ("[DatabaseQuery - register_token_request] - Insert sucsess:")
            return {'ok' : True}

        def onError(failure):
            print ("[DatabaseQuery - register_token_request] - Insert error:")
            pprint.pprint(failure.value)
            raise failure.raiseException()

        def _insert(cursor, user_id, ballot_id):
            statement = "INSERT INTO token_request (blind_token_hash, user_id, ballot_id) VALUES (%s, %s, %s);"
            cursor.execute(statement, (blind_token, user_id, ballot_id))

        deferred = self.dbConnection.runInteraction(_insert, user_id, ballot_id)
        deferred.addCallback(onSuccess)
        deferred.addErrback(onError)

        return deferred

    def retrieve_request_sign(self, user_id):

        """
        Requests all rows ascociated with a user_id from the ballot_register table. Will
        return either a dictionary (onSucsess) or raise an exception (onError) to be
        passed back to the client.

        :param user_id:
        :return:
        """

        def onSuccess(results):
            print ("[DatabaseQuery - retrieve_request_sign] - Query sucsess:")
            pprint.pprint(results, indent=4)

            # Convert list of results to bytes for transport
            encoded_results = pickle.dumps(results)

            return {'ok' : encoded_results}

        def onError(failure):
            print ("[DatabaseQuery - retrieve_request_sign] - Query error:")
            pprint.pprint(failure.value)
            raise failure.raiseException()

        query = "SELECT * FROM token_request WHERE user_id=%s;" % user_id
        deferred = self.dbConnection.runQuery(query)
        deferred.addCallback(onSuccess)
        deferred.addErrback(onError)

        return deferred
