# 年视图模块（杨雨晨负责）
import

os
import

sys

# 月份名称
month_names
= ["January", "February", "March", "April", "May", "June",
   "July", "August", "September", "October", "November", "December"]

# 每月天数（非闰年）
month_days
= [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


# 判断闰年
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


# 计算某日期是星期几（基姆拉尔森公式，返回0=周日，1=周一...6=周六）
def get_weekday(day, month, year):
    if month < 3:
        month

+= 12
year
-= 1
w
= (day + 2 * month + 3 * (month + 1) // 5 + year + year // 4 - year // 100 + year // 400) % 7
return w  # 0=周日，1=周一，...，6=周六


# 显示单个月份的简洁日历（年视图专用，仅公历+农历初一标注）
def print_month_year_view(year, month, flag):
    days

= month_days[month - 1]
# 闰年处理2月
if month == 2 and is_leap_year(year):
    days
= 29

# 打印月份标题
print(f"        {month_names[month - 1]} {year}        ", end="")

# 计算当月1号的星期
first_weekday
= get_weekday(1, month, year)

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


# 显示详细月视图（包含农历和节假日）
def print_month_detail_view(year, month):
    days

= month_days[month - 1]
# 闰年处理2月
if month == 2 and is_leap_year(year):
    days
= 29

# 计算当月1号的星期
first_weekday
= get_weekday(1, month, year)

# 月份中文名称（用于月视图）
month_names_cn
= ["一月", "二月", "三月", "四月", "五月", "六月",
   "七月", "八月", "九月", "十月", "十一月", "十二月"]

# 星期中文名称
weekdays_cn
= ["日", "一", "二", "三", "四", "五", "六"]

# 清屏并打印月视图标题
os
.system('cls' if os.name == 'nt' else 'clear')
print("=" * 50)
print(f"{' ' * 20}{year}年{month_names_cn[month - 1]}{' ' * 20}")
print("=" * 50)
print()

# 打印星期标题
print(" " * 4 + "  ".join(weekdays_cn))
print("  " + "-" * 35)

# 初始化日期网格
day_grid
= [["  " for _ in range(7)] for _ in range(6)]

# 填充日期网格
current_day
= 1
for week in range(6):
    for weekday in range(7):
        if (week == 0 and weekday < first_weekday) or current_day > days:
            continue
        day_grid
[week][weekday] = f"{current_day:2}"
current_day
+= 1

# 打印日期网格（添加农历和节假日标记）
for week in range(6):
    line
= "  "
for weekday in range(7):
    day_str
= day_grid[week][weekday]

# 添加特殊标记
if day_str.strip() != "":
    day_num
= int(day_str)
# 标记周末
if weekday == 0 or weekday == 6:
    day_str
= f"\033[91m{day_str}\033[0m"  # 红色

# 标记农历初一（模拟数据）
if day_num == 1:
    day_str
= f"{day_str}*"

# 标记节假日（模拟几个主要节日）
if month == 1 and day_num == 1:
    day_str
= f"{day_str}元旦"
elif month == 5 and day_num == 1:
day_str
= f"{day_str}劳动"
elif month == 10 and day_num == 1:
day_str
= f"{day_str}国庆"

line
+= day_str + "  "
print(line)

# 在每行日期下面打印农历信息（简化版）
if week < 5:
    lunar_line
= "  "
for weekday in range(7):
    day_str
= day_grid[week][weekday]
if day_str.strip() != "":
    day_num
= int(day_str)
# 模拟农历显示（实际需要农历计算库）
if day_num == 1:
    lunar_line
+= "初一  "
else:
lunar_line
+= f"{day_num - 1:2}   "
else:
lunar_line
+= "     "
print(lunar_line)

print("\n" + "=" * 50)
print("说明：*表示农历初一，红色日期为周末")
print("=" * 50)


# 年视图显示函数：一次性展示12个月
def show_year_view(year):
    os

.system('cls' if os.name == 'nt' else 'clear')  # Windows清屏，Linux/Mac替换为clear
print(f"==================== {year} 年日历（年视图） ====================")
print("注：* 标记为农历初一\n")

flag
= 0
# 按3列一行显示12个月（更紧凑的布局）
for i in range(0, 12, 3):
    flag
= print_month_year_view(year, i + 1, flag)
if i + 2 <= 11:
    flag
= print_month_year_view(year, i + 2, flag)
if i + 3 <= 11:
    flag
= print_month_year_view(year, i + 3, flag)
print("\n\n")


# 月视图显示函数：显示指定月份的详细日历
def show_month_view(year, month):
    print_month_detail_view


(year, month)


# 视图切换主函数
def main():
    year

= int(input("请输入要查看的年份："))

# 显示年视图
show_year_view
(year)

while True:
    print("\n" + "=" * 50)
    print("日历视图选项：")
    print("1. 查看年视图")
    print("2. 查看月视图")
    print("3. 切换年份")
    print("4. 退出")
    print("=" * 50)

    choice
= input("请选择操作（1-4）：").strip()

if choice == "1":
    # 显示年视图
    show_year_view
(year)

elif choice == "2":
# 显示月视图
month
= int(input(f"请输入要查看的月份（1-12，当前年份：{year}）："))
if 1 <= month <= 12:
    show_month_view
(year, month)
else:
print("月份输入错误，请输入1-12之间的数字！")

elif choice == "3":
# 切换年份
year
= int(input("请输入新的年份："))
show_year_view
(year)

elif choice == "4":
print("感谢使用日历程序，再见！")
break

else:
print("无效的选择，请重新输入！")

if __name__ == "__main__":
    main
()