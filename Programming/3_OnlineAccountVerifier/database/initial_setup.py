import psycopg2, os

# Import postgres credentials from environment
postgres_database   = os.environ[ 'POSTGRES_DATABASE' ]
postgres_user       = os.environ[ 'POSTGRES_USER' ]
postgres_password   = os.environ[ 'POSTGRES_PASS' ]
postgres_host       = os.environ[ 'POSTGRES_HOST' ]


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
                        "blind_token varchar(50) UNIQUE PRIMARY KEY, "
                        "user_id integer NOT NULL, "
                        "ballot_id integer NOT NULL, "
                        "created_on timestamp DEFAULT CURRENT_TIMESTAMP, "
                        "UNIQUE (user_id, ballot_id)"
                    ");")

    # Table to hold token registration information
    cursor.execute( "CREATE TABLE IF NOT EXISTS register_vote ("
                        "signed_token varchar(50) UNIQUE PRIMARY KEY, "
                        "voter_address varchar(10) NOT NULL, "
                        "ballot_id integer NOT NULL, "
                        "created_on timestamp DEFAULT CURRENT_TIMESTAMP, "
                        "UNIQUE (user_id, ballot_id)"
                    ");")

    connection.commit()


    #TODO remove testing data

    try:
        cursor.execute("INSERT INTO token_request (user_id, ballot_id, blind_token) VALUES (1234, 5432, 'ThisIsABlineToken_1234_5432');")
        cursor.execute("INSERT INTO token_request (user_id, ballot_id, blind_token) VALUES (2345, 5432, 'ThisIsABlineToken_2345_5432');")

        connection.commit()
    except:
        print( "[initialSetup] Error inserting test data." )


    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
