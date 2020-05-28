from ortools.sat.python import cp_model
from math import exp
import pandas as pd


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solution_list = []

    def on_solution_callback(self):
        self.__solution_count += 1
        my_dict = {}
        for v in self.__variables:
            my_dict[str(v)] = self.Value(v)
        self.__solution_list.append(my_dict)

    def solution_count(self):
        return self.__solution_count

    def get_solution(self):
        return self.__solution_list


def split_table(df):
    p_w = df.copy().drop(['project', 'bu_1', 'bu_2', 'bu_3',
                          'manager_1', 'manager_2', 'manager_3',
                          's_manager_1',
                          'revenue', 'difficulty', 'eta',
                          'dimension', 'home_eff'], axis=1)

    p_o = df.copy()[['revenue', 'home_eff', 'eta']]

    p_m = df.copy()[['manager_1', 'manager_2', 'manager_3']]

    return p_w, p_o, p_m


def all_scores(solution, projects_attributes):
    objective = []
    p_sol = solution.copy().drop(['bacchetta', 'manager_1', 'manager_2', 'manager_3'], axis=1)
    for i in range(p_sol.shape[0]):
        cum = 0
        for j in range(p_sol.shape[1]):
            if solution.iloc[i][j] == 1:
                cum = cum + projects_attributes['revenue'][j] * exp(-projects_attributes['eta'][j]/40)
            else:
                cum = cum + int(projects_attributes['revenue'][j] * projects_attributes['home_eff'][j]) * exp(-projects_attributes['eta'][j]/40)
        objective.append(cum)

    df = pd.concat([solution, pd.Series(objective, name='objective')], axis=1)

    return df


def get_detail(all_solutions, ld):
    best_solution = all_solutions.sort_values(by=['objective'], ascending=False).head(1)
    index_list = get_project(best_solution)
    detail = ld.data[ld.data.index.isin(index_list)]

    return detail


def get_project(best_solution):
    best_solution = best_solution.drop(['bacchetta', 'manager_1', 'manager_2', 'manager_3'], axis=1)
    index = []
    for j in range(best_solution.shape[1]):
        if best_solution.iloc[0][j] == 1:
            index.append(j)
    return index


def export_xlsx(all_solutions, best_solution_detail, n):
    writer = pd.ExcelWriter('data/output_'+str(n)+'.xlsx', engine='xlsxwriter')

    all_solutions.to_excel(writer, sheet_name='all_solutions_'+str(n), index=None)
    best_solution_detail.to_excel(writer, sheet_name='best_solution_detail_'+str(n), index=None)

    writer.save()

    return


def terminated_projects(df):
    list_terminated_projects = []
    for i in range(df.shape[0]):
        if df['eta'].iloc[i] == 0:
            list_terminated_projects.append(i)
    return list_terminated_projects

