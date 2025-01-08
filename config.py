"""UI配置文件：存储所有界面相关的配置参数"""

# 窗口配置：控制主窗口的基本属性
WINDOW = {
    'title': '数独游戏',      # 窗口标题
    'min_width': 500,        # 窗口最小宽度
    'min_height': 600,       # 窗口最小高度
    'padding': 20           # 窗口内边距，控制内容与窗口边缘的距离
}

# 字体配置：定义界面中不同元素使用的字体
FONTS = {
    'title': ('Arial', 24, 'bold'),     # 游戏标题字体
    'cell': ('Arial', 22),              # 数独格子中可编辑数字的字体
    'cell_fixed': ('Arial', 22, 'bold'), # 数独格子中固定数字的字体（加粗）
    'button': ('Arial', 12, 'bold'),     # 按钮文字字体
    'label': ('Arial', 12)              # 普通标签文字字体
}

# 颜色配置：定义界面中各元素的颜色
COLORS = {
    'bg_default': 'systemWindowBody',  # 默认背景色（使用系统默认）
    'bg_highlight': '#e0e8ff',        # 输入框获得焦点时的高亮背景色
    'bg_error': 'red',                # 错误提示的背景色
    'bg_correct': 'green',            # 正确提示的背景色
    'bg_hint': 'blue',                # 提示数字的背景色
    'fg_default': 'black',            # 默认文字颜色
    'fg_fixed': 'black',              # 固定数字的文字颜色
    'fg_hint': 'blue',                # 提示数字的文字颜色
    'button_bg': 'white',             # 按钮背景色
    'button_fg': 'black'              # 按钮文字颜色
}

# 网格配置：控制数独网格的视觉效果
GRID = {
    'border_width': 2,     # 网格边框宽度
    'cell_width': 2,       # 单元格宽度（以字符为单位）
    'cell_padding': 2,     # 单元格内边距
    'relief': 'solid'      # 边框样式（实线）
}

# 按钮配置：控制按钮的视觉效果和布局
BUTTONS = {
    'width': {
        'normal': 8,       # 普通按钮宽度
        'wide': 10         # 宽按钮宽度（用于主要功能按钮）
    },
    'padding': 5,          # 按钮之间的间距
    'relief': 'raised'     # 按钮边框样式（凸起）
}

# 游戏配置：控制游戏的核心参数
GAME = {
    'max_checks': 5,       # 最大检查次数，超过后会显示答案
    'difficulties': {      # 难度设置，数字表示要移除的数字数量
        '简单': 10,        # 简单模式：移除10个数字
        '中等': 25,        # 中等模式：移除25个数字
        '困难': 40         # 困难模式：移除40个数字
    }
} 