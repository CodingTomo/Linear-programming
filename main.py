import config
import or_model
import utilities

loader = config.Loader()

all_solutions = or_model.build_and_resolve(loader)
best_solution_detail = utilities.get_detail(all_solutions, loader)

utilities.export_xlsx(all_solutions, best_solution_detail)






