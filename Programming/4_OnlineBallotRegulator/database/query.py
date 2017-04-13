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


    def search_ballot_register_for_user_id(self, user_id):

        """
        Requests all rows ascociated with a user_id from the ballot_register table. Will
        return either a dictionary (onSucsess) or raise an exception (onError) to be
        passed back to the client.

        :param user_id:
        :return:
        """

        def onSuccess(results):
            print ("[DatabaseQuery - retrieve_ballots] - Query sucsess:")
            # pprint.pprint(results, indent=4)

            # Convert list of results to bytes for transport
            encoded_results = pickle.dumps(results)

            return {'ok' : encoded_results}

        def onError(failure):
            print ("[DatabaseQuery - retrieve_ballots] - Query error:")
            pprint.pprint(failure.value)
            raise failure.raiseException()

        query = "SELECT " \
                    "ballot_register.user_id," \
                    "ballot_register.ballot_id," \
                    "ballot_register.created_on," \
                    "available_ballots.ballot_name," \
                    "available_ballots.ballot_address " \
                "FROM " \
                    "available_ballots, " \
                    "ballot_register " \
                "WHERE " \
                    "ballot_register.user_id=%s AND " \
                    "ballot_register.ballot_id=available_ballots.ballot_id;" % user_id
        deferred = self.dbConnection.runQuery(query)
        deferred.addCallback(onSuccess)
        deferred.addErrback(onError)

        return deferred


    def search_ballots_available_for_all_ballots(self):

        """
        Requests all rows from the ballot_register table. Will return either a dictionary
        (onSucsess) or raise an exception (onError) to be passed back to the client.

        :return:
        """

        def onSuccess(results):
            print ("[DatabaseQuery - search_ballots_available_for_all_ballots] - Query sucsess:")
            # pprint.pprint(results, indent=4)

            # Convert list of results to bytes for transport
            encoded_results = pickle.dumps(results)

            return {'ok' : encoded_results}

        def onError(failure):
            print ("[DatabaseQuery - search_ballots_available_for_all_ballots] - Query error:")
            pprint.pprint(failure.value)
            raise failure.raiseException()

        query = "SELECT * FROM available_ballots;"
        deferred = self.dbConnection.runQuery(query)
        deferred.addCallback(onSuccess)
        deferred.addErrback(onError)

        return deferred

    def search_ballots_available_for_ballot_id(self, ballot_id):

        """
        Requests all rows from the ballot_register table. Will return either a dictionary
        (onSucsess) or raise an exception (onError) to be passed back to the client.

        :return:
        """

        def onSuccess(results):
            print ("[DatabaseQuery - search_ballots_available_for_ballot_id] - Query sucsess:")
            # pprint.pprint(results, indent=4)

            # Convert list of results to bytes for transport
            encoded_results = pickle.dumps(results)

            return {'ok' : encoded_results}

        def onError(failure):
            print ("[DatabaseQuery - search_ballots_available_for_all_ballots] - Query error:")
            pprint.pprint(failure.value)
            raise failure.raiseException()

        query = "SELECT * FROM available_ballots WHERE ballot_id=%s;" % ballot_id
        deferred = self.dbConnection.runQuery(query)
        deferred.addCallback(onSuccess)
        deferred.addErrback(onError)

        return deferred

    def insert_into_ballot_register_user_id_ballot_id(self, user_id, ballot_id):

        """
        Request to register a user for a ballot in the ballot_register table. Will return
        True on sucsess or raise an exception on failure which will be passed back to the client.
        :param user_id:
        :return:
        """

        def onSuccess(result):
            print ("[DatabaseQuery - insert_into_ballot_register_user_id_ballot_id] - Insert sucsess:")
            return {'ok' : True}

        def onError(failure):
            print ("[DatabaseQuery - insert_into_ballot_register_user_id_ballot_id] - Insert error:")
            pprint.pprint(failure.value)
            raise failure.raiseException()

        def _insert(cursor, user_id, ballot_id):
            statement = "INSERT INTO ballot_register (user_id, ballot_id) VALUES (%s, %s);" % (user_id, ballot_id)
            cursor.execute(statement)

        deferred = self.dbConnection.runInteraction(_insert, user_id, ballot_id)
        deferred.addCallback(onSuccess)
        deferred.addErrback(onError)

        return deferred

    def insert_into_ballots_available(self, ballot_name, ballot_address, ballot_interface, ballot_end_date):

        """
        Request to register a new ballot in the ballots_available table. Will return
        True on sucsess or raise an exception on failure which will be passed back to the client.
        :param user_id:
        :return:
        """

        def onSuccess(result):
            print ("[DatabaseQuery - insert_into_ballots_available] - Insert sucsess:")
            return { 'ballot_address' : ballot_address}

        def onError(failure):
            print ("[DatabaseQuery - insert_into_ballots_available] - Insert error:")
            pprint.pprint(failure.value)
            raise failure.raiseException()

        def _insert(cursor, ballot_name, ballot_address, ballot_interface, ballot_end_date):


            statement = "INSERT INTO available_ballots (ballot_name, ballot_address, ballot_interface, ballot_end_date) VALUES (%s, %s, %s, %s);" % ( ballot_name, ballot_address, ballot_interface, ballot_end_date)
            print(statement)
            cursor.execute(statement)

        print("\nballot_name\n",ballot_name,"\nballot_address\n",ballot_address,"\nballot_interface\n",ballot_interface,"\nballot_end_date\n",ballot_end_date)

        deferred = self.dbConnection.runInteraction(_insert, ballot_name, ballot_address, ballot_interface, ballot_end_date)
        deferred.addCallback(onSuccess)
        deferred.addErrback(onError)



        return deferred
