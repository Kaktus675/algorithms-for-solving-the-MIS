from test2 import *
from mis import *
import pickle
chc = bool(input("начать тестирование (нажмите enter) или визуализировать один граф (введите любой текст и нажмите enter): "))
def tests():
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
        tests_visual(result, pol[0], pol[1], st)
        visual_func_family(result, pol[0], pol[1], st)
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
def one_graph():
    n = int(input("количество вершин: "))
    h = float(input("связность от 0 до 1, 0 - не связный, 1 - сильносвязный: "))
    graph_ver = [i for i in range(1, n + 1)]
    graph_neighbors = generate_random_graph(n, h)
    result_a1 = find_max_set_a1_py(graph_ver, graph_neighbors, [])
    result_a2 = find_max_set_a2_py(graph_neighbors)
    visual(graph_neighbors, result_a1, result_a2)
if chc:
    one_graph()
else:
    tests()