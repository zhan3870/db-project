import sqlite3
from Parser import Parser
import time

class DBEngine:
    def __init__(self):
        self.conn = sqlite3.connect('./database/test.db')
        self.c = self.conn.cursor()
        self.p = Parser()

    def write_states(self):
        self.c.execute("Drop table state")
        self.conn.commit()
        print('TABLE DROPPED')

        self.c.execute('''CREATE TABLE state
        (state_id INTEGER PRIMARY KEY,
        name TEXT,
        population INTEGER)
        ''')

        print('TABLE CREATED')

        tuples = []
        for s in self.p.states:
            tuples.append((s.get_state(), s.get_population()))

        self.c.executemany('''INSERT INTO state (name, population) Values (?, ?)''', tuples)
        self.conn.commit()

        print('DONE')

        print('TEST')
        self.check('SELECT * FROM state;')

    def write_flights(self):
        self.c.execute("Drop table flight")
        self.conn.commit()

        print("TABLE DROPPED")

        self.c.execute('''Create Table flight
        (flight_id INTEGER PRIMARY KEY,
        to_state TEXT,
        from_state INTEGER,
        flight_date TEXT)
        ''')

        print('Table CREATED')

        print('WRITING 2019 FLIGHTS')

        i = 0
        tuples = []
        for f in self.p.f_2019:
            tuples.append((self.get_state_id(f.get_to_state()), self.get_state_id(f.get_from_state()), f.get_date()))
            print('Flight - 2019' + ' ' + str(i))
            i = i + 1

        print('DONE 2019')

        i = 0
        for f in self.p.f_2020:
            tuples.append((self.get_state_id(f.get_to_state()), self.get_state_id(f.get_from_state()), f.get_date()))
            print('Flight - 2020' + ' ' +str(i))
            i = i + 1

        print('DONE 2020')

        self.c.executemany('''INSERT INTO flight (to_state, from_state, flight_date) Values (?,?,?)''', tuples)
        self.conn.commit()
        print('DONE')

        print('TEST')
        self.check('SELECT * FROM flight;')

    def write_flights_index(self):
        self.c.execute("Drop table flight_index_date")
        self.conn.commit()

        print("TABLE DROPPED")

        self.c.execute('''Create Table flight_index_date
        (flight_id INTEGER PRIMARY KEY,
        to_state INTEGER,
        from_state INTEGER,
        flight_date TEXT)
        ''')

        print('Table CREATED')

        print('WRITING 2019 FLIGHTS')

        i = 0
        tuples = []
        for f in self.p.f_2019:
            tuples.append((self.get_state_id(f.get_to_state()), self.get_state_id(f.get_from_state()), f.get_date()))
            print('Flight - 2019' + ' ' + str(i))
            i = i + 1

        print('DONE 2019')

        i = 0
        for f in self.p.f_2020:
            tuples.append((self.get_state_id(f.get_to_state()), self.get_state_id(f.get_from_state()), f.get_date()))
            print('Flight - 2020' + ' ' +str(i))
            i = i + 1

        print('DONE 2020')

        self.c.executemany('''INSERT INTO flight_index_date (to_state, from_state, flight_date) Values (?,?,?)''', tuples)
        self.conn.commit()
        print('DONE')

        self.c.execute('''CREATE INDEX index_flight_date ON flight_index_date (flight_date);''')
        self.c.execute('''CREATE INDEX index_to_state ON flight_index_date (to_state);''')
        self.c.execute('''CREATE INDEX index_from_state ON flight_index_date (from_state);''')

        print('INDEX CREATED')

        print('TEST')
        self.check('SELECT * FROM flight_index_date;')

    def write_covid(self):
        self.c.execute("Drop table covid")
        self.conn.commit()

        print("TABLE DROPPED")

        self.c.execute('''Create Table covid
        (covid_id INTEGER PRIMARY KEY,
        state_id INTEGER,
        date TEXT,
        total_cases INTEGER,
        death_total INTEGER,
        recovered_total INTEGER);
        ''')

        print('TABLE CREATED')

        tuples = []
        for c in self.p.covid:
            tuples.append((self.get_state_id(c.get_state()), c.get_date(), c.get_total_cases(), c.get_death(), c.get_recovered()))

        self.c.executemany('''INSERT INTO covid (state_id, date, total_cases, death_total, recovered_total) Values (?,?,?,?,?)''', tuples)
        self.conn.commit()
        print('DONE')

        print('TEST')
        self.check('SELECT * FROM covid;')

    def get_state_id(self, name):
        #get a state id like:
        #mn = db.get_state_id("Minnesota")
        self.c.execute("Select state_id From state where name=?", (name,))
        for row in self.c.fetchall():
            return row[0]

    def check(self, q):
        #returns a set of tuples for any query
        self.c.execute(q)
        return self.c.fetchall()

    def write_all(self):
        #this will clear the db, and rewrite all the data
        #should print the new data set
        self.p.read_data()
        self.write_states()
        self.write_flights()
        self.write_covid()
        self.write_flights_index()
        print('DB DONE')

    def time_query(self, query):
        start = time.time()
        result = self.check(query)
        end = time.time()

        return ((end - start), result)


db = DBEngine()

#can get a timed result on a query like:
#returns a tuple with [0] being the time and [1] being a list of the query result
result = db.time_query('Select * From flight_index_date Order BY flight_date;')
#result = db.time_query('Select * From covid Order BY date;')
print (result)
