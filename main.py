from tkinter import *
from pickle import load, dump
import time




def set_status(text):
    global text_id
    canvas.itemconfig(text_id, text=text)



def key_handler(event):
    global KEY_PLAYER1, KEY_PLAYER2,  SPEED, x1, x2, game_over

    # Управление игроком 1
    if event.keycode == KEY_PLAYER1:
        x1 += SPEED
        canvas.coords(player1, x1, y1, x1 + player_size, y1 + player_size)

    # Управление игроком 2
    elif event.keycode == KEY_PLAYER2:
        x2 += SPEED
        canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)

    # Пауза

    # Проверка завершения гонки
    check_finish()
def check_finish():
    global x1, x2, game_over
    if x1 >= x_finish or x2 >= x_finish:
        game_over = True
        set_status(f'Победил игрок {"первый" if x1 > x2 else "второй"}!')





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

