import psycopg2, time
from onlineballotregulator.server_listener import ServerListener

def main(attempt=0):
    try:
        server = ServerListener()
    except psycopg2.Error as e:
        if attempt > 5:
            print("[main] Attempted connection 5 times, quitting...")
            exit()

        print ( "[main] ERROR: when connecting to database. Waiting for 30seconds and retrying...\n\t-> %s" % (e.pgerror) )
        time.sleep(30)

        server = ServerListener(attempt + 1)
    except KeyError as e:
        print("[main] Key value error when trying to start the verifier.\n%s" % e)
        exit()
    except:
        print("[main] An unknown error occurred. Exiting.")
        exit()

    # Lets start the server.
    server.start()

    # Finally call shutdown method.
    server.shutdown()

if __name__ == "__main__":
    main()
