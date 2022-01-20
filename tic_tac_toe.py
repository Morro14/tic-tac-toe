player_1 = "Player 1"
player_2 = "Player 2"
draw = "Draw"
n = 3


def game_reset():
    """Requests an input ("Y" or "N") in order to know if the user wants to play another round or quit
    the game """
    ask_if_continue = None
    while True:
        print('Do you want to play another round? (Y/N):', end='')
        ask_if_continue = input()
        if ask_if_continue == "Y":
            return ask_if_continue
        elif ask_if_continue == "N":
            return ask_if_continue


def grid_size_input():
    """Requests an input (int) to determine the game field size"""
    while True:
        print("Enter the field length (from 2 to 20): ", end="")
        length = input()
        if length.isdigit() == 1:
            length = int(length)
        else:
            continue
        if 2 <= length <= 20:
            return length


def field_gen(len_gen):
    """Generates a list in a form of a matrix that represents the game field with the length defined by the user.
    Zeroes stand for empty cells."""
    game_gen = []
    for c in range(len_gen):
        game_gen.append([])
        for r in range(len_gen):
            game_gen[c].append(0)
    return game_gen


def grid_print(len_print):
    """Prints out the grid in a text format."""
    print('   ', end='')
    for m in range(1, len_print + 1):
        if m >= 10:
            print(f' {m} ', end='')
        if m < 10:
            print(f'  {m} ', end='')
    print('\n', end='')

    lines = '--- ' * len_print
    print('    ' + lines)
    for i in range(0, len_print):

        print('%2d ' % (i + 1), end='')
        for elem in range(0, len_print):
            if game[i][elem] == 0:
                print(f'|   ', end='') if elem < len_print - \
                    1 else print(f'|   |', end='')
            if game[i][elem] == 1:
                print(f'| X ', end='') if elem < len_print - \
                    1 else print(f'| X |', end='')
            if game[i][elem] == 2:
                print(f'| O ', end='') if elem < len_print - \
                    1 else print(f'| O |', end='')

        print('\n' + '    ' + lines)


def input_check(player):
    """Asks players to make their turn and add result into the list. "1" - Player 1, "2" - Player 2."""
    while True:
        p_input = input(
            f'{player}, enter the row and column numbers (X "space" Y): ')
        p_input = p_input.split(' ')
        if len(p_input) != 2 or p_input[0].isdigit() == 0 or p_input[1].isdigit() == 0:
            continue

        column, row = p_input
        column, row = int(column), int(row)
        if (row not in range(1, n + 1)) or (column not in range(1, n + 1)):
            print('The cell is not on the field!')
            continue
        if game[row - 1][column - 1] != 0:
            print('The cell is occupied!')
            continue
        if player == player_1:
            game[row - 1][column - 1] = 1
        else:
            game[row - 1][column - 1] = 2
        break


def win_count(fn):
    """Saves win/draw stats."""
    player_1_wins, player_2_wins, draws = 0, 0, 0

    def wrapper(*args):
        nonlocal player_1_wins, player_2_wins, draws
        winner_wrapper = fn(*args)
        if winner_wrapper == player_1:
            player_1_wins += 1
            print('Player 1 wins!')

        if winner_wrapper == player_2:
            player_2_wins += 1
            print('Player 2 wins!')

        if winner_wrapper == draw:
            draws += 1
            print('Draw!')
        if winner_wrapper is not None:
            print('\n''---------score---------')
            print(f'<Player 1> wins: {player_1_wins}')
            print(f'<Player 2> wins: {player_2_wins}')
            print(f'Draws: {draws}')
        return winner_wrapper

    return wrapper


def diagonal_1_check(*args):
    """Checks the 1st diagonal for the win condition."""
    for i in range(n - 1):
        if game[i][i] == 0 or game[i][i] != game[i + 1][i + 1]:
            return None
    if game[0][0] == 1:
        return player_1
    if game[0][0] == 2:
        return player_2


def diagonal_2_check(*args):
    """Checks the 2nd diagonal for the win condition"""
    for i in range(n - 1):
        if game[i][n - 1 - i] == 0 or game[i][n - 1 - i] != game[i + 1][n - 2 - i]:
            return None
    if game[0][n - 1] == 1:
        return player_1
    if game[0][n - 1] == 2:
        return player_2


def lines_check(player):
    """Checks rows and columns for the win condition"""
    vertical_list = []

    for i in range(n):
        for z in range(n):
            vertical_list.append(game[z][i])
        vertical_set = set(vertical_list)
        if player == player_1:
            if ((len(set(game[i])) == 1 and game[i][
                0] == 1) or
                    (len(vertical_set) == 1 and game[0][
                        i] == 1)):
                return player_1
        if player == player_2:
            if ((len(set(game[i])) == 1 and game[i][0] == 2) or
                    (len(vertical_set) == 1 and game[0][i] == 2)):
                return player_2

        vertical_list.clear()
        vertical_set.clear()
    return None


def draw_check(*args):
    """Checks for draw condition."""
    for i in range(n):
        if 0 in game[i]:
            return None
    return draw


@win_count
def win_check(player):
    """Checks all the win/draw conditions."""
    winner_check = None
    fn_list = [lines_check, diagonal_1_check, diagonal_2_check, draw_check]
    for i in range(len(fn_list)):
        if winner_check is None:
            winner_check = fn_list[i](player)
    return winner_check


n = grid_size_input()
game = field_gen(n)
grid_print(n)

while True:

    input_check(player_1)
    grid_print(n)
    winner = win_check(player_1)

    if winner is not None:
        if game_reset() == "Y":
            n = grid_size_input()
            game.clear()
            game = field_gen(n)
            grid_print(n)
        else:
            break
        continue

    input_check(player_2)
    grid_print(n)
    winner = win_check(player_2)
    if winner is not None:
        if game_reset() == "Y":
            n = grid_size_input()
            game.clear()
            game = field_gen(n)
            grid_print(n)
        else:
            break
        continue

print("Bye!")
