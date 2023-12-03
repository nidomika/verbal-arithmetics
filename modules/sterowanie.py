import time
from metoda import BacktrackingSearch
from problem import CryptarithmeticProblem


def get_user_input():
    # equation = input("Proszę wpisać równanie (np. SEND + MORE = MONEY): ")
    # equation = "TWO + TWO = FOUR"
    # equation = "NUM + BER = PLAY"
    equation = "SEND + MORE = MONEY"
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
    problem = CryptarithmeticProblem(first, second, result)
    solver = BacktrackingSearch(problem)
    return solver.solve()


def get_string_answer(response, first, second, result):
    if response is not None:
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
        time_start = time.time()
        result = solve_problem(first, second, third)
        time_end = time.time()
        if result[0] is None:
            print("Nie znaleziono rozwiązania.")
        else:
            print("Znaleziono rozwiązanie dla równania:")
            print(first + " + " + second + " = " + third)
            print(get_string_answer(result[0], first, second, third))

        print("Czas wykonania: " + str(time_end - time_start) + "s")
        print("Liczba węzłów: " + str(result[1]))
        print("Liczba powrotów: " + str(result[2]))


if __name__ == "__main__":
    main()
