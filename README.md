# SudokuGame

## 项目简介
这是一个用Python实现的数独游戏，包含生成数独谜题和解题功能。项目使用tkinter实现图形界面，支持多种难度选择、撤销/重做操作、游戏保存/加载等功能。

## 核心算法

### 数独生成算法
1. 使用优化的回溯算法生成完整数独棋盘
2. 首先填充对角线上的3个3x3方格，这些方格互不影响
3. 使用随机打乱的数字顺序填充，确保每次生成的棋盘不同
4. 采用最小可能性优先策略，显著减少回溯次数

### 数独填充算法
1. 使用优化的回溯算法填充剩余格子
2. 优先填充可能性最少的位置，减少无效尝试
3. 提前计算有效数字，避免重复验证
4. 如果填充失败，重新生成整个棋盘

### 唯一解验证
1. 在移除数字创建谜题时，确保生成的数独有唯一解
2. 使用改进的递归算法验证解的唯一性
3. 如果移除某个数字导致多解，则恢复该数字

## 运行方法
1. 确保已安装Python 3.x
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行游戏：
   ```bash
   python sudoku.py
   ```

## 项目结构
- `sudoku.py`: 主程序文件，包含游戏逻辑和UI实现
- `config.py`: 配置文件，包含窗口设置、颜色配置等

---

# SudokuGame (English Version)

## Project Overview
This is a Sudoku game implemented in Python, featuring puzzle generation and solving capabilities. The project uses tkinter for the graphical interface and supports multiple difficulty levels, undo/redo operations, game save/load functionality, and more.

## Core Algorithms

### Sudoku Generation Algorithm
1. Uses an optimized backtracking algorithm to generate complete Sudoku boards
2. First fills the 3 diagonal 3x3 subgrids, which are independent of each other
3. Uses randomly shuffled numbers to ensure unique board generation each time
4. Employs a minimum-possibility-first strategy to significantly reduce backtracking

### Sudoku Filling Algorithm
1. Uses an optimized backtracking algorithm to fill remaining cells
2. Prioritizes cells with the fewest possible numbers to reduce invalid attempts
3. Pre-calculates valid numbers to avoid redundant validation
4. Restarts the entire board generation if filling fails

### Unique Solution Verification
1. Ensures generated puzzles have a unique solution when removing numbers
2. Uses an improved recursive algorithm to verify solution uniqueness
3. Restores removed numbers if they lead to multiple solutions

## Running the Game
1. Ensure Python 3.x is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python sudoku.py
   ```

## Project Structure
- `sudoku.py`: Main program file containing game logic and UI implementation
- `config.py`: Configuration file containing window settings, color schemes, etc.