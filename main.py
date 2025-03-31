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


def cover_cities(adjacency, cost):
    cities = list(range(1, 16))
    best_solution = None
    best_cost = float('inf')

    def is_covered(covers):
        return all(covers[i] for i in cities)

    def backtrack(idx, centers, covers, current_cost):
        nonlocal best_solution, best_cost
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

    return best_solution, best_cost

solution, total_cost = cover_cities(adjacency_cities, cost)
print("Centros instalados en:", [c for c, v in solution.items() if v])
print("Costo total:", total_cost)
