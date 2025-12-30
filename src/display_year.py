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


# 计算某日期是星期几（基姆拉尔森公式，返回0=周日，1=周一...6=周六）
def get_weekday(day, month, year):
    if month < 3:
        month += 12
        year -= 1
    w = (day + 2 * month + 3 * (month + 1) // 5 + year + year // 4 - year // 100 + year // 400) % 7
    return w  # 0=周日，1=周一，...，6=周六


# 显示单个月份的简洁日历（年视图专用，仅公历+农历初一标注）
def print_month(year, month, flag):
    days = month_days[month - 1]
    # 闰年处理2月
    if month == 2 and is_leap_year(year):
        days = 29

    # 打印月份标题
    print(f"        {month_names[month - 1]} {year}        ", end="")

    # 计算当月1号的星期
    first_weekday = get_weekday(1, month, year)

    # 换行显示星期头（简洁版：Su Mo Tu We Th Fr Sa）
    if flag % 3 == 0:
        print("\nSu Mo Tu We Th Fr Sa", end="")

    print()

    # 打印前置空格
    for i in range(first_weekday):
        print("   ", end="")

    # 打印日期（标注农历初一）
    for day in range(1, days + 1):
        if day == 1:
            print(f"{day:2}*", end="")  # * 标记农历初一
        else:
            print(f"{day:3}", end="")

        # 每周换行
        if (first_weekday + day) % 7 == 0:
            print()

    # 补全最后一行空格
    if (first_weekday + days) % 7 != 0:
        print()

    print("-------------------------")
    return flag + 1


# 年视图显示函数：一次性展示12个月
def show_year_view(year):
    os.system('cls' if os.name == 'nt' else 'clear')  # Windows清屏，Linux/Mac替换为clear
    print(f"==================== {year} 年日历（年视图） ====================")
    print("注：* 标记为农历初一\n")

    flag = 0
    # 按3列一行显示12个月（更紧凑的布局）
    for i in range(0, 12, 3):
        flag = print_month(year, i + 1, flag)
        if i + 2 <= 11:
            flag = print_month(year, i + 2, flag)
        if i + 3 <= 11:
            flag = print_month(year, i + 3, flag)
        print("\n\n")


# 视图切换测试主函数
def main():
    year = int(input("请输入要查看的年份："))

    # 调用年视图
    show_year_view(year)

    # 扩展：可在此处添加视图切换逻辑（如输入指令切换月视图/年视图）
    input("按任意键退出...")


if __name__ == "__main__":
    main()