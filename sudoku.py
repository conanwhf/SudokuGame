import tkinter as tk
from ui import Sudoku

if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    # 创建数独游戏实例
    sudoku = Sudoku(root)
    # 开始一个简单难度的新游戏
    sudoku.new_game("简单")
    # 进入主循环,等待用户操作
    root.mainloop()
