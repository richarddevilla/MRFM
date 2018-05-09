#
# This .py file have functions to generate fake profiles
# and store them in a SQLite and MySQL database
#
import mysql.connector
import time
from faker import Faker
from os import path

#Static variables
BASE_DIR = path.dirname(path.abspath(__file__))
MYSQL_SCHEMA_PATH = path.join(BASE_DIR, 'mysql_schema.sql')
DB_NAME = 'profile_1'

#fake generator profile set to return Australian profiles
fake_gen = Faker('en_AU')

#create MySQL connector and cursor
#change the info here to connect to a different MySQL server
#the current MySQL is being hosted on google cloud
mysql_conn = mysql.connector.connect(user='myuser',
                                     password='MyPassword!',
                                     host='192.168.1.5')
mysql_cursor = mysql_conn.cursor()


def mysql_create_db():
    """
        Create MySQL Database and Tables if not already existing
    """
    print('Checking if MySQL Database exist')
    try:
        with open(MYSQL_SCHEMA_PATH, 'rt') as f:
            schema = f.read().split(';')
            for command in schema:
                mysql_cursor.execute(command)
            print('MySQL Database profile created!')
    except:
        print('MySQL Database already exist')
    finally:
        mysql_conn.database = DB_NAME

def create_fakes(quantity):
    """
    :param quantity: integer
    :return: list of contact info, size of list depends on param quantity
    """
    fakes = []
    for i in range(0,quantity):
        fake=(fake_gen.building_number(),
                        fake_gen.street_name(),
                        fake_gen.city(),
                        fake_gen.postcode(),
                        fake_gen.state_abbr(),
                        'Australia',
                        fake_gen.first_name(),
                        fake_gen.last_name(),
                        fake_gen.phone_number(),
                        fake_gen.phone_number(),
                        fake_gen.date_time_this_century(
                            before_now=True,
                            after_now=False,
                            tzinfo=None)
                 )
        fakes.append(fake)
    return fakes

def insert_fakes(entries):
    """
    :param entries: list of contact info

    function takes a list of mutliple personal info.
     iterate through the info and insert it
     to MySQL and Sqlite3 prints execution time on console
    """
    data = create_fakes(entries)
    mysql_create_entry(data)


def mysql_create_entry(data):
    """
    :param data: list of a single person's info
    function would insert the info to MySQL database
    """

    temp_address = []
    temp_profile = []
    for each in data:
        temp_address.append(each[0:5])
        temp_profile.append(each[6:])
    start = time.clock()
    mysql_cursor.execute("BEGIN;")
    mysql_cursor.executemany("""
                INSERT INTO address(
                `line1`,
                `street`,
                `suburb`,
                `postcode`,
                `state`
                )
                VALUES(
                  %s,%s,%s,%s,%s
                )
              """, (
                temp_address[0:5]
                )
                         )
    mysql_cursor.executemany("""
                INSERT INTO profile(
                `first_name`,
                `last_name`,
                `phone_number1`,
                `phone_number2`,
                `birth_date`,
                `address_id`
                )
                VALUES(
                  %s,%s,%s,%s,%s,LAST_INSERT_ID()
                )
              """, (
                temp_profile[6:]
                )
                         )
    mysql_cursor.execute("COMMIT;")
    end = time.clock()
    print('Insert MySQL with BEGIN...COMMIT total time ' + str(end-start))


def upload_document(id,data,name):
    """
    :param data: list of a single person's info
    function would insert the info to MySQL database
    """
    param = [id,data,name[len(name)-1:][0]]
    print(param)
    mysql_cursor.execute("BEGIN;")
    mysql_cursor.executemany("""
                INSERT INTO document(
                `client_id`,
                `document`,
                `doc_type`                                
                )
                VALUES(
                  %s,%s,%s
                )
              """, (param,)
                         )
    mysql_cursor.execute("COMMIT;")

def mysql_search_data(pattern):
    """
    :param pattern: takes a string
    :return result: list of match

    function takes a pattern and look for the pattern in the MySQL database
    this function would look into all fields and return the list of result
    with the full info of the matches
    """
    mysql_cursor.execute('USE {};'.format(DB_NAME), multi=True)
    pattern = '%'+pattern+'%'
    mysql_cursor.execute("""
                SELECT profile.id, 
                CONCAT_WS(' ',profile.first_name,profile.last_name),
                profile.phone_number1,
                profile.phone_number2,
                profile.birth_date,
                CONCAT_WS(' ',address.line1,
                address.street,
                address.suburb,
                address.postcode,
                address.state,
                address.country)
                FROM profile
                LEFT JOIN address ON  profile.address_id=address.id
                WHERE profile.first_name LIKE %s
                OR profile.last_name LIKE %s
                OR profile.phone_number1 LIKE %s
                OR profile.phone_number2 LIKE %s
                OR profile.birth_date LIKE %s
                OR address.line1 LIKE %s
                OR address.street LIKE %s
                OR address.suburb LIKE %s
                OR address.postcode LIKE %s
                OR address.state LIKE %s
                OR address.country LIKE %s;
              """, ([pattern]*11)
                         )
    result=[]
    for each in mysql_cursor.fetchall():
        result.append(each)
    print('MySQL Database searched!!')
    return result

def mysql_search_index(pattern):
    """
    :param pattern: takes a string
    :return result: list of match

    function takes a pattern and look for the pattern in the MySQL database
        this function would look into index and return the full info of the match
    """
    pattern = pattern
    mysql_cursor.execute("""
                SELECT CONCAT_WS(' ',profile.first_name,profile.last_name),
                profile.phone_number1,
                profile.phone_number2,
                profile.birth_date,
                CONCAT_WS(' ',address.line1,
                address.street,
                address.suburb,
                address.postcode,
                address.state,
                address.country)
                FROM profile
                LEFT JOIN address ON  profile.address_id=address.id
                WHERE profile.id=%s;
              """, [pattern]
                         )
    result=[]
    for each in mysql_cursor.fetchall():
        result.append(each)
    print('MySQL Database index searched!!')
    return result

def search_documents(document_id):
    """
    :param pattern: takes a string
    :return result: list of match

    function takes a pattern and look for the pattern in the MySQL database
        this function would look into index and return the full info of the match
    """
    mysql_cursor.execute("""
                SELECT `id`,`doc_type`
                FROM document
                WHERE client_id=%s;
              """, [document_id,])
    result=[]
    for each in mysql_cursor.fetchall():
        result.append(each)
    print('MySQL Database index searched!!')
    return result

def get_document(id):
    mysql_cursor.execute("""
                    SELECT `document`
                    FROM document
                    WHERE id=%s;
                  """, [id, ])
    result = mysql_cursor.fetchone()
    return result[0]

def func_timer(func):
    """
    :param func: takes a function
    :return runtime: time it takes for function to run
    """
    start = time.clock()
    func
    end = time.clock()
    print(end-start)
#calls the create_db functions
mysql_db = mysql_create_db()

#main program to use functions
if __name__ == '__main__':
    while True:
        #Ask user to input quantity of fake records to create
        #it must be a positive integer or 0
        try:
            entries = input('How many records should I insert to SQL?\n'
                            '(more than 10,000 records might take awhile)\n')
            entries = int(entries)
            assert (entries >= 0)
            break
        except (TypeError, ValueError):
            print('Please input an integer')
            continue
        except AssertionError:
            print('Please input a positive integer')
            continue
    #insert fake records to MySQL and Sqlite3
    add_entries = insert_fakes(entries)
    #Ask user to input a general search query
    general_pattern = input('Please input string to search')
    #Run a search to all field in both database and return their time
    func_timer(mysql_search_data(general_pattern))
    #Ask user to input an index search query
    index_pattern = input('Please input index to search')
    # Run a search considering index only in both database and return their time
    func_timer(mysql_search_index(index_pattern))
