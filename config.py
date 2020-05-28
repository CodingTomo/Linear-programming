import pandas as pd


class Loader:
    def __init__(self):
        self.data = pd.read_excel("data/Projects.xlsx")
        self.one_solution = 0
        self.seats = 13
        self.n_projects = self.data.shape[0]
        self.n_managers = 3
        self.days = 30

    def manage_time_dependencies(self):
        self.data['eta'] = self.data['eta'].map(lambda x: x - 1 if x > 0 else x)


