import pandas as pd


class Loader:
    def __init__(self):
        self.data = pd.read_excel("data/Projects.xlsx")
        self.one_solution = 0
        self.seats = 17
        self.n_projects = self.data.shape[0]
        self.n_managers = 3

