class Covid:
    def __init__(self, state, date, total_cases, death_count, recovered):
        self.state = state
        self.date = date
        self.total_cases = total_cases
        self.death_count = death_count
        self.recovered_count = recovered

    def get_state(self):
        return self.state

    def get_date(self):
        return self.date

    def get_total_cases(self):
        return self.total_cases

    def get_death(self):
        return self.death_count

    def get_recovered(self):
        return self.recovered_count
