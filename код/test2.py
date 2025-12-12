import clr
import os
import random
import matplotlib.pyplot as plt
import time
import numpy as np
from matplotlib.widgets import Slider
from scipy import linalg

# Загружаем DLL
current_dir = os.path.dirname(os.path.abspath(__file__))
# Формируем путь к DLL в той же папке
dll_path = os.path.join(current_dir, "Class1.dll")
clr.AddReference(dll_path)
from Class1 import Solver

#генерация графа
def generate_random_graph(n_ver, edge_probability):
    graph = {i: [] for i in range(1, n_ver + 1)}
    for i in range(1, n_ver + 1):
        for j in range(i + 1, n_ver + 1):
            if random.random() < edge_probability:
                graph[i].append(j)
                graph[j].append(i)
    return graph
#поиск максимального независимого множества точным алгоритмом
def find_max_set_a1_cs(graph, neighbors):
    #Быстрая C# версия алгоритма A1
    neighbor_keys = list(neighbors.keys())
    neighbor_arrays = [neighbors[key] for key in neighbor_keys]
    return list(Solver.FindMaxSetA1_Simple(graph, neighbor_keys, neighbor_arrays))
#поиск максимально независимого множество эвристическим алгоритмом
def find_max_set_a2_cs(neighbors):
    #Быстрая C# версия алгоритма A2
    neighbor_keys = list(neighbors.keys())
    neighbor_arrays = [neighbors[key] for key in neighbor_keys]
    return list(Solver.FindMaxSetA2_Simple(neighbor_keys, neighbor_arrays))
# тесты для графов с n вершинами
def test(max_ver,number_of_test_graphs):
    densities = [i * 0.005 for i in range(201)]
    results = {
        'плотность': [],
        'время точного': [],
        'время жадного': [],
        'размер точного': [],
        'размер жадного': [],
        'точность': [],
        'отношение скоростей': [],
    }
    for i in densities:
        print(f"Тестируем плотность {i}...")
        exact_times = [] #время точного алгоритма
        greedy_times = [] # время жадного алгоритма
        exact_sizes = [] # число вершин в точном алгоритме
        greedy_sizes = [] # число вершин в жадном алгоритме
        accuracies = [] # точность жадного алгоритма
        for j in range(number_of_test_graphs):
            graph = generate_random_graph(max_ver,i)
            ver = list(graph.keys())

            start = time.time()
            result_test_a1 = find_max_set_a1_cs(ver,graph)
            exact_time = time.time() - start

            start = time.time()
            result_test_a2 = find_max_set_a2_cs(graph)
            greedy_time = time.time() - start

            exact_times.append(exact_time)
            greedy_times.append(greedy_time)
            exact_sizes.append(len(result_test_a1))
            greedy_sizes.append(len(result_test_a2))

            if len(result_test_a1) == len(result_test_a2):
                accuracies.append(100)
            else:
                accuracies.append(0)
        results["плотность"].append(i)
        results["время точного"].append(np.mean(exact_times))
        results["время жадного"].append(np.mean(greedy_times))
        results["размер точного"].append(np.mean(exact_sizes))
        results["размер жадного"].append(np.mean(greedy_sizes))
        results["точность"].append(np.mean(accuracies))
        results["отношение скоростей"].append(np.mean(exact_times)/np.mean(greedy_times))
    return results
#множественные тесты для графов от step до n с шагом step и полином 3 степени
def tests(max_ver,number_of_test_graphs,step):
    tests_results = []
    for i in range(step,max_ver+1,step):
        k = test(i,number_of_test_graphs)
        tests_results.append(k)
    return tests_results
# полином 3 степени (для функции test )
def test_polinom(test_results):
    x_fit = np.linspace(min(test_results["плотность"]), max(test_results["плотность"]), 100)
    A = np.vander(test_results["плотность"], 4)
    coefficients, residuals, rank, s = linalg.lstsq(A, test_results["точность"])
    y_fit = coefficients[0] * x_fit ** 3 + coefficients[1] * x_fit ** 2 + coefficients[2] * x_fit + coefficients[3]
    y_fit = np.clip(y_fit, 0, 100)
    return x_fit,y_fit

def tests_polinom(tests_results):
    x_fit = []
    y_fit = []
    for i in tests_results:
        pol = test_polinom(i)
        x_fit.append(pol[0])
        y_fit.append(pol[1])
    return x_fit, y_fit
# визуализация тестов
def test_visual(results,x_fit,y_fit):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    # Метрики точности полинома
    y_poly_at_density = np.interp(results['плотность'], x_fit, y_fit)
    s = np.sum((results['точность'] - np.mean(results['точность'])) ** 2)
    if s == 0:
        r2 = 1
    else:
        r2 = 1 - np.sum((results['точность'] - y_poly_at_density) ** 2) / s  # коэфицент детерминации

    # График 1: Время выполнения
    ax1.plot(results['плотность'], results['время точного'], 'ro-', label='Точный алгоритм', linewidth=2)
    ax1.plot(results['плотность'], results['время жадного'], 'bo-', label='Жадный алгоритм', linewidth=2)
    ax1.set_xlabel('Плотность графа')
    ax1.set_ylabel('Время выполнения (сек)')
    ax1.set_title('Зависимость времени выполнения от плотности графа')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # График 2: Точность жадного алгоритма
    ax2.plot(results['плотность'], results['точность'],  'D-', color='green', linewidth=2.5,markersize=6, label='Точность')
    ax2.plot(x_fit, y_fit, 'r-', linewidth=2, label=f'Полином 3 степени\nR² = {r2:.4f}')
    ax2.set_xlabel('Плотность графа')
    ax2.set_ylabel('Средняя точность (%)')
    ax2.set_title('Средняя точность жадного алгоритма')
    ax2.set_ylim(0, 105)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # График 3: Размер множества
    ax3.plot(results['плотность'], results['размер точного'], 'ro-', label='Точный алгоритм', linewidth=2)
    ax3.plot(results['плотность'], results['размер жадного'], 'bo-', label='Жадный алгоритм', linewidth=2)
    ax3.set_xlabel('Плотность графа')
    ax3.set_ylabel('Размер множества')
    ax3.set_title('Зависимость размера максимального независимого множества от плотности графа')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # График 4: Ускорение
    ax4.plot(results['плотность'], results['отношение скоростей'], 'purple', linewidth=2)
    ax4.set_xlabel('Плотность графа')
    ax4.set_ylabel('Отношение времени (точный/жадный)')
    ax4.set_title('Во сколько раз точный алгоритм медленнее')
    ax4.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def tests_visual(results,pol_x,pol_y,step):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    plt.subplots_adjust(bottom=0.15)
    ax_slider = plt.axes([0.25, 0.02, 0.5, 0.03])
    slider = Slider(ax_slider, 'Количество вершин', step, len(results[0])*step, valinit=step, valstep=step)
    def update(val):
        for ax in [ax1, ax2, ax3, ax4]:
            ax.clear()
            ax.grid(True, alpha=0.3)
        n_ver = int(slider.val)//step - 1

        # Данные для текущего количества вершин
        density = results[n_ver]['плотность']
        exact_time = results[n_ver]['время точного']
        greedy_time = results[n_ver]['время жадного']
        accuracy = results[n_ver]['точность']
        exact_size = results[n_ver]['размер точного']
        greedy_size = results[n_ver]['размер жадного']
        speed_ratio = results[n_ver]['отношение скоростей']
        x_fit = pol_x[n_ver]
        y_fit = pol_y[n_ver]

        # Метрики точности полинома
        y_poly_at_density = np.interp(density, x_fit, y_fit)
        s = np.sum((accuracy - np.mean(accuracy)) ** 2)
        if s == 0:
            r2 = 1
        else:
            r2 = 1 - np.sum((accuracy - y_poly_at_density) ** 2) / s  # коэфицент детерминации

        # График 1: Время выполнения
        ax1.plot(density, exact_time, 'o-', color='red', linewidth=2.5,markersize=6, label='Точный алгоритм')
        ax1.plot(density, greedy_time, 's-', color='blue', linewidth=2.5,markersize=6, label='Жадный алгоритм')
        ax1.set_xlabel('Плотность графа', fontsize=12)
        ax1.set_ylabel('Время выполнения (сек)', fontsize=12)
        ax1.set_title('Зависимость времени выполнения от плотности графа', fontsize=14, fontweight='bold')
        ax1.legend()

        # График 2: Точность жадного алгоритма с полиномом
        ax2.plot(density, accuracy, 'D-', color='green', linewidth=2.5,markersize=6, label='Точность')
        ax2.plot(x_fit, y_fit, 'r-', linewidth=2, label=f'Полином 3 степени\nR² = {r2:.4f}')
        ax2.set_xlabel('Плотность графа', fontsize=12)
        ax2.set_ylabel('Точность (%)', fontsize=12)
        ax2.set_title('Средняя точность жадного алгоритма ',fontsize=14, fontweight='bold')
        ax2.set_ylim(0, 105)
        ax2.legend()

        # График 3: Размер множества
        ax3.plot(density, exact_size, 'o-', color='red', linewidth=2.5,markersize=6, label='Точный алгоритм')
        ax3.plot(density, greedy_size, 's-', color='blue', linewidth=2.5,markersize=6, label='Жадный алгоритм')
        ax3.set_xlabel('Плотность графа', fontsize=12)
        ax3.set_ylabel('Размер множества', fontsize=12)
        ax3.set_title('Зависимость размера максимального независимого множества от плотности графа',fontsize=14, fontweight='bold')
        ax3.legend()

        # График 4: Ускорение
        ax4.plot(density, speed_ratio, '^-', color='purple', linewidth=2.5,markersize=6)
        ax4.set_xlabel('Плотность графа', fontsize=12)
        ax4.set_ylabel('Отношение времени (точный/жадный)', fontsize=12)
        ax4.set_title('Во сколько раз точный алгоритм медленнее',fontsize=14, fontweight='bold')

        plt.draw()
    slider.on_changed(update)
    update(1)
    plt.show()

def visual_func_family(results,x_fit,y_fit,step):
    n_values = [f"n={i}" for i in range(step, len(results) * step + 1, step)]
    colors = plt.cm.viridis(np.linspace(0, 1, len(results)))

    # 1. Время выполнения точного алгоритма
    plt.figure(figsize=(12, 8))
    for i in range(len(results)):
        plt.plot(results[i]['плотность'], results[i]["время точного"],color=colors[i], label=n_values[i], linewidth=2)
    plt.xlabel('Плотность графа')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Среднее времени точного алгоритма для разных n')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # 2. Размер множества - точный алгоритм
    plt.figure(figsize=(12, 8))
    for i in range(len(results)):
        plt.plot(results[i]['плотность'], results[i]["размер точного"],color=colors[i], label=n_values[i], linewidth=2)
    plt.xlabel('Плотность графа')
    plt.ylabel('Размер множества')
    plt.title('Изменение среднего размера множества (точный алгоритм) для разных n')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0,1)
    plt.show()

    # 3. Размер множества - жадный алгоритм
    plt.figure(figsize=(12, 8))
    for i in range(len(results)):
        plt.plot(results[i]['плотность'], results[i]["размер жадного"],color=colors[i], label=n_values[i], linewidth=2)
    plt.xlabel('Плотность графа')
    plt.ylabel('Размер независимого множества')
    plt.title('Изменение среднего размера множества (жадный алгоритм) для разных n')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # 4. Сравнение размеров (точный vs жадный)
    plt.figure(figsize=(12, 8))
    for i in range(len(results)):
        plt.plot(results[i]['плотность'], results[i]["размер точного"],color=colors[i], linestyle='-', label=f'{n_values[i]} точный')
        plt.plot(results[i]['плотность'], results[i]["размер жадного"],color=colors[i], linestyle='--', label=f'{n_values[i]} жадный')
    plt.xlabel('Плотность графа')
    plt.ylabel('Размер множества')
    plt.title('Сравнение средних размеров множеств для разных n')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    # 4. Сравнение размеров
    plt.figure(figsize=(12, 8))
    for i in range(len(results)):
        plt.plot(results[i]["плотность"], results[i]["точность"], 'D-', color=colors[i],label=f'Полином {n_values[i]}', linewidth=2)
    plt.xlabel('Плотность графа')
    plt.ylabel('точность')
    plt.title('точность жадного алгоритма')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # 5. Аппроксимирующие полиномы
    plt.figure(figsize=(12, 8))
    for i in range(len(results)):
        y_poly_at_density = np.interp(results[i]['плотность'], x_fit[i], y_fit[i])
        s = np.sum((results[i]['точность'] - np.mean(results[i]['точность'])) ** 2)
        if s == 0:
            r2 = 1
        else:
            r2 = 1 - np.sum((results[i]["точность"] - y_poly_at_density) ** 2) / s # коэфицент детерминации
        plt.plot(x_fit[i], y_fit[i], color=colors[i],label=f'Полином {n_values[i]}\nКоэффициент детерминаци R² = {r2:.2f}', linewidth=2)
    plt.xlabel('Плотность графа')
    plt.ylabel('Точность (%)')
    plt.title('полиномы 3 степени для раззных n')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


