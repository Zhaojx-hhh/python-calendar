# 年视图模块（杨雨晨负责） 
import os
import sys

# 月份名称
month_names = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

# 每月天数（非闰年）
month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# 判断闰年
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# 基姆拉尔森计算星期几（返回 0=周日, 1=周一...6=周六）
def get_weekday(day, month, year):
    if month < 3:
        month += 12
        year -= 1
    w = (day + 2 * month + 3 * (month + 1) // 5 + year + year // 4 - year // 100 + year // 400) % 7
    return w

# 构建单个月份的日历为字符串列表（每行一个字符串），便于横向拼接
def generate_month_lines(year, month):
    days = month_days[month - 1]
    if month == 2 and is_leap_year(year):
        days = 29

    # 标题行
    title = f"{month_names[month - 1]} {year}"
    header = "Su Mo Tu We Th Fr Sa"
    lines = []
    lines.append(f"{title:^27}")
    lines.append(header)

    # 获取1号是星期几
    first_weekday = get_weekday(1, month, year)
    current_line = ""

    # 前导空格
    for _ in range(first_weekday):
        current_line += "   "

    # 添加日期
    for day in range(1, days + 1):
        if day == 1:
            current_line += f"{day:2}*"
        else:
            current_line += f"{day:3}"
        # 每7列换行
        if (first_weekday + day) % 7 == 0:
            lines.append(current_line)
            current_line = ""

    # 最后一行补全
    if current_line:
        lines.append(current_line)

    # 补足空白行到6行日历内容（方便对齐）
    while len(lines) < 8:  # 标题+header+最多6周 = 8行
        lines.append(" " * 27)

    return lines

# 显示年视图（3列并排）
def show_year_view(year):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"==================== {year} 年日历（年视图） ====================")
    print("注：* 标记为农历初一\n")

    all_months = []
    for m in range(1, 13):
        all_months.append(generate_month_lines(year, m))

    # 每次取3个月进行横向拼接
    for row_start in range(0, 12, 3):
        months_in_row = all_months[row_start:row_start + 3]

        # 确保总是3个日历（最后一个不够补空）
        while len(months_in_row) < 3:
            months_in_row.append([""] * 8)

        # 逐行合并三个日历
        for i in range(8):  # 每个日历最多8行
            line_combined = ""
            for j, m_lines in enumerate(months_in_row):
                if j > 0:
                    line_combined += "    "  # 间隔4个空格
                line_combined += f"{m_lines[i]:27}"  # 固定宽度对齐
            print(line_combined)

        print()  # 行间空行

# 主函数
def main():
    try:
        year = int(input("请输入要查看的年份："))
    except ValueError:
        print("请输入有效的年份！")
        return

    show_year_view(year)
    input("\n按任意键退出...")

if __name__ == "__main__":
    main()
