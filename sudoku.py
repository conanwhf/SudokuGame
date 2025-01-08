import tkinter as tk
from tkinter import messagebox
import random
import config

class Sudoku:
    """数独游戏主类，负责管理游戏逻辑和UI"""
    def __init__(self, master):
        """初始化数独游戏
        Args:
            master: tkinter根窗口对象
        """
        self.master = master  # 保存主窗口对象
        master.title(config.WINDOW['title'])  # 设置窗口标题
        # 设置窗口最小尺寸
        master.minsize(config.WINDOW['min_width'], config.WINDOW['min_height'])
        
        # 初始化撤销/重做栈
        self.undo_stack = []
        self.redo_stack = []
        
        # 初始化检查次数
        self.max_checks = config.GAME['max_checks']  # 最大检查次数
        self.check_count = 0
        
        self.new_game()  # 开始新游戏

    def new_game(self, difficulty="简单"):
        """开始新游戏
        Args:
            difficulty: 游戏难度，可选"简单"、"中等"、"困难"
        """
        self.board = self.generate_board()  # 生成完整数独
        self.solution = [row[:] for row in self.board]  # 保存原始答案
        self.cells = {}  # 初始化单元格字典
        
        # 保存当前难度设置
        current_difficulty = difficulty
        
        # 清除所有现有的界面组件
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # 根据难度移除不同数量的数字
        self.remove_numbers(self.board, current_difficulty)
        
        # 创建游戏界面
        self.create_widgets()
        
        # 设置难度下拉菜单的值
        self.difficulty_var.set(current_difficulty)

    def generate_board(self):
        """生成一个完整的数独棋盘"""
        print("开始生成数独棋盘...")
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        # 优化1：先填充对角线上的3个3x3方格
        # 这些方格之间互不影响（不共享行列），可以独立填充
        # 这样可以提供一个良好的初始状态，加快后续填充
        for i in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)  # 随机打乱1-9的顺序
            for row in range(3):
                for col in range(3):
                    # 将打乱后的数字按顺序填入3x3方格
                    board[i + row][i + col] = nums[row * 3 + col]
        
        print("开始填充剩余格子...")
        if self.fill_board(board):
            print("数独棋盘生成成功！")
            return board
        else:
            # 如果填充失败，重新生成整个棋盘
            print("生成失败，重试中...")
            return self.generate_board()

    def fill_board(self, board):
        """使用优化的回溯算法填充数独棋盘
        
        优化策略：
        1. 优先填充可能性最少的位置
        2. 提前计算有效数字，减少无效尝试
        """
        # 找到最优的空位置（可能性最少的位置）
        empty = self.find_empty(board)
        if not empty:
            return True
        
        row, col = empty
        nums = list(range(1, 10))
        random.shuffle(nums)  # 随机打乱数字顺序，增加生成棋盘的随机性
        
        # 优化2：提前计算当前位置所有可能的有效数字
        # 避免在回溯过程中重复验证无效数字
        possible_nums = []
        for num in nums:
            if self.is_valid_for_check(board, row, col, num):
                possible_nums.append(num)
        
        # 只尝试可能的有效数字
        for num in possible_nums:
            board[row][col] = num
            if self.fill_board(board):
                return True
            board[row][col] = 0
        
        return False

    def find_empty(self, board):
        """查找最优的空位置
        
        优化策略：不是返回第一个找到的空位置，而是返回可能性最少的位置
        这样可以显著减少回溯次数，因为：
        1. 可能性少的位置填错的概率更低
        2. 即使填错，也能更快地发现错误并回溯
        """
        min_possibilities = 10  # 初始化为一个大于9的数
        best_position = None
        
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    # 计算当前空位置可以填入的有效数字数量
                    count = 0
                    for num in range(1, 10):
                        if self.is_valid_for_check(board, i, j, num):
                            count += 1
                    # 更新最优位置
                    if count < min_possibilities:
                        min_possibilities = count
                        best_position = (i, j)
                        # 如果找到只有一种可能的位置，立即返回
                        # 这是最优的情况，不需要继续搜索
                        if count == 1:
                            return best_position
        
        return best_position

    def remove_numbers(self, board, difficulty):
        """根据难度移除数字创建数独谜题"""
        print(f"开始移除数字，难度：{difficulty}")
        # 根据难度设置要移除的数字数量
        cells_to_remove = config.GAME['difficulties'][difficulty]  # 根据难度设置要移除的数字数量
        
        print(f"计划移除 {cells_to_remove} 个数字")
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        removed_count = 0
        for i in range(cells_to_remove):
            row, col = positions[i]
            temp = board[row][col]
            board[row][col] = 0
            
            print(f"尝试移除位置 ({row}, {col}) 的数字 {temp}")
            # 如果移除后导致多解，则恢复该数字
            if not self.is_unique_solution(board):
                print(f"移除后会导致多解，恢复数字 {temp}")
                board[row][col] = temp
            else:
                removed_count += 1
                print(f"成功移除数字，当前已移除 {removed_count} 个数字")
        
        print(f"完成数字移除，共移除 {removed_count} 个数字")

    def is_unique_solution(self, board):
        """检查数独谜题是否有唯一解"""
        temp_board = [row[:] for row in board]
        count = [0]  # 使用列表存储计数，以便在内部函数中修改

        def solve():
            if count[0] > 1:  # 如果已经找到多个解，直接返回
                return True
            
            # 找到一个空位置
            empty = self.find_empty(temp_board)
            if not empty:
                count[0] += 1
                return count[0] == 1

            row, col = empty
            for num in range(1, 10):
                if self.is_valid_for_check(temp_board, row, col, num):
                    temp_board[row][col] = num
                    solve()
                    if count[0] > 1:
                        return True
                    temp_board[row][col] = 0
            return False

        solve()
        return count[0] == 1

    def is_valid_for_check(self, board, row, col, num):
        """检查数字在指定位置是否有效
        Args:
            board: 当前数独棋盘状态
            row: 行索引 (0-8)
            col: 列索引 (0-8)
            num: 要检查的数字 (1-9)
        Returns:
            bool: 数字是否有效
        """
        # 检查同一行和同一列
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        # 检查3x3小方格
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def create_widgets(self):
        """创建游戏界面组件"""
        # 创建主容器，移除背景色设置
        main_container = tk.Frame(self.master, padx=20, pady=20)
        main_container.grid(row=0, column=0)

        # 创建标题标签
        title_label = tk.Label(main_container, text="数独游戏",
                              font=config.FONTS['title'], pady=10)
        title_label.grid(row=0, column=0)

        # 创建数独网格的主框架
        main_grid = tk.Frame(main_container, 
                            relief='solid', 
                            borderwidth=2)
        main_grid.grid(row=1, column=0, pady=10)

        # 创建9个3x3的子框架，移除背景色设置
        subgrids = {}
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(main_grid, 
                               relief='solid', 
                               borderwidth=2)
                frame.grid(row=i, column=j, padx=2, pady=2)
                subgrids[(i, j)] = frame

        # 创建9x9的数独格子
        for i in range(9):
            for j in range(9):
                value = self.board[i][j]
                subgrid_row, subgrid_col = i // 3, j // 3
                cell_row, cell_col = i % 3, j % 3
                
                if value == 0:  # 空格子使用Entry组件
                    entry = tk.Entry(subgrids[(subgrid_row, subgrid_col)],
                                   width=2,
                                   font=config.FONTS['cell'],
                                   justify='center',
                                   relief='solid',
                                   borderwidth=1)
                    entry.grid(row=cell_row, column=cell_col,
                             padx=2, pady=2, ipadx=2, ipady=2)
                    entry.bind('<KeyPress>', self.validate_input)
                    # 修改高亮颜色
                    entry.bind('<FocusIn>', lambda e, entry=entry: 
                             entry.configure(bg='#e0e8ff'))
                    entry.bind('<FocusOut>', lambda e, entry=entry: 
                             entry.configure(bg='systemWindowBody'))
                    self.cells[(i, j)] = entry
                else:  # 已有数字使用Label组件
                    label = tk.Label(subgrids[(subgrid_row, subgrid_col)],
                                   text=str(value),
                                   width=2,
                                   font=config.FONTS['cell_fixed'],
                                   relief='solid',
                                   borderwidth=1)
                    label.grid(row=cell_row, column=cell_col,
                             padx=2, pady=2, ipadx=2, ipady=2)
                    self.cells[(i, j)] = label

        # 创建按钮框架
        button_frame = tk.Frame(main_container)
        button_frame.grid(row=2, column=0, pady=15)

        # 创建难度选择框架
        difficulty_frame = tk.Frame(button_frame)
        difficulty_frame.grid(row=0, column=0, padx=10)

        difficulty_label = tk.Label(difficulty_frame,
                                  text="难度:",
                                  font=config.FONTS['label'])
        difficulty_label.grid(row=0, column=0, padx=5)

        difficulties = ["简单", "中等", "困难"]
        self.difficulty_var = tk.StringVar(self.master)
        self.difficulty_var.set(difficulties[0])
        difficulty_dropdown = tk.OptionMenu(difficulty_frame, 
                                          self.difficulty_var, 
                                          *difficulties)
        difficulty_dropdown.config(font=('Arial', 12))
        difficulty_dropdown.grid(row=0, column=1)

        # 创建按钮
        new_game_button = tk.Button(button_frame,
                                   text="新游戏",
                                   font=config.FONTS['button'],
                                   command=self.start_new_game,
                                   width=10,
                                   relief='raised',
                                    bg=config.COLORS['button_bg'],     # 按钮背景色
                                    fg=config.COLORS['button_fg'])     # 按钮文字颜色
        new_game_button.grid(row=0, column=1, padx=10)

        check_button = tk.Button(button_frame,
                                text="检查",
                                font=config.FONTS['button'],
                                command=self.check_solution,
                                width=10,
                                relief='raised',
                                bg=config.COLORS['button_bg'],     # 按钮背景色
                                fg=config.COLORS['button_fg'])     # 按钮文字颜色
        check_button.grid(row=0, column=2, padx=10)

        # 创建状态框架
        status_frame = tk.Frame(main_container)
        status_frame.grid(row=3, column=0, pady=5)

        # 显示剩余检查次数
        self.check_label = tk.Label(status_frame,
                                   text=f"剩余检查次数: {self.max_checks - self.check_count}",
                                   font=config.FONTS['label'])
        self.check_label.grid(row=0, column=0, padx=10)

        # 创建操作按钮框架
        operation_frame = tk.Frame(main_container)
        operation_frame.grid(row=4, column=0, pady=5)

        # 撤销按钮
        self.undo_button = tk.Button(operation_frame,
                                    text="撤销",
                                    font=config.FONTS['button'],
                                    command=self.undo,
                                    width=8,
                                    bg=config.COLORS['button_bg'],     # 按钮背景色
                                    fg=config.COLORS['button_fg'],  # 按钮文字颜色
                                    state='disabled')
        self.undo_button.grid(row=0, column=0, padx=5)

        # 重做按钮
        self.redo_button = tk.Button(operation_frame,
                                    text="重做",
                                    font=config.FONTS['button'],
                                    command=self.redo,
                                    width=8,
                                    bg=config.COLORS['button_bg'],     # 按钮背景色
                                    fg=config.COLORS['button_fg'],     # 按钮文字颜色
                                    state='disabled')
        self.redo_button.grid(row=0, column=1, padx=5)

        # 保存按钮
        save_button = tk.Button(operation_frame,
                               text="保存",
                               font=('Arial', 12, 'bold'),  # 加粗字体
                               command=self.save_game,
                               width=8,
                               bg=config.COLORS['button_bg'],     # 按钮背景色
                               fg=config.COLORS['button_fg'])     # 按钮文字颜色
        save_button.grid(row=0, column=2, padx=5)

        # 加载按钮
        load_button = tk.Button(operation_frame,
                               text="加载",
                               font=('Arial', 12, 'bold'),  # 加粗字体
                               command=self.load_game,
                               width=8,
                               bg=config.COLORS['button_bg'],     # 按钮背景色
                               fg=config.COLORS['button_fg'])     # 按钮文字颜色
        load_button.grid(row=0, column=3, padx=5)

    def start_new_game(self):
        """开始新游戏的处理函数"""
        self.new_game(self.difficulty_var.get())

    def check_solution(self):
        """检查当前解答是否正确"""
        if self.check_count >= self.max_checks:
            messagebox.showwarning("警告", "已达到最大检查次数！")
            return
        
        self.check_count += 1
        self.check_label.config(text=f"剩余检查次数: {self.max_checks - self.check_count}")
        
        has_error = False  # 错误标志
        # 检查所有可编辑的单元格
        for i in range(9):
            for j in range(9):
                if isinstance(self.cells[(i, j)], tk.Entry):
                    value = self.cells[(i, j)].get()
                    # 检查输入是否有效且正确
                    if value == "" or not value.isdigit() or int(value) != self.solution[i][j]:
                        self.cells[(i, j)].config(bg="red")  # 错误标红
                        has_error = True
                    else:
                        self.cells[(i, j)].config(bg="green")  # 正确标绿
        # 显示相应的消息框
        if has_error:
            messagebox.showerror("错误", "数独未完成或有错误")
        else:
            messagebox.showinfo("成功", "数独已完成，且正确！")
        # 如果用户检查次数超过5次且仍有错误，显示正确答案
        if self.check_count >= 5 and has_error:
            for i in range(9):
                for j in range(9):
                    # 只处理可编辑的单元格
                    if isinstance(self.cells[(i, j)], tk.Entry):
                        value = self.cells[(i, j)].get()
                        # 如果单元格为空或值错误
                        if value == "" or not value.isdigit() or int(value) != self.solution[i][j]:
                            # 清空单元格内容
                            self.cells[(i, j)].delete(0, tk.END)
                            # 插入正确答案
                            self.cells[(i, j)].insert(0, str(self.solution[i][j]))
                            # 将答案显示为蓝色加粗字体
                            self.cells[(i, j)].config(fg="blue", font=('Arial', 20, 'bold'))

    def validate_input(self, event):
        """验证输入是否为1-9的数字"""
        # 允许删除和退格键
        if event.keysym in ['BackSpace', 'Delete']:
            return
        # 只允许输入1-9的数字
        if event.char not in '123456789':
            return "break"
        # 如果已经有数字，阻止输入
        if event.widget.get():
            return "break"
        
        # 在输入前保存当前状态用于撤销
        self.save_state()

    def save_state(self):
        """保存当前状态用于撤销"""
        current_state = {}
        for i in range(9):
            for j in range(9):
                if isinstance(self.cells[(i, j)], tk.Entry):
                    current_state[(i, j)] = self.cells[(i, j)].get()
        
        self.undo_stack.append(current_state)
        self.redo_stack.clear()  # 新的操作会清空重做栈
        self.update_undo_redo_buttons()

    def undo(self):
        """撤销操作"""
        if not self.undo_stack:
            return
        
        # 保存当前状态到重做栈
        current_state = {}
        for i in range(9):
            for j in range(9):
                if isinstance(self.cells[(i, j)], tk.Entry):
                    current_state[(i, j)] = self.cells[(i, j)].get()
        self.redo_stack.append(current_state)
        
        # 恢复上一个状态
        previous_state = self.undo_stack.pop()
        for (i, j), value in previous_state.items():
            if isinstance(self.cells[(i, j)], tk.Entry):
                self.cells[(i, j)].delete(0, tk.END)
                if value:
                    self.cells[(i, j)].insert(0, value)
        
        self.update_undo_redo_buttons()

    def redo(self):
        """重做操作"""
        if not self.redo_stack:
            return
        
        # 保存当前状态到撤销栈
        current_state = {}
        for i in range(9):
            for j in range(9):
                if isinstance(self.cells[(i, j)], tk.Entry):
                    current_state[(i, j)] = self.cells[(i, j)].get()
        self.undo_stack.append(current_state)
        
        # 恢复下一个状态
        next_state = self.redo_stack.pop()
        for (i, j), value in next_state.items():
            if isinstance(self.cells[(i, j)], tk.Entry):
                self.cells[(i, j)].delete(0, tk.END)
                if value:
                    self.cells[(i, j)].insert(0, value)
        
        self.update_undo_redo_buttons()

    def update_undo_redo_buttons(self):
        """更新撤销/重做按钮状态"""
        self.undo_button['state'] = 'normal' if self.undo_stack else 'disabled'
        self.redo_button['state'] = 'normal' if self.redo_stack else 'disabled'

    def save_game(self):
        """保存游戏状态"""
        import json
        import os
        
        game_state = {
            'board': self.board,
            'solution': self.solution,
            'current_state': {},
            'difficulty': self.difficulty_var.get(),
            'check_count': self.check_count
        }
        
        # 保存当前填写的数字
        for i in range(9):
            for j in range(9):
                if isinstance(self.cells[(i, j)], tk.Entry):
                    game_state['current_state'][f"{i},{j}"] = self.cells[(i, j)].get()
        
        # 确保存档目录存在
        if not os.path.exists('saves'):
            os.makedirs('saves')
        
        # 保存到文件
        with open('saves/sudoku_save.json', 'w') as f:
            json.dump(game_state, f)
        
        messagebox.showinfo("保存成功", "游戏已保存")

    def load_game(self):
        """加载游戏状态"""
        import json
        import os
        
        if not os.path.exists('saves/sudoku_save.json'):
            messagebox.showerror("错误", "没有找到存档文件")
            return
        
        try:
            with open('saves/sudoku_save.json', 'r') as f:
                game_state = json.load(f)
            
            self.board = game_state['board']
            self.solution = game_state['solution']
            self.check_count = game_state['check_count']
            
            # 重新创建界面
            self.new_game(game_state['difficulty'])
            
            # 恢复保存的数字
            for pos, value in game_state['current_state'].items():
                i, j = map(int, pos.split(','))
                if isinstance(self.cells[(i, j)], tk.Entry) and value:
                    self.cells[(i, j)].insert(0, value)
            
            messagebox.showinfo("加载成功", "游戏已加载")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载存档失败: {str(e)}")

if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    # 创建数独游戏实例
    sudoku = Sudoku(root)
    # 开始一个简单难度的新游戏
    sudoku.new_game("简单")
    # 进入主循环,等待用户操作
    root.mainloop()
