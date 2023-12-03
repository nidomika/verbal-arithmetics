import copy


class BacktrackingSearch:
    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        return self.backtracking(self.problem.assignments)

    def backtracking(self, assignments):
        if self.problem.is_complete(assignments):
            return assignments

        variable = self.problem.get_unassigned_var(assignments)
        domains = copy.deepcopy(self.problem.variables[variable].get_domain().get_domain_list())
        for value in domains:
            if self.problem.check_consistency(assignments, variable, value):
                assignments[variable] = value
                self.problem.update_domains(variable, value)
                result = self.backtracking(assignments)
                if result is not None:
                    return result
                assignments.pop(variable)
                self.problem.cancel_domains(variable, value)
        return None

    def is_complete(self, assignments):
        return self.problem.is_complete(assignments)

    def check_consistency(self, assignment, new_variable, new_value):
        return self.problem.check_consistency(assignment, new_variable, new_value)

    def get_unassigned_var(self, assignment):
        return self.problem.get_unassigned_var(assignment)

    def update_domains(self, var, value):
        self.problem.update_domains(var, value)

    def cancel_domains(self, var, value):
        self.problem.cancel_domains(var, value)
