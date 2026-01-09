# src/views.py

# 月份名称（英文）
month_names = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

# 每月天数（非闰年）
month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# 判断是否为闰年
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# 基姆拉尔森计算星期几（返回 0=周日, 1=周一...6=周六）
def get_weekday(day, month, year):
    if month < 3:
        month += 12
        year -= 1
    w = (day + 2 * month + 3 * (month + 1) // 5 + year + year // 4 - year // 100 + year // 400) % 7
    return w

# 构建单个月的日历行列表（用于横向拼接）
def generate_month_lines(year, month):
    days = month_days[month - 1]
    if month == 2 and is_leap_year(year):
        days = 29

    title = f"{month_names[month - 1]} {year}"
    header = "Su Mo Tu We Th Fr Sa"
    lines = []
    lines.append(f"{title:^27}")  # 居中标题
    lines.append(header)

    first_weekday = get_weekday(1, month, year)
    current_line = "   " * first_weekday  # 前导空格

    for day in range(1, days + 1):
        if day == 1:
            current_line += f"{day:2}*"  # 农历初一标记
        else:
            current_line += f"{day:3}"
        if (first_weekday + day) % 7 == 0:  # 满一周就换行
            lines.append(current_line)
            current_line = ""

    if current_line:
        lines.append(current_line)

    # 补足空白行到8行，保持对齐
    while len(lines) < 8:
        lines.append("")

    return lines

# 显示年视图（三列排版）
def display_year_view(year):
    print(f"==================== {year} 年日历（年视图） ====================")
    print("注：* 标记为农历初一\n")

    all_months = [generate_month_lines(year, m) for m in range(1, 13)]

    for row_start in range(0, 12, 3):  # 每次取3个月
        months_in_row = all_months[row_start:row_start + 3]
        while len(months_in_row) < 3:
            months_in_row.append([""] * 8)  # 不够补空

        for i in range(8):  # 每个日历最多8行
            line = ""
            for j, m_lines in enumerate(months_in_row):
                if j > 0:
                    line += "    "  # 中间加空隙
                part = m_lines[i] if i < len(m_lines) else ""
                line += f"{part:27}"  # 固定宽度
            print(line)
        print()  # 季度之间空一行

# 显示月视图（简洁版）
def display_month_view(year, month):
    days = month_days[month - 1]
    if month == 2 and is_leap_year(year):
        days = 29

    print(f"        {month_names[month - 1]} {year}        ")
    print("Su Mo Tu We Th Fr Sa")

    first_weekday = get_weekday(1, month, year)
    print("   " * first_weekday, end="")

    for day in range(1, days + 1):
        if day == 1:
            print(f"{day:2}*", end="")
        else:
            print(f"{day:3}", end="")
        if (first_weekday + day) % 7 == 0:
            print()
    print("\n-------------------------")
