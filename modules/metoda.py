import copy


class BacktrackingSearch:
    def __init__(self, problem, heuristics=None):
        if heuristics is None:
            heuristics = [False, False, False]
        self.problem = problem
        self.enable_mrv = heuristics[0]
        self.enable_degree = heuristics[1]
        self.enable_forward_checking = heuristics[2]
        self.backtrack_count = 0
        self.node_count = 0
        self.reset()

    # rozwiąż problem i zwróć listę [przypisanie, liczba węzłów, liczba powrotów]
    def solve(self):
        return [self.backtracking(self.problem.assignments), self.node_count, self.backtrack_count]

    # zwróć przypisanie lub None, jeśli nie znaleziono rozwiązania
    def backtracking(self, assignments):
        if self.is_complete(assignments):
            return assignments

        variable = self.get_unassigned_var(assignments)
        domains = copy.deepcopy(self.problem.variables[variable].get_domain().get_domain_list())
        for value in domains:
            self.node_count += 1
            if self.check_consistency(assignments, variable, value):
                assignments[variable] = value
                # Forward Checking
                if self.enable_forward_checking:
                    self.problem.update_domains(variable, value)
                    if not self.forward_check(assignments):
                        # jeśli Forward Checking zwróci False, anuluj przypisanie i kontynuuj
                        self.problem.cancel_domains(variable, value)
                        assignments.pop(variable)
                        continue
                # rekurencyjne wywołanie
                result = self.backtracking(assignments)
                if result is not None:
                    return result
                # jeśli Forward Checking jest włączony, anuluj przypisanie
                if self.enable_forward_checking:
                    self.problem.cancel_domains(variable, value)
                self.backtrack_count += 1
                assignments.pop(variable)
        return None

    # zwróć True, jeśli przypisanie jest kompletne - wszystkie zmienne mają wartości
    def is_complete(self, assignments):
        return len(assignments) == len(self.problem.variables)

    # zwróć True, jeśli przypisanie jest spójne - wszystkie ograniczenia są spełnione
    def check_consistency(self, assignment, new_variable, new_value):
        assignment_copy = copy.deepcopy(assignment)
        assignment_copy[new_variable] = new_value
        for constraint in self.problem.constraints:
            if not constraint.is_consistent(assignment_copy):
                return False
        return True

    # zwróć zmienną, która nie ma przypisanej wartości wg wybranej heurystyki
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

    # zwróć zmienną, która ma najwięcej ograniczeń
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

    # zwróć liczbę ograniczeń dla danej zmiennej
    def count_constraints(self, variable):
        count = 0
        for constraint in self.problem.constraints:
            if variable in constraint.variables:
                count += 1
        return count

    # zwróć True, jeśli po przypisaniu wartości żadna dziedzina nie jest pusta
    def forward_check(self, assignments):
        # Sprawdzenie, czy po przypisaniu wartości żadna dziedzina nie jest pusta
        for variable, domain in self.problem.variables.items():
            if variable not in assignments and not domain.get_domain():
                return False
        return True

    # aktualizuj dziedziny zmiennych
    def update_domains(self, var, value):
        self.problem.update_domains(var, value)

    # anuluj aktualizację dziedzin zmiennych
    def cancel_domains(self, var, value):
        self.problem.cancel_domains(var, value)

    # zresetuj liczniki
    def reset(self):
        self.backtrack_count = 0
        self.node_count = 0
