log = open("log.txt", "w", encoding="utf-8")
log.write("--- Начало работы алгоритма КМП ---\n")

p = input()
log.write(f"Считан образец (p): '{p}'\n\n")

n = len(p)
pref = n * [0]

log.write("--- Построение префикс-функции ---\n")
log.write(f"Инициализация массива pref нулями. Длина массива: {n}\n")

for i in range(1, n):
    log.write(f"\nИтерация i={i}, текущий символ p[{i}] = '{p[i]}'\n")
    j = pref[i - 1]
    log.write(f"  Начальное значение j (из pref[{i - 1}]): {j}\n")

    while p[i] != p[j] and j > 0:
        log.write(f"  Несовпадение: p[{i}] ('{p[i]}') != p[{j}] ('{p[j]}')\n")
        log.write(f"  Откат j к pref[{j - 1}]\n")
        j = pref[j - 1]
        log.write(f"  Новое значение j = {j}\n")

    if p[i] != p[j]:
        log.write(f"  Совпадений нет, j остается равным {j}\n")
        pref[i] = 0
        log.write(f"  -> Записываем pref[{i}] = 0\n")
    else:
        log.write(f"  Совпадение: p[{i}] == p[{j}] ('{p[i]}'). Увеличиваем j.\n")
        pref[i] = j + 1
        log.write(f"  -> Записываем pref[{i}] = {j + 1}\n")

    log.write(f"  Текущий массив pref: [{', '.join(map(str, pref))}]\n")

t = input()
log.write(f"\nСчитан текст (t): '{t}'\n")

log.write("\n--- Поиск вхождений образца в тексте ---\n")
j = 0
log.write("Начальная длина совпадения j = 0\n")
answ = []

for i in range(len(t)):
    log.write(f"\nИтерация по тексту i={i}, текущий символ t[{i}] = '{t[i]}'\n")
    log.write(f"  Текущая длина совпадения j = {j}\n")

    while t[i] != p[j] and j > 0:
        log.write(f"  Несовпадение: t[{i}] ('{t[i]}') != p[{j}] ('{p[j]}')\n")
        log.write(f"  Откат j к pref[{j - 1}]\n")
        j = pref[j - 1]
        log.write(f"  Новое значение j = {j}\n")

    if t[i] == p[j]:
        log.write(f"  Совпадение: t[{i}] == p[{j}] ('{t[i]}'). Увеличиваем j.\n")
        j += 1
        if j == n:
            log.write(f"  !!! Найдено полное вхождение образца (j == {n}). Индекс начала: {i - n + 1}\n")
            answ.append(str(i - n + 1))
            log.write("  Откат j для поиска следующих вхождений к pref[-1]\n")
            j = pref[-1]
            log.write(f"  Новое значение j = {j}\n")
    else:
        log.write(f"  Совпадений нет, j остается равным {j}\n")

log.write("\n--- Завершение алгоритма ---\n")
log.write(f"Всего найдено вхождений: {len(answ)}\n")
log.close()

if answ:
    print(','.join(answ))
else:
    print(-1)