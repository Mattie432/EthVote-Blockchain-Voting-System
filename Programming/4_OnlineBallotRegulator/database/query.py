import os
from twisted.enterprise.adbapi import ConnectionPool


class DatabaseQuery:

    def __init__(self):
        # Import postgres & twisted credentials from environment. Throws if does not exist.
        self.postgres_database   = os.environ[ 'POSTGRES_DATABASE' ]
        self.postgres_user       = os.environ[ 'POSTGRES_USER' ]
        self.postgres_password   = os.environ[ 'POSTGRES_PASS' ]
        self.postgres_host       = os.environ[ 'POSTGRES_HOST' ]

    def connect(self):

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
        if 'dbConnection' in dir(self):
            return self.dbConnection
        else:
            raise ConnectionError

    def search_userid(self, user_id):

        def onSuccess(results):
            print (" onQuerySuccess !!!")
            print(results)
            print(type (results))
            # return {'ok' : False}
            return {'ok' : str.encode(str(results))}

        def onError(error):
            print (" onError !!!")
            print(type(error))
            print(error.getErrorMessage())

        query = "SELECT * FROM ballot_register WHERE user_id=%s;" % user_id
        deferred = self.dbConnection.runQuery(query)
        print(deferred)
        deferred.addCallback(onSuccess)
        # deferred.addErrback(onError)

        return deferred
