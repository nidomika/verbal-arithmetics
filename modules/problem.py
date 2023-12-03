import copy
from abc import ABC, abstractmethod


class CryptarithmeticProblem:
    def __init__(self, first, second, result):
        self.first = first
        self.second = second
        self.result = result
        self.variables = self.get_variables()
        self.assignments = {}
        self.constraints = self.get_constraints()
        self.domain_reduction()

    def domain_reduction(self):
        first_len, second_len, result_len = len(self.first), len(self.second), len(self.result)

        if result_len > first_len and result_len > second_len:
            self.assignments[self.result[0]] = 1
            self.assignments['x'+str(max(len(self.first), len(self.second)) - 1)] = 1
            self.update_domains(self.result[0], 1)
            if first_len != second_len:
                if first_len > second_len:
                    self.assignments[self.first[0]] = 9
                    self.update_domains(self.first[0], 9)
                else:
                    self.assignments[self.second[0]] = 9
                    self.update_domains(self.second[0], 9)

    def get_variables(self):
        variables = list(set(self.first + self.second + self.result))
        variables_elements = {}
        for var in variables:
            domain = self.get_domain(var)
            variables_elements[var] = Variable(var, domain)
        return variables_elements

    def get_constraints(self):
        constraints = []
        variables_copy = copy.deepcopy(list(self.variables.keys()))
        constraints += [AllDifferent(variables_copy)]

        first_padding_list = '0' * (len(self.result) - len(self.first))
        second_padding_list = '0' * (len(self.result) - len(self.second))

        first_reversed = self.first[::-1] + first_padding_list
        second_reversed = self.second[::-1] + second_padding_list
        result_reversed = self.result[::-1]

        previous_carry = None

        for index in range(len(self.result)):
            carry = 'x' + str(index)
            domain = self.get_domain(carry)
            self.variables[carry] = Variable(carry, domain)

            if not previous_carry:
                constraints += [SumEquals([first_reversed[index], second_reversed[index]],
                                          result_reversed[index], carry)]
            else:
                constraints += [SumEquals([first_reversed[index], second_reversed[index], previous_carry],
                                          result_reversed[index], carry)]

            previous_carry = carry

        self.assignments[previous_carry] = 0
        return constraints

    def is_complete(self, assignments):
        return len(assignments) == len(self.variables)

    def get_unassigned_var(self, assignments):
        unassigned_variables = list(filter(lambda x: x not in assignments, self.variables))
        return min(unassigned_variables, key=lambda x: len(self.variables[x].domain.domain))

    def check_consistency(self, assignment, new_variable, new_value):
        assignment_copy = copy.deepcopy(assignment)
        assignment_copy[new_variable] = new_value
        for constraint in self.constraints:
            if not constraint.is_consistent(assignment_copy):
                return False
        return True

    def get_domain(self, var):
        firsts = [self.first[0], self.second[0], self.result[0]]
        if var in firsts:
            return Domain(list(range(1, 10)))
        elif len(var) == 2:
            return Domain([0, 1])
        else:
            return Domain(list(range(0, 10)))

    def update_domains(self, var, value):
        for v in self.variables:
            if v != var and len(var) == 1 and len(v) == 1:  # czyli var i v to nie przeniesienie
                self.variables[v].get_domain().remove_from_domain(value)

    def cancel_domains(self, var, value):
        for v in self.variables:
            if v != var and len(var) == 1 and len(v) == 1:  # czyli var i v to nie przeniesienie
                self.variables[v].get_domain().add_to_domain(value)


class Constraint(ABC):
    @abstractmethod
    def is_consistent(self, assignment):
        pass


# sprawdzenie, czy suma zmiennych jest równa wynikowi
class SumEquals(Constraint):
    def __init__(self, variables, res, carry='0'):
        self.variables = variables
        self.res = res
        self.carry = carry
        self.varList = self.variables + [self.res, self.carry]

    def is_consistent(self, assignment):
        for var in self.varList:
            if var not in assignment:
                return True
        values = list(map(lambda x: assignment[x], self.variables))
        sum_vars = sum(values)
        res_with_carry = assignment[self.res] + (assignment[self.carry] * 10)
        return sum_vars == res_with_carry


# sprawdzenie, czy wszystkie zmienne mają różne wartości
class AllDifferent(Constraint):

    def __init__(self, variables):
        self.variables = variables

    def is_consistent(self, assignment):
        filtered_vars = list(filter(lambda x: (x in assignment) and (len(x) == 1), self.variables))
        values = list(map(lambda x: assignment[x], filtered_vars))
        values_set = set(values)
        return len(values_set) == len(values)


# klasa dziedzicząca po Domain, która dodatkowo przechowuje oryginalną dziedzinę
class Domain:
    def __init__(self, domain):
        self.domain = domain
        self.original_domain = copy.deepcopy(domain)

    # dodaj wartość do domeny po usunięciu przypisania
    def add_to_domain(self, value):
        if value in self.original_domain:
            self.domain += [value]

    # usuń wartość z domeny po przypisaniu
    def remove_from_domain(self, value):
        if value in self.domain:
            self.domain.remove(value)

    def get_next_free_domain(self):
        return self.domain[0]

    def get_domain_list(self):
        return self.domain


class Variable:
    def __init__(self, variable, domain):
        self.variable = variable
        self.domain = domain

    def get_var(self):
        return self.variable

    def get_domain(self):
        return self.domain
