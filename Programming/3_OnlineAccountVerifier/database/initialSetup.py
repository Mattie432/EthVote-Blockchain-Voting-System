import psycopg2, os

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


    # cursor.execute( "CREATE TABLE IF NOT EXISTS users ("
    #                     "user_id integer PRIMARY KEY, "
    #                     "ballot_id varchar(10) NOT NULL, "
    #                     "created_on timestamp NOT NULL"
    #                 ");")

    print( "[initialSetup] Creating tables if they do not exist." )

    # Table to hold token request information
    cursor.execute( "CREATE TABLE IF NOT EXISTS token_request ("
                        "blind_token varchar(50) UNIQUE PRIMARY KEY, "
                        "user_id integer NOT NULL, "
                        "ballot_id integer NOT NULL, "
                        "created_on timestamp NOT NULL"
                    ");")

    # Table to hold token registration information
    cursor.execute( "CREATE TABLE IF NOT EXISTS register_vote ("
                        "signed_token varchar(50) UNIQUE PRIMARY KEY, "
                        "voter_address varchar(10) NOT NULL, "
                        "ballot_id integer NOT NULL, "
                        "created_on timestamp NOT NULL"
                    ");")

    connection.commit()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
