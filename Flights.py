class Flights:
    def __init__(self, to_state_id, from_state_id, date):
        self.to_state_id = to_state_id
        self.from_state_id = from_state_id
        self.date = date

    def get_to_state(self):
        return self.to_state_id

    def get_from_state(self):
        return self.from_state_id

    def get_date(self):
        return self.date
