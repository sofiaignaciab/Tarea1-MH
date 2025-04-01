import psutil
import time

cost = {
    1: 60, 2: 30, 3: 60, 4: 70, 5: 130,
    6: 60, 7: 70, 8: 60, 9: 80, 10: 70,
    11: 50, 12: 90, 13: 30, 14: 30, 15: 100
}

adjacency_cities = {
    1: [1, 4, 3, 13],
    2: [2, 4, 1, 12, 15],
    3: [3, 4, 13, 1, 5, 6],
    4: [4, 1, 2, 3, 5, 12],
    5: [5, 4, 8, 6, 3, 12, 7, 9],
    6: [6, 5, 9, 3],
    7: [7, 8, 5,12,15,14,11,10],
    8: [8, 5, 7, 9, 10],
    9: [9, 8, 10, 11, 6,5],
    10: [10, 8, 9, 11, 7],
    11: [11, 9, 10, 7, 14],
    12: [12, 5, 4, 2, 15, 7],
    13: [13, 1, 3],
    14: [14, 11, 7, 15],
    15: [15, 14, 2,12, 7]
}


def cover_cities( adjacency, cost):
    cities = list(range(1, 16))
    best_solution = None
    best_cost = float('inf')
    node_counter = 0

    def is_covered(covers):
        return all(covers[i] for i in cities)

    def backtrack(idx, centers, covers, current_cost):
        nonlocal best_solution, best_cost, node_counter
        node_counter += 1

        if idx > 15:
            if is_covered(covers) and current_cost < best_cost:
                best_solution = centers.copy()
                best_cost = current_cost
            return

        centers[idx] = True
        new_covers = covers.copy()
        for c in adjacency[idx]:
            new_covers[c] = True
        backtrack(idx + 1, centers, new_covers, current_cost + cost[idx])

        centers[idx] = False
        backtrack(idx + 1, centers, covers.copy(), current_cost)

    centers = {i: False for i in cities}
    covers = {i: False for i in cities}
    backtrack(1, centers, covers, 0)

    return best_solution, best_cost, node_counter


# Obtener el proceso actual
process = psutil.Process()

# Obtener el tiempo de CPU antes de ejecutar la función
cpu_times_before = process.cpu_times()

# Obtener el uso de CPU y memoria antes de ejecutar la función
cpu_before = psutil.cpu_percent(interval=0.1)
memory_process_before = process.memory_info().rss  # En bytes

# Ejecutar la función cover_cities
solution, total_cost, node_count = cover_cities(adjacency_cities, cost)

# Medir el tiempo de ejecución
end_time = time.perf_counter()

# Obtener el tiempo de CPU después de ejecutar la función
cpu_times_after = process.cpu_times()

# Obtener el uso de CPU y memoria después de ejecutar la función
cpu_after = psutil.cpu_percent(interval=0.1)  # Medir uso de CPU después
memory_process_after = process.memory_info().rss  # En bytes

# Calcular la memoria usada por el proceso
memory_used_by_process = memory_process_after - memory_process_before  # En bytes

# Calcular el tiempo de CPU utilizado por el proceso
cpu_time_used = cpu_times_after.user - cpu_times_before.user  # Tiempo de CPU en modo usuario

# Mostrar los resultados
print("Centros instalados en:", [c for c, v in solution.items() if v])
print("Costo total:", total_cost)
print(f"Uso de CPU antes: {cpu_before}%")
print(f"Uso de CPU después: {cpu_after}%")
print(f"Tiempo de CPU usado por el proceso: {cpu_time_used:.4f} segundos")
print(f"Memoria usada por el proceso (antes): {memory_process_before / (1024 ** 2):.2f} MB")
print(f"Memoria usada por el proceso (después): {memory_process_after / (1024 ** 2):.2f} MB")
print(f"Memoria extra usada por el proceso: {memory_used_by_process / (1024 ** 2):.2f} MB")
print(f"Número de nodos creados: {node_count}")