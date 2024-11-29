from tkinter import *
from pickle import load, dump
import time




def set_status(text):
    global text_id
    canvas.itemconfig(text_id, text=text)
def pause_toggle():
    global pause
    if not game_over:
        pause = not pause
        if pause:
            set_status("Пауза")
        else:
            set_status("Вперед!")
def menu_toggle():
    global menu_mode
    menu_mode = not menu_mode
    if menu_mode:
        menu_show()
    else:
        menu_hide()


def key_handler(event):
    global KEY_PLAYER1, KEY_PLAYER2, KEY_PAUSE, KEY_ESC, KEY_ENTER, SPEED, x1, x2, game_over, menu_mode, menu_current_index

    # Управление игроком 1
    if event.keycode == KEY_PLAYER1:
        x1 += SPEED
        canvas.coords(player1, x1, y1, x1 + player_size, y1 + player_size)

    # Управление игроком 2
    elif event.keycode == KEY_PLAYER2:
        x2 += SPEED
        canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)

    # Пауза
    elif event.keycode == KEY_PAUSE:
        pause_toggle()

    # Выход в меню
    elif event.keycode == KEY_ESC:
        if not menu_mode:
            menu_toggle()

    # Выбор опции в меню
    elif event.keycode == KEY_ENTER and menu_mode:
        menu_enter()

    # Перемещение вверх в меню
    elif event.keycode == KEY_UP and menu_mode:
        menu_up()

    # Перемещение вниз в меню
    elif event.keycode == KEY_DOWN and menu_mode:
        menu_down()

    # Проверка завершения гонки
    check_finish()
def check_finish():
    global x1, x2, game_over
    if x1 >= x_finish or x2 >= x_finish:
        game_over = True
        set_status(f'Победил игрок {"первый" if x1 > x2 else "второй"}!')


def menu_enter():
    global menu_current_index, menu_options
    option = menu_options[menu_current_index]

    if option == 'Возврат в игру':
        menu_toggle()
    elif option == 'Новая игра':
        game_new()
        menu_hide()
    elif option == 'Сохранить':
        game_save()
    elif option == 'Загрузить':
        game_load()
    elif option == 'Выход':
        game_exit()
def game_new():
    global x1, x2, game_over, pause, menu_mode
    x1, y1 = 50, 50
    x2, y2 = x1, y1 + player_size + 100
    canvas.coords(player1, x1, y1, x1 + player_size, y1 + player_size)
    canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)
    game_over = False
    pause = False
    menu_mode = False
    set_status("Вперед!")
def game_resume():
    global menu_mode
    menu_mode = False
    menu_hide()
def game_save():
    data = {
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
        'game_over': game_over,
        'pause': pause,
        'menu_mode': menu_mode,
        'menu_current_index': menu_current_index
    }
    with open('save.pkl', 'wb') as f:
        dump(data, f)
    set_status("Игра сохранена!")
def game_load():
    global x1, y1, x2, y2, game_over, pause, menu_mode, menu_current_index
    try:
        with open('save.pkl', 'rb') as f:
            data = load(f)
        x1 = data['x1']
        y1 = data['y1']
        x2 = data['x2']
        y2 = data['y2']
        game_over = data['game_over']
        pause = data['pause']
        menu_mode = data['menu_mode']
        menu_current_index = data['menu_current_index']
        canvas.coords(player1, x1, y1, x1 + player_size, y1 + player_size)
        canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)
        if menu_mode:
            menu_show()
        else:
            menu_hide()
        set_status("Игра загружена!")
    except FileNotFoundError:
        set_status("Файл сохранения не найден.")
def game_exit():
    window.destroy()
def menu_show():
    for i in range(len(menu_options)):
        canvas.itemconfig(menu_options_id[i], state=NORMAL)
def menu_hide():
    for id in menu_options_id:
        canvas.itemconfig(id, state=HIDDEN)
def menu_up():
    global menu_current_index
    menu_current_index = (menu_current_index - 1) % len(menu_options)
    menu_update()
def menu_down():
    global menu_current_index
    menu_current_index = (menu_current_index + 1) % len(menu_options)
    menu_update()
def menu_update():
    for i in range(len(menu_options)):
        color = 'green' if i == menu_current_index else 'black'
        canvas.itemconfig(menu_options_id[i], fill=color)
def menu_create(canvas):
    global menu_options_id
    y = 200
    for option in menu_options:
        id = canvas.create_text(game_width // 2, y, text=option, font=('Arial', '20'), fill='black')
        menu_options_id.append(id)
        y += 40
game_width = 800
game_height = 800
menu_mode = True
menu_options = ['Возврат в игру', 'Новая игра', 'Сохранить', 'Загрузить', 'Выход']
menu_current_index = 3
menu_options_id = []

KEY_UP = 38
KEY_DOWN = 40
KEY_ESC = 27
KEY_ENTER = 13

player_size = 100
x1, y1 = 50, 50
x2, y2 = x1, y1 + player_size + 100
player1_color = 'red'
player2_color = 'blue'

x_finish = game_width - 50

KEY_PLAYER1 = 39
KEY_PLAYER2 = 68
KEY_PAUSE = 112

SPEED = 12

game_over = False
pause = False

game_width = 800
game_height = 800
window = Tk()
window.title('DMEC')

canvas = Canvas(window, width=game_width, height=game_height, bg='white')
canvas.pack()
menu_create(canvas)
player1 = canvas.create_rectangle(x1,
                                  y1,
                                  x1 + player_size,
                                  y1 + player_size,
                                  fill=player1_color)
player2 = canvas.create_rectangle(x2,
                                  y2,
                                  x2 + player_size,
                                  y2 + player_size,
                                  fill=player2_color)
finish_id = canvas.create_rectangle(x_finish,
                                    0,
                                    x_finish + 10,
                                    game_height,
                                    fill='black')
text_id = canvas.create_text(x1,
                             game_height - 50,
                             anchor=SW,
                             font=('Arial', '25'),
                             text='Вперед!')
window.bind('<KeyRelease>', key_handler)
window.mainloop()

