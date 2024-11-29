import tkinter as tk

from tkinter import messagebox
# Глобальные переменные и константы
game_width = 800
game_height = 800
menu_mode = True
menu_options = ["Возврат в игру", "Новая игра", "Сохранить", "Загрузить", "Выход"]
menu_current_index = 0
menu_options_id = []

KEY_UP = 87
KEY_DOWN = 83
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
KEY_PAUSE = 32

SPEED = 12
menu_x = game_width // 2
menu_y = game_height // 2
menu_id = []  # Список для хранения идентификаторов пунктов меню

# Создание пунктов меню

game_over = False
pause = False
window = tk.Tk()
window.title("ИГРА")

canvas = tk.Canvas(window, width=game_width, height=game_height, bg="white")
canvas.pack()

# Отображение текста статуса
text_id = canvas.create_text(game_width // 2, 30, text="", font=('Arial', 16))

# Рисуем игроков
player1 = canvas.create_rectangle(x1, y1, x1 + player_size, y1 + player_size, fill=player1_color)
player2 = canvas.create_rectangle(x2, y2, x2 + player_size, y2 + player_size, fill=player2_color)


# Функция установки статуса
def set_status(message="", color="black"):
    canvas.itemconfig(text_id, text=message, fill=color)

# Функция переключения паузы
def pause_toggle():
    global pause
    pause = not pause
    if pause:
        set_status("Игра приостановлена", "green")
    else:
        set_status("")

# Функция переключения режима меню
def menu_toggle():
    global menu_mode
    menu_mode = not menu_mode
    if menu_mode:
        menu_show()
    else:
        menu_hide()
# Перемещаемся вверх по меню
def menu_up():
    global menu_current_index
    if menu_current_index > 0:
        menu_current_index -= 1
        highlight_menu_option()

# Перемещаемся вниз по меню
def menu_down():
    global menu_current_index
    if menu_current_index < len(menu_options) - 1:
        menu_current_index += 1
        highlight_menu_option()

# Подсветка текущего пункта меню
def highlight_menu_option():
    for i, option in enumerate(menu_options):
        if i == menu_current_index:
            canvas.itemconfigure(menu_options_id[i], fill="blue")
        else:
            canvas.itemconfigure(menu_options_id[i], fill="black")

# Обработчик событий клавиатуры
def key_handler(event):
    global menu_mode, menu_current_index, pause, game_over
    if event.char == chr(KEY_ESC):
        menu_toggle()
    elif event.char == chr(KEY_PAUSE):
        pause_toggle()
    elif menu_mode:
        if event.char == chr(KEY_UP):
            menu_up()
        elif event.char == chr(KEY_DOWN):
            menu_down()
        elif event.char == chr(KEY_ENTER):
            menu_enter(menu_current_index)
    elif not pause and not game_over:
        if event.char == chr(KEY_PLAYER1):
            canvas.move(player1, SPEED, 0)
            x1 += SPEED
        elif event.char == chr(KEY_PLAYER2):
            canvas.move(player2, SPEED, 0)
            x2 += SPEED
        check_finish()

# Проверяем достижение финишной черты
def check_finish():
    global game_over
    if x1 >= x_finish or x2 >= x_finish:
        game_over = True
        winner = "Красный" if x1 >= x_finish else "Синий"
        set_status(f"Победил {winner} игрок!", "green")

# Выбор пункта меню
def menu_enter(index):
    global menu_mode, pause, game_over, x1, y1, x2, y2
    if index == 0:  # Возврат в игру
        menu_mode = False
        pause = False
    elif index == 1:  # Новая игра
        game_new()
    elif index == 2:  # Сохранить
        game_save()
    elif index == 3:  # Загрузить
        game_load()
    elif index == 4:  # Выход
        window.destroy()

# Начало новой игры
def game_new():
    global x1, y1, x2, y2, game_over
    x1, y1 = 50, 50
    x2, y2 = x1, y1 + player_size + 100
    canvas.coords(player1, x1, y1, x1 + player_size, y1 + player_size)
    canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)
    game_over = False
    pause = False
    menu_mode = False
    set_status("")

# Возобновление игры
def game_resume():
    global pause, menu_mode
    pause = False
    menu_mode = False
    set_status("")

# Сохранение игры
def game_save():
    with open("save.dat", "wb") as file:
        dump([x1, y1, x2, y2], file)
    messagebox.showinfo("Сохранено", "Текущая позиция игроков успешно сохранена!")

# Загрузка игры
def game_load():
    global x1, y1, x2, y2
    try:
        with open("save.dat", "wb") as file:
            pass
    except FileExistsError:
        print("Файл уже существует")
    except Exception as e:
        print(f"Произошла ошибка при создании файла: {e}")


# Выход из игры
def game_exit():
    window.destroy()

# Показываем меню
def menu_show():
    for id in menu_options_id:
        canvas.itemconfigure(id, state="normal")

# Скрываем меню
def menu_hide():
    global menu_visible

    if menu_visible:
        # Код для скрытия меню
        canvas.itemconfig(menu_id, state='hidden')
        menu_visible = False
    else:
        # Код для отображения меню
        canvas.itemconfig(menu_id, state='normal')
        menu_visible = True

