import config
import or_model
import utilities

loader = config.Loader()
terminated_projects = []
to_print = len(terminated_projects)
for i in range(loader.days):
    print("{}. iteration".format(i))
    all_solutions = or_model.build_and_resolve(loader, terminated_projects)
    best_solution_detail = utilities.get_detail(all_solutions, loader)
    if i == 0 or to_print < len(terminated_projects):
        print('printed')
        utilities.export_xlsx(all_solutions, best_solution_detail, i)
    loader.manage_time_dependencies()
    to_print = len(terminated_projects)
    terminated_projects = utilities.terminated_projects(loader.data)



