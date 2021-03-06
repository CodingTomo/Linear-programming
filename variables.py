def add_projects(model, n_projects):
    projects = [model.NewIntVar(0, 1, 'project_' + str(i+1)) for i in range(n_projects)]
    return projects


def add_project_conditions(model, n_projects):
    project_conditions = [model.NewBoolVar('project_condition_' + str(i+1)) for i in range(n_projects)]
    return project_conditions


def add_manager_conditions(model, n_managers):
    manager_conditions = [model.NewBoolVar('m_condition_'+str(i+1)) for i in range(n_managers)]
    return manager_conditions


def add_bacchetta(model):
    bacchetta = model.NewIntVar(0, 1, 'bacchetta')
    return bacchetta


def add_managers(model, n_managers):
    managers = [model.NewIntVar(0, 1, 'manager_' + str(i+1)) for i in range(n_managers)]
    return managers


def add_workers(model, n_workers):
    workers = [model.NewIntVar(0, 1, 'worker_' + str(i+1)) for i in range(n_workers)]
    return workers
