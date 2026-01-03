# 公历计算模块（陈一帆负责） 
import datetime

class SolarCalendar:
    """公历日历计算类"""
    
    # 月份名称
    MONTH_NAMES = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    # 星期名称（周日开头）
    WEEKDAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    
    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        判断是否为闰年
        
        参数:
            year: 年份
            
        返回:
            bool: 是闰年返回True，否则返回False
            
        规则:
            1. 能被4整除但不能被100整除的是闰年
            2. 能被400整除的是闰年
        """
        if year < 1:
            raise ValueError("年份必须为正整数")
        
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    @staticmethod
    def get_month_days(year: int, month: int) -> int:
        """
        获取指定年月的天数
        
        参数:
            year: 年份
            month: 月份（1-12）
            
        返回:
            int: 该月的天数
            
        异常:
            ValueError: 月份不在1-12范围内
        """
        if not 1 <= month <= 12:
            raise ValueError("月份必须在1-12之间")
        
        # 各月份天数（非闰年2月为28天）
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # 如果是闰年且是2月
        if month == 2 and SolarCalendar.is_leap_year(year):
            return 29
        
        return month_days[month - 1]
    
    @staticmethod
    def get_weekday(year: int, month: int, day: int) -> int:
        """
        计算指定日期是星期几（蔡勒公式）
        
        参数:
            year: 年份（支持任意年份）
            month: 月份（1-12）
            day: 日期
            
        返回:
            int: 星期几（0=周日，1=周一，...，6=周六）
            
        异常:
            ValueError: 日期无效
        """
        # 验证日期有效性
        if month < 1 or month > 12:
            raise ValueError("月份必须在1-12之间")
        
        max_days = SolarCalendar.get_month_days(year, month)
        if day < 1 or day > max_days:
            raise ValueError(f"日期必须在1-{max_days}之间")
        
        # 蔡勒公式（Zeller's congruence）
        if month < 3:
            month += 12
            year -= 1
        
        century = year // 100
        year_of_century = year % 100
        
        # 蔡勒公式计算
        h = (day + (13 * (month + 1)) // 5 + year_of_century + 
             year_of_century // 4 + century // 4 - 2 * century) % 7
        
        # 调整结果为0-6（0=周六，1=周日，...，6=周五）
        # 我们需要0=周日，1=周一，...，6=周六
        weekday = (h + 6) % 7
        
        return weekday
    
    @staticmethod
    def get_weekday_name(weekday: int) -> str:
        """
        获取星期几的名称
        
        参数:
            weekday: 星期几（0-6）
            
        返回:
            str: 星期名称缩写
        """
        if not 0 <= weekday <= 6:
            raise ValueError("星期必须在0-6之间")
        return SolarCalendar.WEEKDAY_NAMES[weekday]
    
    @staticmethod
    def get_month_name(month: int) -> str:
        """
        获取月份名称
        
        参数:
            month: 月份（1-12）
            
        返回:
            str: 月份名称
        """
        if not 1 <= month <= 12:
            raise ValueError("月份必须在1-12之间")
        return SolarCalendar.MONTH_NAMES[month - 1]
    
    @staticmethod
    def generate_month_matrix(year: int, month: int) -> list:
        """
        生成指定月份的日历矩阵（6行×7列）
        
        参数:
            year: 年份
            month: 月份
            
        返回:
            list: 6×7的二维列表，空白处用0表示
            
        示例:
            generate_month_matrix(2020, 1)  # 2020年1月
            返回:
            [
                [0, 0, 0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9, 10, 11],
                ...
            ]
        """
        # 初始化6×7的矩阵，全部填充0
        matrix = [[0 for _ in range(7)] for _ in range(6)]
        
        # 获取该月的天数和第一天是星期几
        total_days = SolarCalendar.get_month_days(year, month)
        first_day_weekday = SolarCalendar.get_weekday(year, month, 1)
        
        # 填充日期
        row, col = 0, first_day_weekday
        for day in range(1, total_days + 1):
            matrix[row][col] = day
            
            # 移动到下一个位置
            col += 1
            if col >= 7:
                col = 0
                row += 1
        
        return matrix
    
    @staticmethod
    def generate_year_calendar(year: int) -> dict:
        """
        生成指定年份的完整日历数据
        
        参数:
            year: 年份
            
        返回:
            dict: 键为月份（1-12），值为该月的日历矩阵
        """
        year_calendar = {}
        
        for month in range(1, 13):
            month_matrix = SolarCalendar.generate_month_matrix(year, month)
            year_calendar[month] = month_matrix
        
        return year_calendar
    
    @staticmethod
    def get_date_info(year: int, month: int, day: int) -> dict:
        """
        获取指定日期的详细信息
        
        参数:
            year: 年份
            month: 月份
            day: 日期
            
        返回:
            dict: 包含日期各种信息的字典
        """
        if month < 1 or month > 12:
            raise ValueError("月份必须在1-12之间")
        
        max_days = SolarCalendar.get_month_days(year, month)
        if day < 1 or day > max_days:
            raise ValueError(f"日期必须在1-{max_days}之间")
        
        weekday = SolarCalendar.get_weekday(year, month, day)
        weekday_name = SolarCalendar.get_weekday_name(weekday)
        month_name = SolarCalendar.get_month_name(month)
        
        # 计算是该年的第几天
        day_of_year = day
        for m in range(1, month):
            day_of_year += SolarCalendar.get_month_days(year, m)
        
        # 计算该月有多少周（可能有4-6周）
        matrix = SolarCalendar.generate_month_matrix(year, month)
        week_count = sum(1 for row in matrix if any(row))
        
        return {
            "year": year,
            "month": month,
            "month_name": month_name,
            "day": day,
            "weekday": weekday,
            "weekday_name": weekday_name,
            "day_of_year": day_of_year,
            "is_leap_year": SolarCalendar.is_leap_year(year),
            "month_days": max_days,
            "week_count": week_count,
            "first_weekday": SolarCalendar.get_weekday(year, month, 1),
            "last_weekday": SolarCalendar.get_weekday(year, month, max_days)
        }
    
    @staticmethod
    def validate_date(year: int, month: int, day: int) -> bool:
        """
        验证日期是否有效
        
        参数:
            year: 年份
            month: 月份
            day: 日期
            
        返回:
            bool: 日期有效返回True，否则返回False
        """
        try:
            # 使用datetime验证更准确
            datetime.date(year, month, day)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def get_week_number(year: int, month: int, day: int) -> int:
        """
        计算指定日期是该年的第几周（ISO标准，周一开始）
        
        参数:
            year: 年份
            month: 月份
            day: 日期
            
        返回:
        """
