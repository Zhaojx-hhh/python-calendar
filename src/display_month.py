import calendar
from datetime import datetime


def print_aligned_calendar(year=None, month=None):
    """
    打印对齐的月视图日历
    """
    if year is None or month is None:
        now = datetime.now()
        year, month = now.year, now.month

    # 验证月份
    if month < 1 or month > 12:
        print(f"错误：月份必须在1-12之间")
        return

    # 创建日历对象
    cal = calendar.Calendar(calendar.SUNDAY)
    month_days = cal.monthdayscalendar(year, month)

    # 设置单元格宽度
    cell_width = 4  # 每个单元格4个字符宽度

    # 星期标题（英文缩写）
    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    # 打印月份标题
    title = f"{calendar.month_name[month]} {year}"
    print(f"\n{'=' * (len(weekdays) * cell_width)}")
    print(title.center(len(weekdays) * cell_width))
    print(f"{'=' * (len(weekdays) * cell_width)}")

    # 打印星期标题（居中对齐）
    for wd in weekdays:
        print(f"{wd:^{cell_width}}", end="")
    print()
    print("-" * (len(weekdays) * cell_width))

    # 打印日期（每个日期居中对齐）
    for week in month_days:
        for day in week:
            if day == 0:
                # 空日期
                print(f"{'':^{cell_width}}", end="")
            else:
                # 如果是今天，特殊标记
                now = datetime.now()
                if year == now.year and month == now.month and day == now.day:
                    print(f"{f'[{day}]':^{cell_width}}", end="")
                else:
                    print(f"{day:^{cell_width}d}", end="")
        print()  # 换行

    print(f"{'=' * (len(weekdays) * cell_width)}")


def print_chinese_aligned_calendar(year=None, month=None):
    """
    打印对齐的中文月视图日历
    """
    if year is None or month is None:
        now = datetime.now()
        year, month = now.year, now.month

    # 中文月份名称
    chinese_months = {
        1: "一月", 2: "二月", 3: "三月", 4: "四月",
        5: "五月", 6: "六月", 7: "七月", 8: "八月",
        9: "九月", 10: "十月", 11: "十一月", 12: "十二月"
    }

    # 中文星期（每个占2字符）
    chinese_weekdays = ["日", "一", "二", "三", "四", "五", "六"]

    # 创建日历对象
    cal = calendar.Calendar(calendar.SUNDAY)
    month_days = cal.monthdayscalendar(year, month)

    # 单元格宽度（中文需要更大宽度）
    cell_width = 6  # 每个单元格6个字符宽度

    # 打印标题
    title = f"{year}年 {chinese_months[month]}"
    print(f"\n{'=' * (len(chinese_weekdays) * cell_width)}")
    print(title.center(len(chinese_weekdays) * cell_width))
    print(f"{'=' * (len(chinese_weekdays) * cell_width)}")

    # 打印星期标题
    for wd in chinese_weekdays:
        print(f"星期{wd}".center(cell_width), end="")
    print()
    print("-" * (len(chinese_weekdays) * cell_width))

    # 打印日期
    for week in month_days:
        for day in week:
            if day == 0:
                print(f"{'':^{cell_width}}", end="")
            else:
                now = datetime.now()
                if year == now.year and month == now.month and day == now.day:
                    print(f"{f'[{day}]':^{cell_width}}", end="")
                else:
                    print(f"{day:^{cell_width}d}", end="")
        print()

    print(f"{'=' * (len(chinese_weekdays) * cell_width)}")


# 测试
if __name__ == "__main__":
    print("英文对齐月视图:")
    print_aligned_calendar(2024, 3)

    print("\n\n中文对齐月视图:")
    print_chinese_aligned_calendar(2024, 3)




