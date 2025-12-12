from test2 import *
import pickle

sav = bool(input("загрузить готовый тест (нажмите enter) или начать тест (введите любой текст и нажмите enter): "))

if sav:
    n = int(input("количество вершин: "))
    g = int(input("количество тестов для каждой плотности: "))

t = bool(input("многократные тесты (введите любой текст) или одноразовые тесты (нажмите enter без ввода):"))

if t:
    st = int(input("шаг: "))
    if sav:
        result = tests(n, g, st)
        with open('results.pkl', 'wb') as f:
            pickle.dump(result, f)
    else:
        with open('results.pkl', 'rb') as f:
            result = pickle.load(f)
    pol = tests_polinom(result)
    tests_visual(result,pol[0],pol[1],st)
    visual_func_family(result,pol[0],pol[1],st)
else:
    if sav:
        result = test(n, g)
        with open('results.pkl', 'wb') as f:
            pickle.dump(result, f)
    else:
        with open('results.pkl', 'rb') as f:
            result = pickle.load(f)
    pol = test_polinom(result)
    test_visual(result, pol[0], pol[1])

with open('results.pkl', 'wb') as f:
    pickle.dump(result, f)