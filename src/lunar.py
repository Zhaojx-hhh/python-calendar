# 农历计算模块（许梓轩负责）
# 导入lunarcalendar库的核心类和函数（适配0.0.9版本）
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
from lunarcalendar import SOLAR_TERMS, MONTHS, LUNAR_MONTHS


def get_lunar_date(year, month, day):
    """
    公历转农历核心函数
    :param year: 公历年（如2025）
    :param month: 公历月（1-12）
    :param day: 公历日（1-31）
    :return: 农历日期/节气字符串（如"腊月初五"、"冬至"）
    """
    try:
        # 构建公历日期对象
        solar_date = Solar(year, month, day)

        # 第一步：判断当天是否为节气，若是直接返回节气名称
        for term_index, term_name in enumerate(SOLAR_TERMS):
            # 获取该节气在当年的公历日期
            term_solar = Converter.Term2Solar(year, term_index)
            if solar_date == term_solar:
                return term_name

        # 第二步：非节气则转换为农历日期
        lunar_date = Converter.Solar2Lunar(solar_date)

        # 处理闰月
        if lunar_date.isleap:
            lunar_month_name = f"闰{LUNAR_MONTHS[lunar_date.month - 1]}"
        else:
            lunar_month_name = LUNAR_MONTHS[lunar_date.month - 1]

        # 农历日期名称映射（初一到三十）
        lunar_day_names = [
            "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
            "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
            "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"
        ]
        lunar_day_name = lunar_day_names[lunar_date.day - 1]

        # 拼接农历日期字符串
        return f"{lunar_month_name}{lunar_day_name}"

    except DateNotExist:
        # 处理无效日期（如2月30日）
        return "日期无效"


def get_month_lunar_dates(year, month):
    """
    批量获取指定公历月份的所有农历信息（配合显示模块）
    :param year: 公历年
    :param month: 公历月
    :return: 字典，key为公历日（1-31），value为农历/节气字符串
    """
    lunar_month_dict = {}
    # 先判断当月天数
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2:
        # 闰年2月29天
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            days = 29
        else:
            days = 28
    else:
        days = month_days[month - 1]

    # 遍历当月每一天，获取农历信息
    for day in range(1, days + 1):
        lunar_month_dict[day] = get_lunar_date(year, month, day)

    return lunar_month_dict


# 测试代码（验证功能是否正常）
if __name__ == "__main__":
    # 测试单日期转换
    print("2024年12月21日：", get_lunar_date(2024, 12, 21))  # 应输出“冬至”
    print("2025年1月29日：", get_lunar_date(2025, 1, 29))  # 应输出农历日期（如“正月初二”）
    print("2025年2月30日：", get_lunar_date(2025, 2, 30))  # 应输出“日期无效”

    # 测试批量获取整月农历信息
    print("\n2025年1月农历信息：")
    jan_2025_lunar = get_month_lunar_dates(2025, 1)
    for day, lunar_info in jan_2025_lunar.items():
        print(f"1月{day}日：{lunar_info}")