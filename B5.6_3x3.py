player_1 = "Игрок 1"
player_2 = "Игрок 2"
draw = "Ничья"
n = 3  # длинна поля (игра может проходить на поле любого размера)


def game_reset():
    """Спрашивает, начать ли новый раунд """
    ask_if_continue = None
    while True:
        print('Хотите начать новую игру? (Y/N):', end='')
        ask_if_continue = input()
        if ask_if_continue == "Y":
            return ask_if_continue
        elif ask_if_continue == "N":
            return ask_if_continue


#   def grid_size_input():  # включить для возможности задавать размер поля (требуется включить функцию перед основным
#       # циклом и внутри цикла)
#       """Запрашивает размер поля"""
#       while True:
#           print("Введите длину поля (от 2 до 20: ")
#           length = input()
#           if length.isdigit() == 1:
#               length = int(length)
#           else:
#               continue
#           if 2 <= length <= 20:
#               return length


def field_gen(len_gen):
    """Создаёт список в виде матрицы, в которую будут записываться ходы """
    game_gen = []
    for c in range(len_gen):
        game_gen.append([])
        for r in range(len_gen):
            game_gen[c].append(0)
    return game_gen


def grid_print(len_print):
    """Выводит поле в виде строк"""
    print('   ', end='')
    for m in range(1, len_print + 1):  # нумерация колонок
        if m >= 10:  # если поле больше 10
            print(f' {m} ', end='')
        if m < 10:
            print(f'  {m} ', end='')
    print('\n', end='')

    lines = '--- ' * len_print
    print('    ' + lines)
    for i in range(0, len_print):

        print('%2d ' % (i + 1), end='')  # нумерация строк
        for elem in range(0, len_print):  #
            if game[i][elem] == 0:
                print(f'|   ', end='') if elem < len_print - 1 else print(f'|   |', end='')
            if game[i][elem] == 1:
                print(f'| X ', end='') if elem < len_print - 1 else print(f'| X |', end='')
            if game[i][elem] == 2:
                print(f'| O ', end='') if elem < len_print - 1 else print(f'| O |', end='')

        print('\n' + '    ' + lines)


def input_check(player):
    """Запрашивает ход и записывает его в матрицу. 0 - пусто, 1 - игрок 1, 2 - игрок 2"""
    while True:
        p_input = input(f'{player}, введите номер столбца и строки (X пробел Y): ')
        p_input = p_input.split(' ')
        if len(p_input) != 2 or p_input[0].isdigit() == 0 or p_input[1].isdigit() == 0:
            continue

        column, row = p_input
        column, row = int(column), int(row)
        if (row not in range(1, n + 1)) or (column not in range(1, n + 1)):
            print('Клетка вне поля!')
            continue
        if game[row - 1][column - 1] != 0:
            print('Клетка занята!')
            continue
        if player == player_1:
            game[row - 1][column - 1] = 1
        else:
            game[row - 1][column - 1] = 2
        break


def win_count(fn):
    """Сохраняет результаты"""
    player_1_wins, player_2_wins, draws = 0, 0, 0

    def wrapper(*args):
        """Выводит имя победителя/ничью и статистику"""
        nonlocal player_1_wins, player_2_wins, draws
        winner_wrapper = fn(*args)
        if winner_wrapper == player_1:
            player_1_wins += 1
            print('Игрок 1 победил!')

        if winner_wrapper == player_2:
            player_2_wins += 1
            print('Игрок 2 победил!')

        if winner_wrapper == draw:
            draws += 1
            print('Ничья!')
        if winner_wrapper is not None:
            print('\n''---------счёт---------')
            print(f'<Игрок 1> победы: {player_1_wins}')
            print(f'<Игрок 2> победы: {player_2_wins}')
            print(f'Ничьи: {draws}')
        return winner_wrapper

    return wrapper


def diagonal_1_check(*args):
    """Проверяет диагональ 1 на выполнение условия победы"""
    for i in range(n - 1):
        if game[i][i] == 0 or game[i][i] != game[i + 1][i + 1]:  # проверка диагонали на равенство значений
            return None
    if game[0][0] == 1:
        return player_1
    if game[0][0] == 2:
        return player_2


def diagonal_2_check(*args):
    """Проверяет диагональ 2 на выполнение условия победы"""
    for i in range(n - 1):
        if game[i][n - 1 - i] == 0 or game[i][n - 1 - i] != game[i + 1][n - 2 - i]:
            return None
    if game[0][n - 1] == 1:
        return player_1
    if game[0][n - 1] == 2:
        return player_2


def lines_check(player):
    """Проверяет линии на выполнение условия победы"""
    vertical_list = []  # список для значений столбца

    for i in range(n):
        for z in range(n):
            vertical_list.append(game[z][i])
        vertical_set = set(vertical_list)
        if player == player_1:
            if ((len(set(game[i])) == 1 and game[i][
                0] == 1) or  # проверка длинны множества значений строки и первого элемента строки
                    (len(vertical_set) == 1 and game[0][
                        i] == 1)):  # проверка длинны множества значений столбца и первого элемента столбца
                return player_1
        if player == player_2:
            if ((len(set(game[i])) == 1 and game[i][0] == 2) or
                    (len(vertical_set) == 1 and game[0][i] == 2)):
                return player_2

        vertical_list.clear()  # очищает список и множество перед проверкой следующего столбца
        vertical_set.clear()
    return None


def draw_check(*args):
    """Проверяет результаты на ничью"""
    for i in range(n):
        if 0 in game[i]:
            return None
    return draw


@win_count
def win_check(player):
    """Выполняет все проверки"""
    winner_check = None
    fn_list = [lines_check, diagonal_1_check, diagonal_2_check, draw_check]
    for i in range(len(fn_list)):
        if winner_check is None:
            winner_check = fn_list[i](player)
    return winner_check


# начало
#  n = grid_size_input()  # ввод размера поля (включить для возможности задавать размер поля)
game = field_gen(n)  # создание поля(матрицы)
grid_print(n)  # вывод поле в виде текста

while True:  # основной цикл

    # ход игрока 1
    input_check(player_1)
    grid_print(n)
    winner = win_check(player_1)

    if winner is not None:  # запрос о перезапуске игры в случае победы/ничьи
        if game_reset() == "Y":
            #   n = grid_size_input()  # включить для возможности задавать размер поля
            game.clear()  # создание новой игры в случае перезапуска
            game = field_gen(n)
            grid_print(n)
        else:
            break
        continue

    # ход игрока 2
    input_check(player_2)
    grid_print(n)
    winner = win_check(player_2)
    if winner is not None:
        if game_reset() == "Y":
            #   n = grid_size_input()  # включить для возможности задавать размер поля
            game.clear()
            game = field_gen(n)
            grid_print(n)
        else:
            break
        continue

print("Пока!")  #
