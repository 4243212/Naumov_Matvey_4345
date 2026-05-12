from collections import deque


class Node:
    def __init__(self, letter='', parent=None):
        self.letter = letter
        self.parent = parent
        self.childs = {}

        self.link = None
        self.term_link = None

        self.out = []


log = open("log.txt", "w", encoding="utf-8")
log.write("--- Начало работы алгоритма Ахо-Корасика с джокерами ---\n")

text = input().strip()
pattern = input().strip()

wild = input().strip()
bad = input().strip()

log.write(f"Считан текст: '{text}'\n")
log.write(f"Считан шаблон: '{pattern}'\n")
log.write(f"Джокер: '{wild}', Запрещенный символ: '{bad}'\n\n")

parts = []

i = 0

log.write("--- Разбиение шаблона на подстроки ---\n")
while i < len(pattern):

    if pattern[i] == wild:
        i += 1
        continue

    start = i
    cur = []

    while i < len(pattern) and pattern[i] != wild:
        cur.append(pattern[i])
        i += 1

    parts.append(("".join(cur), start))
    log.write(f"Извлечена часть: '{''.join(cur)}' со смещением {start}\n")

tree = Node()

log.write("\n--- Построение Бора (Trie) ---\n")
for word, shift in parts:

    log.write(f"Добавление слова '{word}' (смещение {shift}) в Бор\n")
    current = tree

    for ch in word:

        if ch not in current.childs:
            log.write(f"  Создан новый узел для символа '{ch}'\n")
            current.childs[ch] = Node(ch, current)
        else:
            log.write(f"  Переход в существующий узел '{ch}'\n")

        current = current.childs[ch]

    current.out.append((len(word), shift))
    log.write(f"  Узел '{ch}' помечен как конец подстроки. Добавлено в out: длина {len(word)}, смещение {shift}\n")

tree.link = tree

queue = deque()

log.write("\n--- Построение суффиксных и терминальных ссылок (BFS) ---\n")
log.write("Инициализация ссылок для детей корня\n")
for child in tree.childs.values():
    child.link = tree
    queue.append(child)

while queue:

    current = queue.popleft()

    for ch, child in current.childs.items():

        queue.append(child)

        link = current.link

        log.write(f"Поиск суффиксной ссылки для узла '{ch}'\n")

        while link != tree and ch not in link.childs:
            link = link.link

        if ch in link.childs:
            child.link = link.childs[ch]
            log.write(f"  Установлена суффиксная ссылка\n")
        else:
            child.link = tree
            log.write(f"  Суффиксов в дереве нет, ссылка ведет в корень\n")

        if child.link.out:
            child.term_link = child.link
            log.write(f"  Установлена терминальная ссылка\n")
        else:
            child.term_link = child.link.term_link

cnt = [0] * len(text)

current = tree

log.write("\n--- Поиск вхождений подстрок в тексте ---\n")
for i in range(len(text)):

    ch = text[i]
    log.write(f"\nИтерация i={i}, текущий символ текста '{ch}'\n")

    while current != tree and ch not in current.childs:
        log.write(f"  Нет перехода по '{ch}'. Прыжок по суффиксной ссылке.\n")
        current = current.link

    if ch in current.childs:
        current = current.childs[ch]
        log.write(f"  Успешный переход в узел '{ch}'\n")
    else:
        current = tree
        log.write(f"  Сброс указателя в корень дерева\n")

    check = current

    while check:

        for length, shift in check.out:

            start = i - length + 1 - shift
            log.write(f"  Найдено совпадение! Длина: {length}, Смещение: {shift}.\n")
            log.write(f"  Возможная стартовая позиция всего шаблона: {start}\n")

            if 0 <= start and start + len(pattern) <= len(text):
                cnt[start] += 1
                log.write(f"    -> Счетчик совпадений для позиции {start} увеличен до {cnt[start]}\n")

        check = check.term_link

need = len(parts)

log.write(f"\n--- Финальная проверка кандидатов. Нужно совпадений частей: {need} ---\n")
for start in range(len(text) - len(pattern) + 1):

    if cnt[start] != need:
        continue

    log.write(f"\nКандидат на позиции {start} собрал все {need} частей.\n")
    ok = True

    for j in range(len(pattern)):
        if pattern[j] == wild:
            if text[start + j] == bad:
                log.write(
                    f"  Ошибка: Джокер совпал с запрещенным символом '{bad}' на позиции {start + j}. Кандидат отклонен.\n")
                ok = False
                break

    if ok:
        log.write(f"  -> Вхождение шаблона полностью подтверждено! Выводим позицию: {start + 1}\n")
        print(start + 1)

log.write("\n--- Завершение алгоритма ---\n")
log.close()