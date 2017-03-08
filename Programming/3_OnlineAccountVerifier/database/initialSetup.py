import psycopg2

connection = psycopg2.connect(database='onlineaccountverifier', user='docker', host='localhost')
cursor = connection.cursor()

cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "mydata"))
cursor.execute("SELECT * FROM test;")
connection.commit()
cursor.close()
connection.close()
