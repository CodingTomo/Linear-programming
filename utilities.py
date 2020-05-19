from ortools.sat.python import cp_model
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
    p_w = df.copy().drop(['bu_1', 'bu_2', 'bu_3',
                          'manager_1', 'manager_2', 'manager_3',
                          's_manager_1',
                          'revenue', 'difficulty', 'eta',
                          'dimension', 'home_eff', 'project'], axis=1)

    p_o = df.copy()[['revenue', 'home_eff']]

    p_m = df.copy()[['manager_1', 'manager_2', 'manager_3']]

    return p_w, p_o, p_m


def all_scores(solution, projects_attributes):
    objective = []
    p_sol = solution.copy().drop(['bacchetta', 'manager_1', 'manager_2', 'manager_3'], axis=1)
    for i in range(p_sol.shape[0]):
        cum = 0
        for j in range(p_sol.shape[1]):
            if solution.iloc[i][j] == 1:
                cum = cum + projects_attributes['revenue'][j]
            else:
                cum = cum + int(projects_attributes['revenue'][j] * projects_attributes['home_eff'][j])
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


def export_xlsx(all_solutions, best_solution_detail):
    writer = pd.ExcelWriter('data/output.xlsx', engine='xlsxwriter')

    all_solutions.to_excel(writer, sheet_name='all_solutions', index=None)
    best_solution_detail.to_excel(writer, sheet_name='best_solution_detail', index=None)

    writer.save()

    return

