#include <iostream>
#include <windows.h>
#include <vector>
#include <algorithm>

using namespace std;

struct Square {
    int x, y, w;
};

int n;
int min_count = 5;
bool found = false;
vector<Square> best_res;
int table[45][45];

void solve(int count, vector<Square>& squares, int min_y, int empty) {
    if (count >= min_count) return;

    int start_y = -1, start_x = -1;
    for (int r = min_y; r < n; ++r) {
        for (int c = 0; c < n; ++c) {
            if (table[r][c] == 0) {
                start_y = r;
                start_x = c;
                break;
            }
        }
        if (start_y != -1) break;
    }

    if (start_y == -1) {
        cout << "Квадрат заполнен\n";
        if (count <= min_count) {
            min_count = count;
            found = true;
            best_res = squares;
            cout << "Решение найдено за " << min_count << " квадратов, у нас новый min_count (или подтверждённый)\n";
        }
        return;
    }
    cout << "Наша первая пустая клетка - (" << start_x << "; " << start_y << ")\n";
    int max_w = 0;
    int limit = min(n - start_y, n - start_x);
    
    for (int w = 1; w <= limit; ++w) {
        bool possible = true;
        for (int i = 0; i < w; ++i) {
            if (table[start_y + i][start_x + w - 1] == 1 || 
                table[start_y + w - 1][start_x + i] == 1) {
                possible = false;
                break;
            }
        }
        if (!possible) break;
        max_w = w;
    }

    cout << "В эту клетку мы можем поместить квадрат стороной до " << max_w << ". Начинаем перебор\n";

    for (int w = max_w; w >= 1; --w) {
        if ((n - start_y) * (n - start_y) * (min_count - count - 1) < empty - w * w) {
            cout << "Если мы поместим квадрат со стороной " << w << " в клетку (" << start_x << "; " << start_y << "), то никак не успеем всё заполнить, поэтому заканчиваем рассмотрение.\n";
            return;
        }

        for (int r = start_y; r < start_y + w; ++r)
            for (int c = start_x; c < start_x + w; ++c)
                table[r][c] = 1;
        cout << "С добавлением квадрата со стороной " << w << " в клетку (" << start_x << "; " << start_y << ") наш стол выглядит так:\n";
        for(int i = 0; i < n; i++){
            for(int j = 0; j < n; j++){
                cout << table[i][j];
            }
            cout << "\n";
        }
        squares.push_back({start_x + 1, start_y + 1, w});

        solve(count + 1, squares, start_y, empty - w * w);
        
        squares.pop_back();
        for (int r = start_y; r < start_y + w; ++r)
            for (int c = start_x; c < start_x + w; ++c)
                table[r][c] = 0;
        cout << "Откатываемся на шаг назад, удаляем квадрат, теперь наш стол выглядит так:\n";
        for(int i = 0; i < n; i++){
            for(int j = 0; j < n; j++){
                cout << table[i][j];
            }
            cout << "\n";
        }
        if (found && min_count <= count + 1) return;
    }
}

int main() {
    SetConsoleOutputCP(65001);
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    if (!(cin >> n)) return 0;

    for(int i = 0; i < 45; i++)
        for(int j = 0; j < 45; j++) table[i][j] = 0;

    int scale = 1;
    int original_n = n;
    int new_n = 0;

    if (n % 2 != 0) {
        for (int d = 2; d <= n / 2; ++d) {
            if (n % d == 0) {
                new_n = d;
                scale = n / d;
                break;
            }
        }
        if (new_n != 0){ 
            n = new_n;
            cout << "Число составное, ответ для него такой же, как и для " << n << ", но с учётом масштаба\n";
            cout << "Поэтому найдём решения для n = " << n << "\n";
        }
        cout << "Как и для всех простых чисел располагаем наши первые 3 кадрата гарантированно\n";
        int k = (n + 1) / 2;
        for (int r = 0; r < k; ++r)
            for (int c = 0; c < k; ++c) table[r][c] = 1;
        for (int r = 0; r < k - 1; ++r)
            for (int c = k; c < n; ++c) table[r][c] = 1;
        for (int r = k; r < n; ++r)
            for (int c = 0; c < k - 1; ++c) table[r][c] = 1;
        cout << "Располагаем квадрат со стороной " << k << " на позицию (1, 1)\n";
        cout << "Располагаем квадрат со стороной " << k - 1 << " на позицию (" << k + 1 << ", 1)\n";
        cout << "Располагаем квадрат со стороной " << k - 1<< " на позицию (1, " << k + 1 << ")\n";
        vector<Square> initial_squares = {
            {1, 1, k},
            {k + 1, 1, k - 1},
            {1, k + 1, k - 1}
        };

        int empty_space = n * n - (k * k + 2 * (k - 1) * (k - 1));
        cout << "Начинаем бектрекинг с min_count = " << min_count << "\n";
        while (!found) {
            solve(3, initial_squares, 0, empty_space);
            if (!found){
                cout << "Решение за " << min_count << " шагов не найдено, теперь ищем решение за " << ++min_count << " шагов\n";
            }
        }

        if (new_n != 0) {
            for (int i = 0; i < (int)best_res.size(); ++i) {
                best_res[i].x = (best_res[i].x - 1) * scale + 1;
                best_res[i].y = (best_res[i].y - 1) * scale + 1;
                best_res[i].w *= scale;
            }
        }
    } else {
        cout << "Число чётное, этот случай тривиален, просто заполняем его четырьмя квадратами со стороной n / 2\n";
        int half = n / 2;
        best_res = {
            {1, 1, half},
            {1, half + 1, half},
            {half + 1, 1, half},
            {half + 1, half + 1, half}
        };
        min_count = 4;
    }

    cout << best_res.size() << "\n";
    for (int i = 0; i < (int)best_res.size(); ++i) {
        cout << best_res[i].x << " " << best_res[i].y << " " << best_res[i].w << "\n";
    }

    return 0;
}