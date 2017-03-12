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

    cursor.execute( "CREATE TABLE IF NOT EXISTS available_ballots ("
                        "ballot_id serial UNIQUE PRIMARY KEY, "
                        "ballot_name varchar(50) UNIQUE NOT NULL, "
                        "ballot_address varchar(50) UNIQUE NOT NULL, "
                        "created_on timestamp DEFAULT CURRENT_TIMESTAMP "
                    ");")

    cursor.execute( "CREATE TABLE IF NOT EXISTS ballot_register ("
                        "ballot_register_id serial UNIQUE PRIMARY KEY, "
                        "user_id integer NOT NULL, "
                        "ballot_id integer NOT NULL REFERENCES available_ballots(ballot_id) ON DELETE CASCADE, "
                        "created_on timestamp DEFAULT CURRENT_TIMESTAMP, "
                        "UNIQUE (user_id, ballot_id)"
                    ");")

    connection.commit()

    #TODO remove test data

    cursor.execute("INSERT INTO available_ballots (ballot_id, ballot_name, ballot_address) VALUES (4321, 'Selly Oak Regional', '0xd12cd8a37f074e7eafae618c986ff825666198bd');")
    cursor.execute("INSERT INTO available_ballots (ballot_id, ballot_name, ballot_address) VALUES (5432, 'Birmigham City Council', '0x2910543af39aba0cd09dbb2d50200b3e800a63d2');")
    cursor.execute("INSERT INTO available_ballots (ballot_id, ballot_name, ballot_address) VALUES (6543, 'London', '0xfa52274dd61e1643d2205169732f29114bc240b3');")

    connection.commit()

    cursor.execute("INSERT INTO ballot_register (user_id, ballot_id) VALUES (1234, 4321);")
    cursor.execute("INSERT INTO ballot_register (user_id, ballot_id) VALUES (1234, 5432);")
    cursor.execute("INSERT INTO ballot_register (user_id, ballot_id) VALUES (2345, 5432);")

    connection.commit()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
