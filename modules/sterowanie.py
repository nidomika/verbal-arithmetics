from problem import CryptarithmeticProblem


def get_user_input():
    # equation = input("Please enter an equation (e.g., SEND + MORE = MONEY): ")
    equation = "TWO + TWO = FOUR"
    equation = equation.replace(" ", "")
    left_side, right_side = equation.split("=")
    addends = left_side.split("+")
    return addends[0], addends[1], right_side


def get_equation(first, second, result):
    if first == "" or second == "" or result == "":
        return "Proszę wprowadzić prawidłowe równanie (np. TWO + TWO = FOUR)."
    if len(set(first + second + result)) > 10:
        return "Proszę wprowadzić równanie składające się z maksymalnie 10 różnych znaków."
    if any(char.isdigit() for char in first+second+result):
        return "Proszę wprowadzić tylko litery."
    elif len(first) > len(result) or len(second) > len(result):
        return "Dodawane liczby nie mogą być dłuższe niż wynik."
    return "OK"


def solve_problem(first, second, result):
    solver = CryptarithmeticProblem(first, second, result)
    return solver.backtracking(solver.assignments)


def get_string_answer(response, first, second, result):
    if response != -1:
        first_value = int("".join(list(map(lambda c: str(response[c]), first))))
        second_value = int("".join(list(map(lambda c: str(response[c]), second))))
        result_value = int("".join(list(map(lambda c: str(response[c]), result))))
        string_result = str(first_value) + " + " + str(second_value) + " = " + str(result_value)
        return string_result


def main():
    first, second, third = get_user_input()
    message = get_equation(first, second, third)
    if message != "OK":
        print(message)
    else:
        result = solve_problem(first, second, third)

        if result is None:
            print("Nie znaleziono rozwiązania.")
        else:
            print("Znaleziono rozwiązanie dla równania:")
            print(first + " + " + second + " = " + third)
            print(get_string_answer(result, first, second, third))


if __name__ == "__main__":
    main()
