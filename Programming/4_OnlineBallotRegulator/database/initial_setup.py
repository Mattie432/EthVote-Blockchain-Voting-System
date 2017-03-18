import psycopg2, os
from psycopg2.extensions import adapt


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
                        "created_on timestamp DEFAULT CURRENT_TIMESTAMP, "
                        "ballot_interface varchar(5000) NOT NULL "
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

        ballot_interface = """[{"constant":false,"inputs":[{"name":"_votingOptionIndex","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_votingOptionName","type":"string"}],"name":"addVotingOption","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"getRegisteredVoterCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finalizeVotingOptions","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"getBallotName","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_voter","type":"address"}],"name":"giveRightToVote","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"voters","outputs":[{"name":"eligableToVote","type":"bool"},{"name":"voted","type":"bool"},{"name":"votedFor","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_index","type":"uint256"}],"name":"getVotingOptionsVoteCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_index","type":"uint256"}],"name":"getVotingOptionsName","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"getVotingOptionsLength","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"votingOptions","outputs":[{"name":"name","type":"string"},{"name":"voteCount","type":"uint256"}],"payable":false,"type":"function"},{"inputs":[{"name":"_ballotName","type":"string"},{"name":"_ballotEndTime","type":"uint256"}],"payable":false,"type":"constructor"}]"""

        cursor.execute("INSERT INTO available_ballots (ballot_id, ballot_name, ballot_address, ballot_interface) VALUES (%s, %s, %s, %s);", (4321, 'Selly Oak Regional', '0xB476f990B00995ae3F70C9A972811E6fF506De65', ballot_interface))
        cursor.execute("INSERT INTO available_ballots (ballot_id, ballot_name, ballot_address, ballot_interface) VALUES (%s, %s, %s, %s);", (5432, 'Birmigham City Council', '0xB476f990B00995ae3F70C9A972811E6fF506De66', ballot_interface))
        cursor.execute("INSERT INTO available_ballots (ballot_id, ballot_name, ballot_address, ballot_interface) VALUES (%s, %s, %s, %s);", (6543, 'London', '0xB476f990B00995ae3F70C9A972811E6fF506De67', ballot_interface))
        connection.commit()
    except Exception as e:
        print( "[initialSetup] Error inserting test data in available_ballots." )
        # print(e)

    try:
        cursor.execute("INSERT INTO ballot_register (user_id, ballot_id) VALUES (1234, 4321);")
        cursor.execute("INSERT INTO ballot_register (user_id, ballot_id) VALUES (1234, 5432);")
        cursor.execute("INSERT INTO ballot_register (user_id, ballot_id) VALUES (2345, 5432);")
        connection.commit()
    except Exception as e:
        print( "[initialSetup] Error inserting test data in ballot_register." )
        # print(e)

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
