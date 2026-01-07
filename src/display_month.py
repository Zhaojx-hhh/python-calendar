import calendar
from datetime import datetime


def print_month_calendar(year=None, month=None, start_day=calendar.SUNDAY):
    """
    打印指定年月的基础月视图日历

    Parameters:
        year: 年份，默认为当前年份
        month: 月份，默认为当前月份
        start_day: 周起始日，默认周日开始
    """
    # 参数验证
    if year is None or month is None:
        now = datetime.now()
        year, month = now.year, now.month

    # 验证月份范围
    if month < 1 or month > 12:
        print(f"错误：月份必须在1-12之间，当前输入：{month}")
        return

    # 创建日历对象
    cal = calendar.TextCalendar(start_day)

    # 获取月视图文本
    month_text = cal.formatmonth(year, month)

    # 修复对齐问题
    lines = month_text.strip().split('\n')

    # 提取标题行
    title_line = lines[0]

    # 修复星期标题行
    if len(lines) > 1:
        # 保持原有的星期标题
        week_header = lines[1]

        # 获取日期行并修复对齐
        date_lines = []
        for i in range(2, len(lines)):
            line = lines[i]
            # 修复数字对齐问题
            if line.strip():  # 跳过空行
                # 将多个空格替换为固定宽度的空格
                date_lines.append(' '.join([f"{cell:>2}" for cell in line.split()]))
            else:
                date_lines.append("")

    # 重新构建月视图
    print(f"\n{'=' * 30}")
    print(f"      {calendar.month_name[month]} {year}")
    print(f"{'=' * 30}")

    # 打印修复后的内容
    print(title_line)
    if len(lines) > 1:
        print(week_header)
        print('-' * 30)
        for line in date_lines:
            print(line)

    print(f"{'=' * 30}")


def print_custom_month_calendar(year=None, month=None):
    """
    自定义月视图日历，解决对齐问题
    """
    # 参数验证
    if year is None or month is None:
        now = datetime.now()
        year, month = now.year, now.month

    # 验证月份范围
    if month < 1 or month > 12:
        print(f"错误：月份必须在1-12之间，当前输入：{month}")
        return

    # 创建日历对象（从周日开始）
    cal = calendar.Calendar(calendar.SUNDAY)

    # 获取该月的日期矩阵
    month_days = cal.monthdayscalendar(year, month)

    # 星期标题
    weekdays = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]

    # 打印日历
    print(f"\n{'=' * 30}")
    print(f"      {calendar.month_name[month]} {year}")
    print(f"{'=' * 30}")

    # 打印星期标题
    print(" ".join(f"{day:>2}" for day in weekdays))
    print("-" * 30)

    # 打印日期
    for week in month_days:
        week_str = []
        for day in week:
            if day == 0:
                week_str.append("  ")
            else:
                week_str.append(f"{day:2d}")
        print(" ".join(week_str))

    print(f"{'=' * 30}")


def print_pretty_month_calendar(year=None, month=None):
    """
    美观的月视图日历，带中文支持
    """
    # 参数验证
    if year is None or month is None:
        now = datetime.now()
        year, month = now.year, now.month

    # 验证月份范围
    if month < 1 or month > 12:
        print(f"错误：月份必须在1-12之间，当前输入：{month}")
        return

    # 中文月份名称
    chinese_months = {
        1: "一月", 2: "二月", 3: "三月", 4: "四月",
        5: "五月", 6: "六月", 7: "七月", 8: "八月",
        9: "九月", 10: "十月", 11: "十一月", 12: "十二月"
    }

    # 中文星期
    chinese_weekdays = ["日", "一", "二", "三", "四", "五", "六"]

    # 创建日历对象（从周日开始）
    cal = calendar.Calendar(calendar.SUNDAY)

    # 获取该月的日期矩阵
    month_days = cal.monthdayscalendar(year, month)

    # 打印日历
    print(f"\n{'=' * 40}")
    print(f"          {year}年 {chinese_months[month]}")
    print(f"{'=' * 40}")

    # 打印星期标题
    print("  " + "  ".join(f"{day:^3}" for day in chinese_weekdays))
    print("-" * 40)

    # 打印日期
    for week in month_days:
        week_str = []
        for day in week:
            if day == 0:
                week_str.append("    ")
            else:
                # 如果是当前日期，用特殊标记
                now = datetime.now()
                if year == now.year and month == now.month and day == now.day:
                    week_str.append(f"[{day:2d}]")
                else:
                    week_str.append(f" {day:2d} ")
        print("".join(week_str))

    print(f"{'=' * 40}")


# 测试函数
if __name__ == "__main__":
    print("方法1: 使用calendar库的formatmonth方法（有问题）")
    print_month_calendar(2024, 3)

    print("\n方法2: 自定义月视图（修复对齐）")
    print_custom_month_calendar(2024, 3)

    print("\n方法3: 美观的中文月视图")
    print_pretty_month_calendar(2024, 3)

    print("\n方法4: 打印当前月份")
    print_pretty_month_calendar()






