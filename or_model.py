# OrTools
from ortools.sat.python import cp_model

# custom modules
import utilities
from contraints import add_seat_constraints, add_objective_function, add_bacchetta_constraint,\
                        add_manager_constraints, add_manager_conditions_constraints, add_project_condition_constraint,\
                        add_worker_constraints, add_terminated_projects_constraints

from variables import add_projects, add_manager_conditions, add_bacchetta, add_managers,\
    add_project_conditions, add_workers

# other
import pandas as pd


def build_and_resolve(ld, terminated_projects):
    projects_workers, projects_attributes, project_manager = utilities.split_table(ld.data)
    model = cp_model.CpModel()

    projects = add_projects(model, ld.n_projects)
    bacchetta = add_bacchetta(model)
    managers = add_managers(model, ld.n_managers)
    # workers = add_workers(model, projects_workers.shape[1])
    m_conditions = add_manager_conditions(model, ld.n_managers)
    # p_conditions = add_project_conditions(model, ld.n_projects)

    add_seat_constraints(model, projects, bacchetta, managers, ld.seats, ld.n_projects, projects_workers)
    add_bacchetta_constraint(model, bacchetta)
    add_manager_conditions_constraints(model, projects, m_conditions, ld.n_projects, ld.n_managers, project_manager)
    add_manager_constraints(model, m_conditions, managers, ld.n_managers)
    # add_project_condition_constraint(model, projects, p_conditions, ld.n_projects)
    add_terminated_projects_constraints(model, projects, terminated_projects)

    if ld.one_solution == 1:
        add_objective_function(model, projects, ld.n_projects, projects_attributes)
        find_one_solution(model, projects)
    else:
        solutions = find_all_solution(model, projects, bacchetta, managers)
        df = utilities.all_scores(solutions, projects_attributes)

    return df


def find_one_solution(model, projects):
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    print('Maximum of objective function: %i' % solver.ObjectiveValue())
    for project in projects:
        print('{} : {}'.format(str(project), solver.Value(project)))
    return


def find_all_solution(model, projects, bacchetta, managers):
    solver = cp_model.CpSolver()
    solution_printer = utilities.VarArraySolutionPrinter(projects+[bacchetta]+managers)
    status = solver.SearchForAllSolutions(model, solution_printer)

    print('Status = %s' % solver.StatusName(status))
    print('Number of solutions found: %i' % solution_printer.solution_count())

    solutions = pd.DataFrame(solution_printer.get_solution())

    return solutions

