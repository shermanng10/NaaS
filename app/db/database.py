import psycopg2


def connect_to_db():
    connectionString = 'dbname=naas user=postgres host=localhost'
    try:
        return psycopg2.connect(connectionString)
    except:
        print('Couldn\'t connect to the database.')
