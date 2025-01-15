# 生成题库
import random
import copy


def generate_sudoku_board():
    # 创建一个9x9的二维列表，表示数独棋盘
    board = [[0] * 9 for _ in range(9)]

    # 递归函数，用于填充数独棋盘的每个单元格
    def filling_board(row, col):
        # 检查是否填充完成整个数独棋盘
        if row == 9:
            return True

        # 计算下一个单元格的行和列索引
        next_row = row if col < 8 else row + 1
        next_col = (col + 1) % 9

        # 获取当前单元格在小九宫格中的索引
        box_row = row // 3
        box_col = col // 3

        # 随机生成1到9的数字
        numbers = random.sample(range(1, 10), 9)

        for num in numbers:
            # 检查行、列、小九宫格是否已经存在相同的数字
            if num not in board[row] and all(board[i][col] != num for i in range(9)) and all(
                    num != board[i][j] for i in range(box_row * 3, box_row * 3 + 3) for j in
                    range(box_col * 3, box_col * 3 + 3)):
                board[row][col] = num

                # 递归填充下一个单元格
                if filling_board(next_row, next_col):
                    return True

                # 回溯，将当前单元格重置为0
                board[row][col] = 0

        return False

    # 填充数独棋盘
    filling_board(0, 0)

    return board


def create_board(level):  # level数字越大代表游戏难度越大
    """
    生成一个随机的数独棋盘,空白格少
    """
    board = generate_sudoku_board()
    board1 = copy.deepcopy(board)
    for i in range(81):
        row = i // 9
        col = i % 9
        if random.randint(0, 9) < level:
            board1[row][col] = 0
    return (board, board1)


import tkinter as tk
import ctypes
from tkinter import messagebox

root = tk.Tk()
# 界面优化代码---------------------------------
# 调用api设置成由应用程序缩放
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# 调用api获得当前的缩放因子
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
# 设置缩放因子
root.tk.call('tk', 'scaling', ScaleFactor / 75)
# --------------------------------------------

root.title('数独游戏')
root.geometry('900x1000')
frame = tk.Frame(root, width=500, height=500)
frame.pack()


# 输入框验证函数 ——针对已给出的数字
def validate_input1(new_value):
    if new_value.isdigit() and int(new_value) >= 1 and int(new_value) <= 9:
        return True
    return False


# 输入框验证函数 ——针对待填入的数字
def validate_input2(new_value):
    if new_value == "":
        return True

    if len(new_value) == 1 and new_value.isdigit():
        if 1 <= int(new_value) <= 9:
            return True
    return False


validate_cmd1 = frame.register(validate_input1)
validate_cmd2 = frame.register(validate_input2)


# 绘制九宫格
def print_board(frame, board):
    """
    在界面上显示数独棋盘
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                label = tk.Entry(frame, width=4, font=('TimesNewom', 15, 'bold'), validate="key",
                                 validatecommand=(validate_cmd2, "%P"))
            else:
                label = tk.Entry(frame, width=4, font=('TimesNewom', 15, 'bold'), validate="key",
                                 validatecommand=(validate_cmd1, "%P"))  # 注意这里的参数要和上面的label一致，否则会出奇怪的bug~
                label.insert(-1, str(board[i][j]))

            label.grid(row=i, column=j, padx=10, pady=10)

            # 添加高亮显示
            label.row = i
            label.col = j
            label.bind('<FocusIn>', highlight)
            label.bind('<Leave>', unhighlight)
            label.bind('<KeyRelease>', update_board)


# 高亮显示当前格子所在的行、列和小九宫格
def highlight(event):
    row, col = event.widget.row, event.widget.col
    for i in range(9):
        # 高亮行
        if i != row:
            label = event.widget.master.grid_slaves(row=i, column=col)[0]
            label.config(bg='yellow', font=('times', 15))
        # 高亮列
        if i != col:
            label = event.widget.master.grid_slaves(row=row, column=i)[0]
            label.config(bg='yellow', font=('times', 15))
        # 高亮小九宫格
        r = row // 3 * 3 + i // 3
        c = col // 3 * 3 + i % 3
        if (r, c) != (row, col):
            label = event.widget.master.grid_slaves(row=r, column=c)[0]
            label.config(bg='yellow', font=('times', 15))

    # 高亮当前格子
    label = event.widget
    label.config(bg='yellow')


# 取消高亮显示
def unhighlight(event):
    row, col = event.widget.row, event.widget.col
    for i in range(9):
        # 取消高亮行
        if i != row:
            label = event.widget.master.grid_slaves(row=i, column=col)[0]
            label.config(bg='white', font=('times', 15))
        # 取消高亮列
        if i != col:
            label = event.widget.master.grid_slaves(row=row, column=i)[0]
            label.config(bg='white', font=('times', 15))
        # 取消高亮小九宫格
        r = row // 3 * 3 + i // 3
        c = col // 3 * 3 + i % 3
        if (r, c) != (row, col):
            label = event.widget.master.grid_slaves(row=r, column=c)[0]
            label.config(bg='white', font=('times', 15))

        # 取消高亮显示相同数字的格子
        for i in range(9):
            for j in range(9):
                if board[i][j] == board[row][col]:
                    label = event.widget.master.grid_slaves(row=i, column=j)[0]
                    label.config(fg='black', font=('times', 15))

    # 取消高亮当前格子
    label = event.widget
    label.config(bg='white')


# 更新当前格子的值，并高亮相同数字
def update_board(event):
    row, col = event.widget.row, event.widget.col
    val = event.widget.get()
    if len(val) > 0:
        if val.isdigit() and 1 <= int(val) <= 9:
            aa[1][row][col] = int(val)
        else:
            event.widget.delete(0, 'end')
            event.widget.insert(0, str(aa[1][row][col]))

    # 高亮相同数字的格子
    for i in range(9):
        for j in range(9):
            if aa[1][i][j] == aa[1][row][col]:
                label = event.widget.master.grid_slaves(row=i, column=j)[0]
                label.config(fg='red', font=('times', 15, 'bold'))


def XX(level):
    global aa  # 通过全局变量可以获取每次按键刷新后的棋盘
    aa = create_board(level)
    return aa


board = XX(5)[1]
print_board(frame, board)


# 添加按键组件
def Button(root, level1, level2):
    button1 = tk.Button(root, text="出题:难度1", command=lambda: print_board(frame, XX(level1)[1]), relief="raised",
                        height=2, font=('楷体', 10, 'bold'))  # 注意加上lambda!
    button1.pack(side=tk.LEFT, padx=10, pady=10)

    button2 = tk.Button(root, text="出题:难度2", command=lambda: print_board(frame, XX(level2)[1]), relief="raised",
                        height=2, font=('楷体', 10, 'bold'))
    button2.pack(side=tk.LEFT, padx=10, pady=10)

    button3 = tk.Button(root, text="解题", command=lambda: print_board(frame, aa[0]), relief="raised", height=2,
                        font=('楷体', 10, 'bold'))
    button3.pack(side=tk.LEFT, padx=10, pady=10)

    button4 = tk.Button(root, text="验证", command=lambda: check(aa[1]), relief="raised", height=2,
                        font=('楷体', 10, 'bold'))
    button4.pack(side=tk.LEFT, padx=10, pady=10)

    button_quit = tk.Button(root, text='退出', command=root.quit, bg='red', relief="raised", height=2,
                            font=('楷体', 10, 'bold'))
    button_quit.pack(side=tk.RIGHT, padx=10, pady=10)


Button(root, 5, 7)


# 判断输赢
def check_victory(sudo):
    # 检查每行是否有重复数字
    for row in sudo:
        if len(set(row)) != 9:
            return False

    # 检查每列是否有重复数字
    for col in range(9):
        column = [sudo[row][col] for row in range(9)]
        if len(set(column)) != 9:
            return False

    # 检查每个3x3的小九宫格内是否有重复数字
    for box_row in range(3):
        for box_col in range(3):
            box = [sudo[box_row * 3 + i][box_col * 3 + j] for i in range(3) for j in range(3)]
            if len(set(box)) != 9:
                return False
    return True


def check(sudo):
    if sudo == aa[1]:
        if check_victory(sudo):
            messagebox.showinfo("提示", "恭喜你，你赢了！")
        else:
            messagebox.showinfo("提示", "很遗憾，你输了！")


root.mainloop()

