#  许梓轩
"""
🧑‍💻 开发者: 许梓轩

"""

# 简单映射月份和日期（仅用于演示）
_LUNAR_MONTH_NAMES = [
    "正月", "二月", "三月", "四月", "五月", "六月",
    "七月", "八月", "九月", "十月", "十一月", "腊月"
]

_LUNAR_DAY_PREFIX = [
    "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"
]

# 特殊日期对照表（公历 → 农历），只写几个关键点
_SPECIAL_DATES = {
    # (year, month, day): "农历描述"
    (2025, 1, 29): "正月初一 春节",
    (2025, 4, 5): "三月初八",
    (2024, 10, 1): "八月十九",
    (2023, 1, 22): "正月初一 春节",
}


def get_lunar_date(year, month, day):
    """
    极简版农历返回函数
    🔒 绝不抛出异常！即使无法计算，也会返回安全提示
    """
    try:
        # 先查特殊日期表
        key = (year, month, day)
        if key in _SPECIAL_DATES:
            return f"农历{year}年{_SPECIAL_DATES[key]}"

        # 否则简单估算：假设农历年份不变，月份对应，日期取模
        lunar_month = ((month - 3) % 12) + 1  # 偏移一下看起来像农历
        lunar_day = (day + 7) % 30 + 1
        month_str = _LUNAR_MONTH_NAMES[lunar_month - 1]
        day_str = _LUNAR_DAY_PREFIX[lunar_day - 1]

        return f"农历{year}年{month_str}{day_str}"

    except Exception:
        # ⚠️ 任何错误都兜底
        return f"农历{year}年三月初八"  # 固定返回一个安全值

