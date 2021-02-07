import tkinter as tk
import random as rd
import subprocess
from tkinter import messagebox
from numpy import array
from time import sleep


player = 'X'
buttons_grid = [[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]
copied_grid = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]
violet = '#94268e'


def sign_config(sign_label, sign_text, **additions):
    return sign_label.config(additions, text=sign_text, )


def free_places():
    places = []
    for i in range(3):
        for j in range(3):
            if not buttons_grid[i][j]['text']:
                places.append([i, j])
    return places


def win_color(*buttons, which_color=violet):
    for i in buttons:
        i.config(bg=which_color)


def game_check(which_button_grid):
    for i in range(3):
        if which_button_grid[i][0]['text'] == which_button_grid[i][1]['text'] == which_button_grid[i][2]['text'] != '':
            for j in range(3):
                win_color(which_button_grid[i][j])
            return 1
        elif which_button_grid[0][i]['text'] == which_button_grid[1][i]['text'] == which_button_grid[2][i]['text'] != '':
            for j in range(3):
                win_color(which_button_grid[j][i])
            return 1

    if which_button_grid[0][0]['text'] == which_button_grid[1][1]['text'] == which_button_grid[2][2]['text'] != '':
        for i in range(3):
            win_color(which_button_grid[i][i])
        return 1

    elif which_button_grid[0][2]['text'] == which_button_grid[1][1]['text'] == which_button_grid[2][0]['text'] != '':
        win_color(
            which_button_grid[0][2], which_button_grid[1][1], which_button_grid[2][0])
        return 1  # A player has won

    elif not free_places():
        return 0  # Game Draw

    return -1  # Game still not finished


def restart_game(board_name):  # Restarts the whole app (Rerun)
    restart_window = messagebox.askyesno(
        'Restart', 'Do you want to restart the game?')

    if restart_window:
        board_name.destroy()
        subprocess.run(['python3', 'simpletictactoe.py'])
    else:
        return None


def pvp_game(i, j, sign_label):  # Person Vs Person
    global player

    if not buttons_grid[i][j]['text'] and game_check(buttons_grid) == -1:
        if player == 'X':
            buttons_grid[i][j].config(text="X")

            if game_check(buttons_grid) == -1:
                player = "O"
                sign_config(sign_label, player + ' turn')

            elif game_check(buttons_grid) == 1:
                sign_config(sign_label, player + ' won!', fg='red')

            elif game_check(buttons_grid) == 0:
                sign_config(sign_label, 'DRAW', fg='green')

        elif player == 'O':
            buttons_grid[i][j].config(text="O")

            if game_check(buttons_grid) == -1:
                player = 'X'
                sign_config(sign_label, player + ' turn')

            elif game_check(buttons_grid) == 1:
                sign_config(sign_label, player + 'won!', fg='blue')

            elif game_check(buttons_grid) == 0:
                sign_config(sign_label, 'DRAW', fg='green')


def free_spot(i, j):  # Check for free spots in the board
    return buttons_grid[i][j]['text'] == ''


players = ['player', 'pc']
turn = rd.choice(players)


def pve_game(i, j, sign_label):  # Person Vs Environment (Computer)
    global turn
    sign_config(sign_label, turn.capitalize() + ' turn')

    def countdown(timing=35): # Countdown for 3.5 seconds each time before the enemy plays
        while timing > -1:
            countdown_label = tk.Label(
                game_board, text=f'PC will play in:\n {int(timing/10)} seconds') # Divided by 10 so it so it shows in seconds
            countdown_label.grid(row=4, column=1)
            game_board.after(100) # Every 1000 is 1 second so if it is 1000 then the player will be delayed for 1 sec
            timing -= 1
            game_board.update()

    def enemy_strategy():
        global turn

        for i in range(3):
            for j in range(3):
                xo_text = buttons_grid[i][j]['text']
                copied_grid[i][j].config(text=xo_text)

        corners = [[0, 0], [2, 0], [2, 2], [0, 2]]
        middle_sides = [[0, 1], [1, 0], [2, 1], [1, 2]]

        if len(free_places()) == 9:

            any_corner = rd.choice(corners)

            buttons_grid[any_corner[0]][any_corner[-1]].config(text='O')
            copied_grid[any_corner[0]][any_corner[-1]].config(text='O')

            turn = 'player'
            sign_config(sign_label, turn.capitalize() + ' turn')

        elif free_spot(1, 1):
            buttons_grid[1][1].config(text='O')
            copied_grid[1][1].config(text='O')
            turn = 'player'
            sign_config(sign_label, turn.capitalize() + ' turn')

        elif (buttons_grid[0][0]['text'] == buttons_grid[2][2]['text'] == 'X' and buttons_grid[1][1]['text'] == 'O' and len(free_places()) == 6) or \
                (buttons_grid[2][0]['text'] == buttons_grid[0][2]['text'] == 'X' and buttons_grid[1][1]['text'] == 'O' and len(free_places()) == 6):
            any_side = rd.choice(middle_sides)
            buttons_grid[any_side[0]][any_side[-1]].config(text='O')
            turn = 'player'
            sign_config(sign_label, turn.capitalize() + ' turn')

        else:
            for x, i in enumerate(free_places()):
                grid_copy = array(buttons_grid)
                grid_copy[i[0]][i[-1]].config(text='O')

                if game_check(grid_copy) == 1:
                    buttons_grid[i[0]][i[-1]].config(text='O')
                    sign_config(sign_label, 'Pc Won!', fg='red')
                    break

                elif game_check(grid_copy) == 0:
                    buttons_grid[i[0]][i[-1]].config(text='O')
                    sign_config(sign_label, 'DRAW', fg='green')
                    break

                elif game_check(grid_copy) == -1:
                    copied_grid[i[0]][i[-1]].config(text='')
                    grid_copy[i[0]][i[-1]].config(text='')

                    if x == len(free_places())-1:
                        places_len = len(free_places())

                        for j, y in enumerate(free_places()):
                            if j < places_len - 1:
                                copied_grid[y[0]][y[-1]].config(text='X')

                                if game_check(copied_grid) == 1:
                                    buttons_grid[y[0]][y[-1]].config(text='O')
                                    turn = 'player'
                                    sign_config(
                                        sign_label, turn.capitalize() + ' turn')
                                    break
                                else:
                                    copied_grid[y[0]][y[-1]].config(text='')
                                    continue
                            else:
                                buttons_grid[i[0]][i[-1]].config(text='O')
                                copied_grid[i[0]][i[-1]].config(text='O')
                                turn = 'player'
                                sign_config(sign_label, turn.capitalize() + ' turn')
                                break
                    else:
                        continue

    if not buttons_grid[i][j]['text'] and game_check(buttons_grid) == -1:
        if turn == 'player':
            buttons_grid[i][j].config(text='X')

            if game_check(buttons_grid) == -1:
                turn = 'pc'
                sign_config(sign_label, turn.capitalize() + ' turn')
                countdown()
                enemy_strategy()

            elif game_check(buttons_grid) == 1:
                sign_config(sign_label, 'Player Won!', fg='blue')

            elif game_check(buttons_grid) == 0:
                sign_config(sign_label, 'DRAW', fg='green')

        elif turn == 'pc':
            sign_config(sign_label, turn.capitalize() + ' turn')
            countdown()
            enemy_strategy()


def board(function_to_use=None):
    global game_board
    game_board = tk.Tk()
    game_board.title('1 VS 1')
    sign_label = tk.Label(game_board, text=f"{turn.capitalize()} turn", font=('normal', 23, 'bold'), fg=violet)
    sign_label.grid(row=0, column=1)

    for i in range(3):
        for j in range(3):
            buttons_grid[i][j] = tk.Button(game_board, height=3, width=5, text='',
                                           command=lambda r=i, c=j, turn_label=sign_label: function_to_use(r, c, turn_label), border=0, bg='#e6cd15', fg='#00239c',
                                           font=('normal', 40, 'bold'), bd=10, relief='sunken')
            buttons_grid[i][j].grid(row=i+1, column=j)

            copied_grid[i][j] = tk.Button(game_board, text='') # Will generate a second grid to do some tests on it.

    resexit_font = ('Arial', 11, 'bold')

    restart_button = tk.Button(game_board, fg=violet, text='Restart', height=2, width=25,
                               command=lambda: restart_game(game_board), border=4, relief='sunken', bg='black', font=resexit_font)
    restart_button.grid(row=0, column=2)

    exit_button = tk.Button(game_board, fg=violet, text='Exit', height=2, width=25,
                            command=lambda: exit(), border=4, relief='sunken', bg='black', font=resexit_font)
    exit_button.grid(row=0, column=0)

    game_board.resizable(0, 0)
    game_board.mainloop()


def destroy_open(screen_destroy, screen_open, which_function):
    screen_destroy.destroy()
    screen_open(which_function)


def menu_screen_func():
    global turn
    menu_screen = tk.Tk()
    menu_screen.geometry('750x540')
    menu_screen.title('Tic Tac Toe')
    
    menu_screen.columnconfigure(0, weight=1)
    menu_screen.columnconfigure(1, weight=1)
    menu_screen.rowconfigure(0, weight=1)
    menu_screen.rowconfigure(1, weight=8)
    menu_screen.rowconfigure(2, weight=1)
    
    tk.messagebox.showinfo('INFO', '''If you choose to play versus pc and it's PC turn, press any button once to start the game.
\nThe enemy will play 3 seconds after you do.''')

    menu_label = tk.Label(menu_screen, text='Choose Game Mode', font=('arial', 18, 'normal'), bg='black', fg='white')
    menu_label.grid(row=0, column=0, sticky='NSEW', columnspan=2)

    button_font = ('palatino', 22, 'bold')
    butpvp = tk.Button(menu_screen, text='1 Vs 1',
                       command=lambda: destroy_open(menu_screen, board, pvp_game), bg='red', fg='black', font=button_font,
                       activebackground='black', activeforeground='red', bd=6) # destroys current screen and open the new screen
    
    butpvp.grid(row=1, column=0, sticky='NSEW')

    butpve = tk.Button(menu_screen, text='1 Vs Pc', bg='blue', fg='black', activebackground='black',
                       activeforeground='blue', font=button_font, bd=6, command=lambda: destroy_open(menu_screen, board, pve_game))

    butpve.grid(row=1, column=1, sticky='NSEW')

    exit_button = tk.Button(menu_screen, text='Exit', bg='black', fg='white', command=lambda: exit(),
    font=('arial', 16, 'normal'), bd=4, relief='groove')
    exit_button.grid(row=2, column=0, sticky='NSEW', columnspan=2)

    menu_screen.mainloop()


if __name__ == '__main__':
    menu_screen_func()
