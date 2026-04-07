def solve():
    costs = list(map(int, input().split()))
    cost_repl, cost_ins, cost_del, cost_individ = costs
    A = input().strip()
    B = input().strip()

    n, m = len(A), len(B)
    dp = []
    for i in range(n + 1):
        dp.append([])
        for j in range(m + 1):
            dp[i].append([0, ''])

    with open("log.txt", "w", encoding="utf-8") as log_file:
        def log(text):
            log_file.write(text + "\n")

        def log_matrix():
            header = "      " + " ".join(f"{ch:>3}" for ch in B)
            log(header)
            for r in range(n + 1):
                row_char = " " if r == 0 else A[r - 1]
                row_vals = " ".join(f"{dp[r][c][0]:>3}" for c in range(m + 1))
                log(f"{row_char} {row_vals}")
            log("")

        log(f"Начало вычисления.\nСтрока A: '{A}'\nСтрока B: '{B}'\n")

        for i in range(1, n + 1):
            dp[i][0] = [dp[i - 1][0][0] + cost_del, 'D']

        for j in range(1, m + 1):
            dp[0][j] = [dp[0][j - 1][0] + cost_ins, 'I']

        log("Матрица после инициализации краев:")
        log_matrix()

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost_delete = dp[i - 1][j][0] + cost_del
                cost_insert = dp[i][j - 1][0] + cost_ins

                if A[i - 1] == B[j - 1]:
                    cost_replace = dp[i - 1][j - 1][0]
                    rep_type = "Совпадение"
                else:
                    cost_replace = dp[i - 1][j - 1][0] + cost_repl
                    rep_type = "Замена"

                if i >= 2:
                    cost_individual = dp[i - 2][j - 1][0] + cost_individ
                    can_4b = True
                else:
                    cost_individual = float('inf')
                    can_4b = False

                mn = min(cost_delete, cost_insert, cost_replace, cost_individual)
                if cost_delete == mn:
                    dp[i][j] = [mn, 'D']
                elif cost_insert == mn:
                    dp[i][j] = [mn, 'I']
                elif cost_replace == mn:
                    if A[i - 1] == B[j - 1]:
                        dp[i][j] = [mn, 'M']
                    else:
                        dp[i][j] = [mn, 'R']
                else:
                    dp[i][j] = [mn, '4']

                log(f"Клетка [{i}][{j}] | A[{i - 1}]='{A[i - 1]}', B[{j - 1}]='{B[j - 1]}'")
                log(f"  1. Удаление: {dp[i - 1][j][0]} + {cost_del} = {cost_delete}")
                log(f"  2. Вставка: {dp[i][j - 1][0]} + {cost_ins} = {cost_insert}")
                log(f"  3. {rep_type}: {dp[i - 1][j - 1][0]} + {0 if rep_type == 'Совпадение' else cost_repl} = {cost_replace}")
                if can_4b:
                    log(f"  4. Операция из индивидуального варианта: {dp[i - 2][j - 1][0]} + {cost_individ} = {cost_individual}")
                log(f"  Результат dp[{i}][{j}] = {dp[i][j][0]}\n")

        log("Финальная матрица:")
        log_matrix()
        log(f"Итоговое расстояние: {dp[n][m][0]}")

    print(dp[n][m][0])
    i = n
    j = m
    s = ''
    while i != 0 or j != 0:
        s += dp[i][j][1]
        if s[-1] == 'M' or s[-1] == 'R':
            i -= 1
            j -= 1
        elif s[-1] == 'D':
            i -= 1
        elif s[-1] == 'I':
            j -= 1
        else:
            i -= 2
            j -= 1

    s = s[::-1]
    print(s)


if __name__ == "__main__":
    solve()