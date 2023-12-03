import time
from metoda import BacktrackingSearch
from problem import CryptarithmeticProblem


# pobierz input od użytkownika
def get_user_input():
    equation = input("Proszę wpisać równanie (np. SEND + MORE = MONEY): ")
    enable_mrv = input("Czy włączyć usprawnienie MRV ('najbardziej ograniczona zmienna')? (y/n): ")
    enable_degree = input("Czy włączyć usprawnienie degree ('najbardziej ograniczająca zmienna')? (y/n): ")
    enable_forward_checking = input("Czy włączyć usprawnienie FC (sprawdzanie w przód)? (y/n): ")

    if enable_mrv == "y":
        enable_mrv = True
    else:
        enable_mrv = False
    if enable_degree == "y":
        enable_degree = True
    else:
        enable_degree = False
    if enable_forward_checking == "y":
        enable_forward_checking = True
    else:
        enable_forward_checking = False

    equation = equation.replace(" ", "")
    left_side, right_side = equation.split("=")
    addends = left_side.split("+")
    return [addends[0], addends[1], right_side], [enable_mrv, enable_degree, enable_forward_checking]


# pobierz input z pliku
def get_inputs_from_file():
    inputs = []
    try:
        with open("input.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                equation, enable_mrv, enable_degree, enable_forward_checking = line.split(";")
                equation = equation.replace(" ", "")
                left_side, right_side = equation.split("=")
                addends = left_side.split("+")
                if len(addends) != 2:
                    return "Niepoprawny format równania. Powinno być w formacie: SEND+MORE=MONEY"
                inputs.append(
                    [[addends[0], addends[1], right_side], [enable_mrv, enable_degree, enable_forward_checking]])
            return inputs
    except FileNotFoundError:
        return "Nie znaleziono pliku 'input.txt'."
    except ValueError:
        return "Plik 'input.txt' jest niepoprawnie sformatowany. Powinien być w formacie: EQUATION;MRV;DEGREE;" \
                  "FORWARD_CHECKING, gdzie MRV, DEGREE, FORWARD_CHECKING to wartości True/False, a EQUATION to " \
                  "równanie w formacie: SEND+MORE=MONEY "


# sprawdź poprawność wpisanego równania
def get_equation(first, second, result):
    if first == "" or second == "" or result == "":
        return "Proszę wprowadzić prawidłowe równanie (np. TWO + TWO = FOUR)."
    if len(set(first + second + result)) > 10:
        return "Proszę wprowadzić równanie składające się z maksymalnie 10 różnych znaków."
    if any(char.isdigit() for char in first + second + result):
        return "Proszę wprowadzić tylko litery."
    elif len(first) > len(result) or len(second) > len(result):
        return "Dodawane liczby nie mogą być dłuższe niż wynik."
    return "OK"


# zwróć string z rozwiązaniem w formacie "123+456=789"
def get_string_answer(response, first, second, result):
    if response is not None:
        first_value = int("".join(list(map(lambda c: str(response[c]), first))))
        second_value = int("".join(list(map(lambda c: str(response[c]), second))))
        result_value = int("".join(list(map(lambda c: str(response[c]), result))))
        string_result = str(first_value) + "+" + str(second_value) + "=" + str(result_value)
        return string_result


# rozwiąż równanie wprowadzone z klawiatury
def solve_equation_from_keyboard():
    equation, heuristics = get_user_input()
    message = get_equation(equation[0], equation[1], equation[2])
    if message != "OK":
        print(message)
    else:
        time_start = time.time()
        result = solve_problem(equation[0], equation[1], equation[2], heuristics)
        time_end = time.time()
        if result[0] is None:
            print("Nie znaleziono rozwiązania.")
        else:
            print("\nZnaleziono rozwiązanie dla równania:")
            print(equation[0] + "+" + equation[1] + "=" + equation[2])
            print(get_string_answer(result[0], equation[0], equation[1], equation[2]))

            print("\nCzas wykonania: " + str(time_end - time_start) + "s")
            print("Liczba węzłów: " + str(result[1]))
            print("Liczba powrotów: " + str(result[2]))


# rozwiąż równania z pliku i zapisz je do pliku
def solve_equations_from_file():
    inputs = get_inputs_from_file()
    if type(inputs) is str:
        print(inputs)
    else:
        results = []
        i = 1
        for equation, heuristics in inputs:
            heuristics = list(map(lambda x: x == "True", heuristics))
            print("Rozwiązywanie równania:", i, "z", len(inputs))
            time_start = time.time()
            result = solve_problem(equation[0], equation[1], equation[2], heuristics)
            time_end = time.time()
            time_elapsed = time_end - time_start
            if result[0] is None:
                results.append("Nie znaleziono rozwiązania.")
            else:
                solution = get_string_answer(result[0], equation[0], equation[1], equation[2])
                results.append(
                    equation[0] + "+" + equation[1] + "=" + equation[2] + ";" +
                    str(heuristics[0]) + ";" + str(heuristics[1]) + ";" + str(heuristics[2]) + ";" +
                    str(time_elapsed) + ";" + str(result[1]) + ";" + str(result[2]) + ";" + solution)
            i += 1
        save_results_to_file(results)
        print("Rozwiązania zapisano do pliku output.csv.")


# zapisz rozwiązania do pliku output.csv
def save_results_to_file(results):
    with open("output.csv", "w") as file:
        file.write("EQUATION;MRV;DEGREE;FORWARD_CHECKING;TIME;NODES;BACKTRACKS;SOLUTION\n")
        for result in results:
            file.write(result + "\n")


# rozwiąż problem i zwróć listę [przypisanie, liczba węzłów, liczba powrotów]
def solve_problem(first, second, result, heuristics):
    problem = CryptarithmeticProblem(first, second, result)
    solver = BacktrackingSearch(problem, heuristics)
    return solver.solve()


def main():
    print("Proszę wybrać tryb działania programu:")
    print("1. Wprowadzenie równania z klawiatury")
    print("2. Wczytanie równań z pliku input.txt i zapis do pliku output.txt")
    choice = input("Wybór: ")
    if choice == "1":
        solve_equation_from_keyboard()
    elif choice == "2":
        solve_equations_from_file()
    else:
        print("Proszę wprowadzić poprawny wybór.")


if __name__ == "__main__":
    main()
