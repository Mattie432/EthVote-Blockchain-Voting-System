import pickle

import psycopg2, os, sys
from psycopg2.extensions import adapt

# Import postgres credentials from environment
postgres_database   = os.environ[ 'POSTGRES_DATABASE' ]
postgres_user       = os.environ[ 'POSTGRES_USER' ]
postgres_password   = os.environ[ 'POSTGRES_PASS' ]
postgres_host       = os.environ[ 'POSTGRES_HOST' ]
work_dir            = os.environ[ 'WORK_DIR' ]

sys.path.insert(0, work_dir + "/") # Hack to work before we've started our project
from ethereum.ethereum import Ethereum

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
                        "ballot_name varchar(500) UNIQUE NOT NULL, "
                        "ballot_address varchar(500) UNIQUE NOT NULL, "
                        "created_on timestamp DEFAULT CURRENT_TIMESTAMP, "
                        "ballot_interface varchar(6000) NOT NULL, "
                        "ballot_end_date integer NOT NULL"
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


    try:

        e = Ethereum()
        ballot_interface = '' #str(e.getBallotInterface())



        cursor.execute("INSERT INTO available_ballots (ballot_id, ballot_name, ballot_address, ballot_interface, ballot_end_date) VALUES (%s, %s, %s, %s, %s);", (1234, 'Election of the Member of Parliament for the Harborne Constituency', '0x80cc71dbd709104d54afdd0a09413571c1f1f2c9', pickle.dumps(ballot_interface), 1603238400))
        cursor.execute("INSERT INTO available_ballots (ballot_id, ballot_name, ballot_address, ballot_interface, ballot_end_date) VALUES (%s, %s, %s, %s, %s);",
                       (4321, 'Election of Police and Crime Commissioner for Edgbaston area', '0x7439C3A100eD66a411b2b1ff9772aB9E9B9060A2', ballot_interface, 1603238400))
        # cursor.execute("INSERT INTO available_ballots (ballot_id, ballot_name, ballot_address, ballot_interface, ballot_end_date) VALUES (%s, %s, %s, %s, %s);",
        #                (5432, 'Birmigham City Council', '0xB476f990B00995ae3F70C9A972811E6fF506De66', ballot_interface, 1603238400))
        cursor.execute("INSERT INTO available_ballots (ballot_id, ballot_name, ballot_address, ballot_interface, ballot_end_date) VALUES (%s, %s, %s, %s, %s);", (6543, 'Referendum on the United Kingdoms membership of the European Union', '0x9c932c2e3866a06b89f0ed2496ddd4240e718a5a', pickle.dumps(ballot_interface), 1603238400))
        # connection.commit()
    except Exception as e:
        print( "[initialSetup] Error inserting test data in available_ballots." )
        # print("\n\n\n", e, "\n\n\n")

    try:
        cursor.execute("INSERT INTO ballot_register (user_id, ballot_id) VALUES (1234, 1234);")
        cursor.execute("INSERT INTO ballot_register (user_id, ballot_id) VALUES (1234, 6543);")

        cursor.execute("INSERT INTO ballot_register (user_id, ballot_id) VALUES (2345, 6543);")
        connection.commit()
    except Exception as e:
        print( "[initialSetup] Error inserting test data in ballot_register." )
        # print(e)

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
