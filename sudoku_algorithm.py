import random
import config

class SudokuAlgorithm:
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