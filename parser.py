from State import State
from Covid import Covid
from Flights import Flights
from Census import Census
import csv
import glob

class Parser:
    def __init__(self):
        self.flight_2019 = './flight_data/flight_2019.csv'
        self.flight_2020 = './flight_data/flight_2020.csv'
        self.census_path = './census/census.csv'

        self.f_2019 = []
        self.f_2020 = []
        self.states = []
        self.covid = []

    def read_flight_logs(self, file):
        flight_list = []
        with open(file) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                f = Flights(row['ORIGIN_STATE_NM'], row['DEST_STATE_NM'],row['FL_DATE'])
                flight_list.append(f)
        return flight_list

    def get_states(self, f_2019, f_2020, covid):
        state_list = []
        seen = []
        #get all states flown in 2020
        for f in f_2020:
            if f.get_to_state() not in seen:
                seen.append(f.get_to_state())
                s = State(f.get_to_state(), self.get_population(f.get_to_state()))
                state_list.append(s)
            elif f.get_from_state() not in seen:
                seen.append(f.get_from_state())
                s = State(f.get_from_state(), self.get_population(f.get_from_state()))
                state_list.append(s)

        #get all states flown in 2019
        for f in f_2019:
            if f.get_to_state() not in seen:
                seen.append(f.get_to_state())
                s = State(f.get_to_state(), self.get_population(f.get_to_state()))
                state_list.append(s)
            elif f.get_from_state() not in seen:
                seen.append(f.get_from_state())
                s = State(f.get_from_state(), self.get_population(f.get_from_state()))
                state_list.append(s)

        #get all covid cities
        for c in covid:
            if c.get_state() not in seen:
                seen.append(c.get_state())
                s = State(c.get_state(), self.get_population(c.get_state()))
                state_list.append(s)

        return state_list

    def get_covid_csv(self):
        return glob.glob('./covid_data/*.csv')

    def read_covid_data(self):
        covid_list = []
        for file in self.get_covid_csv():
            sub_string = file.split('.')[1]
            date = sub_string.split('/')[2]
            with open(file) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    c = Covid(str(row['Province_State']), self.convert_date(date), str(row['Confirmed']), str(row['Deaths']), str(row['Recovered']))
                    covid_list.append(c)
        return covid_list

    def convert_date(self, date):
        #needs to be year-month-day
        #is month-day-year
        date_list = date.split('-')
        return date_list[2] + '-' + date_list[0] + '-' + date_list[1]

    def read_census(self):
        census_list = []
        with open(self.census_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                c = Census(row['NAME'], row['POPESTIMATE2019'])
                census_list.append(c)
        return census_list

    def get_population(self, state):
        for c in self.census:
            if c.get_state() == state:
                return c.get_population()
        return 0


    def read_data(self):
        print('CENSUS')
        self.census = self.read_census()
        print('2019 Flight Data')
        self.f_2019 = self.read_flight_logs(self.flight_2019)
        print('2020 Flight Data')
        self.f_2020 = self.read_flight_logs(self.flight_2020)
        print('COVID Data')
        self.covid = self.read_covid_data()
        print('State Data')
        self.states = self.get_states(self.f_2019, self.f_2020, self.covid)
        print('DONE Parsing')
