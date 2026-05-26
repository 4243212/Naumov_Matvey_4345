import sys


def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    log = open("log.txt", "w", encoding="utf-8")
    log.write("--- Начало работы алгоритма ветвей и границ для TSP ---\n")

    n = int(input_data[0])
    log.write(f"Размерность матрицы (количество городов): {n}\n")

    matrix = []
    idx = 1

    for i in range(n):
        row = []
        for j in range(n):
            row.append(float(input_data[idx]))
            idx += 1
        matrix.append(row)

    log.write("\nСчитанная матрица смежности:\n")
    for i in range(n):
        log.write(f"  Город {i}: {matrix[i]}\n")

    log.write("\n--- Расчет минимальных исходящих рёбер (min_out) ---\n")
    min_out = [float('inf')] * n
    for i in range(n):
        min_val = float('inf')
        for j in range(n):
            if i != j and matrix[i][j] >= 0 and matrix[i][j] < min_val:
                min_val = matrix[i][j]
        min_out[i] = min_val
        log.write(f"  Для города {i} минимальное ребро: {min_val}\n")

    best_cost = float('inf')
    best_path = [0] * n

    current_path = [0] * n
    current_path[0] = 0

    visited = [False] * n
    visited[0] = True

    log.write("\n--- Запуск поиска в глубину (DFS) с оценкой границ ---\n")

    def dfs(curr_node, current_cost, level):
        nonlocal best_cost, best_path

        indent = "  " * level

        log.write(f"{indent}Текущий город: {curr_node}, Уровень: {level}, Текущая стоимость: {current_cost}\n")
        log.write(f"{indent}Текущий маршрут: {current_path[:level]}\n")

        if level == n:
            log.write(
                f"{indent}[База рекурсии] Посещены все {n} городов. Проверка возврата в город 0 из города {curr_node}...\n")
            if matrix[curr_node][0] >= 0:
                total_cost = current_cost + matrix[curr_node][0]
                log.write(f"{indent}  -> Успешный возврат. Полная стоимость замкнутого пути: {total_cost}\n")
                if total_cost < best_cost:
                    log.write(
                        f"{indent}  [!!!] Обновление рекорда! Предыдущая лучшая стоимость: {best_cost} -> Новая лучшая стоимость: {total_cost}\n")
                    best_cost = total_cost
                    best_path = current_path[:]
                else:
                    log.write(f"{indent}  -> Маршрут не эффективнее лучшего известного ({best_cost}). Пропускаем.\n")
            else:
                log.write(f"{indent}  -> Ошибка: Ребро возврата из {curr_node} в 0 отсутствует (значение -1).\n")
            return

        log.write(
            f"{indent}[Подсчет нижней границы] Базовая стоимость: {current_cost} + min_out текущего узла ({min_out[curr_node]})\n")
        bound = current_cost + min_out[curr_node]
        for i in range(n):
            if not visited[i]:
                bound += min_out[i]
                log.write(f"{indent}  Добавлен min_out непосещенного города {i}: +{min_out[i]}\n")

        log.write(f"{indent}  -> Итоговая нижняя граница (bound) для ветви: {bound} (Текущий рекорд: {best_cost})\n")

        if bound >= best_cost:
            log.write(
                f"{indent}[X] ОТСЕЧЕНИЕ ВЕТВИ: Нижняя граница {bound} >= лучшей стоимости {best_cost}. Поиск в этом направлении прекращен.\n")
            return

        log.write(f"{indent}[Цикл ветвления] Перебор возможных переходов из города {curr_node}:\n")
        for i in range(n):
            if not visited[i]:
                if matrix[curr_node][i] >= 0:
                    log.write(
                        f"{indent}  -> Город {i} свободен. Переход по ребру со стоимостью {matrix[curr_node][i]}\n")
                    visited[i] = True
                    current_path[level] = i

                    dfs(i, current_cost + matrix[curr_node][i], level + 1)

                    visited[i] = False
                    log.write(
                        f"{indent}[Шаг назад / Backtracking] Возврат из ветки города {i}. Восстановление состояния для города {curr_node}.\n")
                else:
                    log.write(f"{indent}  -> Город {i} свободен, но путь в него невозможен (нет ребра).\n")
            else:
                log.write(f"{indent}  -> Город {i} пропущен (уже посещен).\n")

    dfs(0, 0.0, 1)

    log.write("\n--- Алгоритм завершен ---\n")
    log.write(f"Лучший найденный путь: {best_path}\n")
    log.write(f"Минимальная стоимость: {best_cost}\n")
    log.close()

    print(*(best_path))
    print(float(best_cost))


if __name__ == "__main__":
    solve()