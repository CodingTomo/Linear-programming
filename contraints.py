
def add_seat_constraints(model, projects, bacchetta, managers, n_seats, n_projects, p_w):
    weighted_sum_project = 0
    for i in range(n_projects):
        weighted_sum_project = weighted_sum_project + projects[i] * p_w.sum(axis=1).iloc[i]
    model.Add(weighted_sum_project + bacchetta + sum(managers) <= n_seats)
    model.Add(weighted_sum_project + bacchetta + sum(managers) > n_seats - 1)

    return


def add_objective_function(model, projects, n_projects, projects_attributes):
    objective_addend_list = []

    for i in range(n_projects):
        if projects[i] == 1:
            addend = int((projects_attributes['revenue'].iloc[i]))
        else:
            addend = int((projects_attributes['revenue'].iloc[i]) * (projects_attributes['home_eff'].iloc[i]))
        objective_addend_list.append(addend)

    model.Maximize(sum(objective_addend_list))

    return


def add_manager_conditions_constraints(model, projects, m_conditions, n_projects, n_managers, project_manager):
    for j in range(n_managers):
        pr_list = []
        for i in range(n_projects):
            if project_manager.iloc[i][j] == 1:
                pr_list.append(projects[i])
        model.Add(sum(pr_list) > 0).OnlyEnforceIf(m_conditions[j])
        model.Add(sum(pr_list) <= 0).OnlyEnforceIf(m_conditions[j].Not())

    return


def add_bacchetta_constraint(model, bacchetta):
    model.Add(bacchetta == 1)

    return


def add_manager_constraints(model, p_conditions, managers, n_managers):
    for j in range(n_managers):
        model.Add(managers[j] == 1).OnlyEnforceIf(p_conditions[j])
        model.Add(managers[j] == 0).OnlyEnforceIf(p_conditions[j].Not())

    return


def add_project_condition_constraint(model, projects, p_conditions, n_projects):
    for i in range(n_projects):
        model.Add(projects[i] == 1).OnlyEnforceIf(p_conditions[i])
        model.Add(projects[i] == 0).OnlyEnforceIf(p_conditions[i].Not())


def add_worker_constraints(model, p_conditions, workers, project_worker):
    # model.Add(workers[i] == 1)
    return


def add_terminated_projects_constraints(model, projects, terminated_projects):
    if len(terminated_projects) > 0:
        for i in terminated_projects:
            model.Add(projects[i] == 0)
    return






