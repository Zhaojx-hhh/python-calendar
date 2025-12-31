# 月视图模块（王康骏负责） 
import calendar

calendar
from datetime import datetime


def print_month_calendar(year=None, month=None):
    """
    打印指定年月的基础月视图日历
    """
    # 参数验证
    if year is None or month is None:
        now = datetime.now()
        year, month = now.year, now.month
    else:
        # 确保参数是整数
        try:
            year= int(year)
            month= int(month)
        except ValueError:
             print("错误：年份和月份必须是数字")
             return

# 验证月份范围
    if month < 1 or month > 12:
        print(f"错误：月份必须在1-12之间，当前输入：{month}")
        return

    # 验证年份范围（示例：限制在1900-2100之间）
    if year < 1900 or year > 2100:
        print(f"警告：年份{year}可能超出有效范围")

    try:
        # 创建日历对象
        cal= calendar.TextCalendar(calendar.SUNDAY)  # 从周日开始

        # 打印月视图
        print(f"\n{'=' * 30}")
        print(f"      {calendar.month_name[month]} {year}")
        print(f"{'=' * 30}")
        print(cal.formatmonth(year, month))
        print(f"{'=' * 30}")
    except Exception as e:
        print(f"生成日历时发生错误：{e}")






