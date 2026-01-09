# src/views.py
# 日历视图模块：负责生成年/月日历界面，支持农历初一标记

# --- 基础配置 ---
month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# 每月默认天数（非闰年）
month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


# --- 农历函数注入机制 ---
# 外部传入 get_lunar_date 函数（来自 my_lunar）
_get_lunar_date_func = None


def set_lunar_function(get_lunar_fn):
    """
    由 main.py 注入农历查询函数
    示例：views.set_lunar_function(get_lunar_date)
    """
    global _get_lunar_date_func
    _get_lunar_date_func = get_lunar_fn


# --- 工具函数 ---
def is_leap_year(year):
    """判断是否为闰年"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def get_weekday(day, month, year):
    """
    使用基姆拉尔森公式计算星期几
    返回值：0=周日, 1=周一, ..., 6=周六
    """
    if month < 3:
        month += 12
        year -= 1
    w = (day + 2 * month + 3 * (month + 1) // 5 + year + year // 4 - year // 100 + year // 400) % 7
    return w


# --- 单月日历生成 ---
def generate_month_lines(year, month):
    """
    生成指定年月的日历行列表（每行为字符串），用于横向拼接显示
    支持在农历初一日期后添加 *
    """
    global _get_lunar_date_func

    # 确定该月总天数
    days = month_days[month - 1]
    if month == 2 and is_leap_year(year):
        days = 29

    # 构建标题和表头
    title = f"{month_names[month - 1]} {year}"
    header = "Su Mo Tu We Th Fr Sa"
    lines = []
    lines.append(f"{title:^27}")  # 居中标题
    lines.append(header)

    # 计算每月1号是星期几
    first_weekday = get_weekday(1, month, year)
    current_line = "   " * first_weekday  # 前导空格对齐星期

    # 逐日绘制
    for day in range(1, days + 1):
        # 判断是否为农历初一
        is_lunar_first_day = False
        if _get_lunar_date_func is not None:
            try:
                lunar_str = _get_lunar_date_func(year, month, day)
                if isinstance(lunar_str, str) and "初一" in lunar_str:
                    is_lunar_first_day = True
            except Exception as e:
                # 安全降级：出错就不标星号
                pass

        # 添加日期 + 星号（如果需要）
        if is_lunar_first_day:
            current_line += f"{day:2}*"
        else:
            current_line += f"{day:3}"

        # 每周结束换行（注意：周日是 (first_weekday + day) % 7 == 0）
        if (first_weekday + day) % 7 == 0:
            lines.append(current_line)
            current_line = ""

    # 添加最后一行未完成的部分
    if current_line:
        lines.append(current_line)

    # 补足到8行，保持三列对齐美观
    while len(lines) < 8:
        lines.append("")

    return lines


# --- 年视图显示 ---
def display_year_view(year):
    """
    显示某一年的全年12个月日历（三列排版）
    """
    print(f"==================== {year} 年日历（年视图） ====================")
    print("注：* 标记为农历初一\n")

    # 预生成所有月份的行数据
    all_months = [generate_month_lines(year, m) for m in range(1, 13)]

    # 每次输出3个月（共4行）
    for row_start in range(0, 12, 3):
        months_in_row = all_months[row_start:row_start + 3]
        # 不够三个补空行
        while len(months_in_row) < 3:
            months_in_row.append([""] * 8)

        # 拼接每一行的高度（最多8行）
        for i in range(8):
            line = ""
            for j, m_lines in enumerate(months_in_row):
                if j > 0:
                    line += "    "  # 中间留空隙
                part = m_lines[i] if i < len(m_lines) else ""
                line += f"{part:27}"  # 固定宽度，保证对齐
            print(line)
        print()  # 季度之间空一行


# --- 月视图显示（简洁版）---
def display_month_view(year, month):
    """
    显示单个月份的日历（用于月视图模式）
    """
    global _get_lunar_date_func

    days = month_days[month - 1]
    if month == 2 and is_leap_year(year):
        days = 29

    print(f"        {month_names[month - 1]} {year}        ")
    print("Su Mo Tu We Th Fr Sa")

    first_weekday = get_weekday(1, month, year)
    print("   " * first_weekday, end="")

    for day in range(1, days + 1):
        is_lunar_first = False
        if _get_lunar_date_func is not None:
            try:
                lunar_str = _get_lunar_date_func(year, month, day)
                if isinstance(lunar_str, str) and "初一" in lunar_str:
                    is_lunar_first = True
            except:
                pass

        if is_lunar_first:
            print(f"{day:2}*", end="")
        else:
            print(f"{day:3}", end="")

        if (first_weekday + day) % 7 == 0:
            print()  # 换行

    if (first_weekday + day) % 7 != 0:
        print()  # 最后补换行

    print("-------------------------")
