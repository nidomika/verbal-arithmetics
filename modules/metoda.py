import copy


class BacktrackingSearch:
    def __init__(self, problem, enable_mrv=True, enable_degree=False, enable_forward_checking=True):
        self.problem = problem
        self.enable_mrv = enable_mrv
        self.enable_degree = enable_degree
        self.enable_forward_checking = enable_forward_checking
        self.backtrack_count = 0
        self.node_count = 0

    def solve(self):
        return [self.backtracking(self.problem.assignments), self.node_count, self.backtrack_count]

    def backtracking(self, assignments):
        if self.is_complete(assignments):
            return assignments

        variable = self.get_unassigned_var(assignments)
        domains = copy.deepcopy(self.problem.variables[variable].get_domain().get_domain_list())
        for value in domains:
            self.node_count += 1
            if self.check_consistency(assignments, variable, value):
                assignments[variable] = value
                if self.enable_forward_checking:
                    self.problem.update_domains(variable, value)
                    if not self.forward_check(assignments):
                        # Jeśli Forward Checking zwróci `False`, anuluj przypisanie i kontynuuj
                        self.problem.cancel_domains(variable, value)
                        assignments.pop(variable)
                        continue

                result = self.backtracking(assignments)
                if result is not None:
                    return result

                if self.enable_forward_checking:
                    self.problem.cancel_domains(variable, value)
                self.backtrack_count += 1
                assignments.pop(variable)
        return None

    def is_complete(self, assignments):
        return len(assignments) == len(self.problem.variables)

    def check_consistency(self, assignment, new_variable, new_value):
        assignment_copy = copy.deepcopy(assignment)
        assignment_copy[new_variable] = new_value
        for constraint in self.problem.constraints:
            if not constraint.is_consistent(assignment_copy):
                return False
        return True

    def get_unassigned_var(self, assignments):
        if self.enable_mrv:
            unassigned_variables = sorted(list(filter(lambda x: x not in assignments, self.problem.variables)))
            return min(unassigned_variables, key=lambda x: len(self.problem.variables[x].domain.domain))
        elif self.enable_degree:
            return self.degree(assignments)
        else:
            for var in sorted(self.problem.variables):
                if var not in assignments:
                    return var

    def degree(self, assignments):
        unassigned_variables = sorted([v for v in self.problem.variables if v not in assignments])
        most_constraining = None
        max_constraints = -1
        for var in unassigned_variables:
            num_constraints = self.count_constraints(var)
            if num_constraints > max_constraints:
                max_constraints = num_constraints
                most_constraining = var
        return most_constraining

    def count_constraints(self, variable):
        count = 0
        for constraint in self.problem.constraints:
            if variable in constraint.variables:
                count += 1
        return count

    def forward_check(self, assignments):
        # Sprawdzenie, czy po przypisaniu wartości żadna dziedzina nie jest pusta
        for variable, domain in self.problem.variables.items():
            if variable not in assignments and not domain.get_domain():
                return False
        return True

    def update_domains(self, var, value):
        self.problem.update_domains(var, value)

    def cancel_domains(self, var, value):
        self.problem.cancel_domains(var, value)
