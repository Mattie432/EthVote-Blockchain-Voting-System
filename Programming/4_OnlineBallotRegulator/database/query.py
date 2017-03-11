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


    def retrieve_ballots(self, user_id):

        """
        Requests all rows ascociated with a user_id from the ballot_register table. Will
        return either a dictionary (onSucsess) or raise an exception (onError) to be
        passed back to the client.

        :param user_id:
        :return:
        """

        def onSuccess(results):
            print ("[DatabaseQuery - retrieve_ballots] - Query sucsess:")
            pprint.pprint(results, indent=4)

            # Convert list of results to bytes for transport
            encoded_results = pickle.dumps(results)

            return {'ok' : encoded_results}

        def onError(failure):
            print ("[DatabaseQuery - retrieve_ballots] - Query error:")
            pprint.pprint(failure.value)
            raise failure.raiseException()

        query = "SELECT * FROM ballot_register WHERE user_id=%s;" % user_id
        deferred = self.dbConnection.runQuery(query)
        deferred.addCallback(onSuccess)
        deferred.addErrback(onError)

        return deferred


    def register_userid_ballotid(self, user_id, ballot_id):

        """
        Request to register a user for a ballot in the ballot_register table. Will return
        True on sucsess or raise an exception on failure which will be passed back to the client.
        :param user_id:
        :return:
        """

        def onSuccess():
            print ("[DatabaseQuery - register_userid_ballotid] - Insert sucsess:")
            return {'ok' : True}

        def onError(failure):
            print ("[DatabaseQuery - register_userid_ballotid] - Insert error:")
            pprint.pprint(failure.value)
            raise failure.raiseException()

        def _insert(cursor, user_id, ballot_id):
            statement = "INSERT INTO ballot_register (user_id, ballot_id) VALUES (%s, %s);" % (user_id, ballot_id)
            cursor.execute(statement)

        deferred = self.dbConnection.runInteraction(_insert, user_id, ballot_id)
        deferred.addCallback(onSuccess)
        deferred.addErrback(onError)

        return deferred
