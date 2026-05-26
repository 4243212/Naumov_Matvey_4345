import sys

input_data = sys.stdin.read().split()

log = open("log.txt", "w", encoding="utf-8")
log.write("--- Начало работы 2-приближенного алгоритма (АДО МОД) для TSP ---\n")

start_vertex = int(input_data[0])
log.write(f"Стартовая вершина для обхода: {start_vertex}\n")

matrix_elements = input_data[1:]
n = int(len(matrix_elements) ** 0.5)
log.write(f"Количество вершин в графе (n): {n}\n")

adj_matrix = []
idx = 0
for i in range(n):
    row = []
    for j in range(n):
        row.append(float(matrix_elements[idx]))
        idx += 1
    adj_matrix.append(row)

log.write("\nСчитанная матрица весов графа:\n")
for i in range(n):
    log.write(f"  Вершина {i}: {adj_matrix[i]}\n")

log.write("\n--- Построение Минимального Остовного Дерева (Алгоритм Прима) ---\n")
mst_adj = {i: [] for i in range(n)}
visited_mst = [False] * n

visited_mst[start_vertex] = True
log.write(f"Инициализация MST со стартовой вершины: {start_vertex}\n")

for step in range(n - 1):
    log.write(f"\n[Шаг {step + 1}] Поиск минимального ребра для расширения MST:\n")
    min_weight = float('inf')
    u_min, v_min = -1, -1

    for u in range(n):
        if visited_mst[u]:
            for v in range(n):
                if not visited_mst[v] and adj_matrix[u][v] != -1:
                    if adj_matrix[u][v] < min_weight:
                        min_weight = adj_matrix[u][v]
                        u_min, v_min = u, v

    if u_min != -1 and v_min != -1:
        mst_adj[u_min].append(v_min)
        mst_adj[v_min].append(u_min)
        visited_mst[v_min] = True
        log.write(f"  -> Добавлено ребро ({u_min} <-> {v_min}) с весом {min_weight}\n")
        log.write(f"  -> Вершина {v_min} добавлена в множество посещенных в MST\n")
    else:
        log.write("  [!] Ошибка: Не удалось найти связное ребро. Граф несвязный.\n")

log.write("\n--- Сортировка списков смежности MST по весам ребер ---\n")
for u in range(n):
    log.write(f"  Вершина {u} до сортировки: {mst_adj[u]}\n")
    mst_adj[u].sort(key=lambda v: adj_matrix[u][v])
    log.write(f"  Вершина {u} после сортировки (приоритет минимальным ребрам): {mst_adj[u]}\n")

log.write("\n--- Обход дерева в глубину (DFS) для построения маршрута ---\n")
path = []
visited_dfs = [False] * n

def dfs(node, level=1):
    indent = "  " * level
    log.write(f"{indent}Вход в вершину {node}\n")

    visited_dfs[node] = True
    path.append(node)
    log.write(f"{indent}  -> Вершина {node} добавлена в итоговый путь (Shortcuts в действии)\n")

    for neighbor in mst_adj[node]:
        if not visited_dfs[neighbor]:
            log.write(f"{indent}  Идем в непосещенного соседа {neighbor}\n")
            dfs(neighbor, level + 1)
        else:
            log.write(f"{indent}  Сосед {neighbor} уже посещен, пропускаем его (срезаем угол)\n")

    log.write(f"{indent}Выход из вершины {node}\n")

dfs(start_vertex)

log.write(f"\nЗамыкание маршрута: возврат в стартовую вершину {start_vertex}\n")
path.append(start_vertex)

log.write("\n--- Подсчет итоговой длины построенного пути ---\n")
total_length = 0.0
for i in range(len(path) - 1):
    u = path[i]
    v = path[i + 1]
    step_cost = adj_matrix[u][v]
    total_length += step_cost
    log.write(f"  Переход [{i}]: {u} -> {v} | Стоимость: {step_cost} | Текущая сумма: {total_length}\n")

log.write("\n--- Алгоритм завершен ---\n")
log.write(f"Итоговый путь: {path}\n")
log.write(f"Полная длина пути: {total_length:.2f}\n")
log.close()

print(f"{total_length:.2f}")
print(*(path))