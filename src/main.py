print("======================================")
print("      Python万年历系统")
print("======================================")
print("")
print("开发团队：")
print("  组长：赵晶鑫")
print("  公历模块：陈一帆")
print("  农历模块：许梓轩")
print("  月视图：王康骏")
print("  年视图：杨雨晨")
print("  键盘控制：叶玮韬")
print("  测试美化：曾博艺")
print("======================================")
print("")
print("项目初始化成功！")
print("请各成员按分工开发对应模块。")


import sys
import os

# 添加 vendor 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vendor_path = os.path.join(project_root, "vendor")
if os.path.exists(vendor_path):
    sys.path.insert(0, vendor_path)
# ========== 分开导入，一个失败不影响其他 ==========
SolarCalendar = None
get_lunar_date = None
display_month_view = None
display_year_view = None
KeyboardController = None

# 1. 导入 solar 模块
try:
    from solar import SolarCalendar
    print("✅ solar 模块导入成功")
except ImportError as e:
    print(f"⚠️  solar 模块导入失败: {e}")

# 2. 导入 lunar 模块
try:
    from lunar import get_lunar_date
    print("✅ lunar 模块导入成功")
except ImportError as e:
    print(f"⚠️  lunar 模块导入失败: {e}")

# 3. 导入视图显示模块
try:
    from views import display_month_view, display_year_view
    print("✅ views 模块导入成功")
except ImportError as e:
    print(f"⚠️  views 模块导入失败: {e}")

# 4. 导入键盘控制模块
def start_keyboard_control():
    if KeyboardController is None:
        print("❌ 无法启动键盘控制：KeyboardController 模块未成功加载")
        print("💡 提示：请检查是否存在 controller.py 文件，或运行 pip 安装相关依赖")
        return

    try:
        keyboard_ctrl = KeyboardController()
        keyboard_ctrl.run()  # 假设有个 run 方法
    except Exception as e:
        print(f"启动键盘控制器时出错: {e}")


def display_team_info():
    """显示开发团队信息"""

def display_team_info():
    """显示开发团队信息"""
    print("=" * 50)
    print("        Python 万年历系统")
    print("=" * 50)
    print("\n👥 开发团队 (25组):")
    print("  • 组长: 赵晶鑫")
    print("  • 公历模块: 陈一帆")
    print("  • 农历模块: 许梓轩")
    print("  • 月视图: 王康骏")
    print("  • 年视图: 杨雨晨")
    print("  • 键盘控制: 叶玮韬")
    print("  • 测试优化: 曾博艺")
    print("=" * 50)
    print("项目初始化成功！")
    print("请各成员按分工开发对应模块。\n")


# main.py - 万年历主框架程序
import sys
from datetime import datetime

# 导入自定义模块（确保这些文件在同级目录下）
try:
    import display_month
    import display_year
    import keyboard
    import lunar
    import solar
except ModuleNotFoundError as e:
    print(f"模块导入失败: {e}")
    print("请确保 display_month.py, display_year.py, keyboard.py, lunar.py, solar.py 存在于当前路径。")
    sys.exit(1)


class CalendarApp:
    def __init__(self):
        self.current_date = datetime.now()

    def show_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 40)
        print("           万年历主菜单")
        print("=" * 40)
        print("1. 显示指定月份日历")
        print("2. 显示指定年份日历")
        print("3. 查看今日农历信息")
        print("4. 切换到农历视图（实验性）")
        print("5. 退出程序")
        print("=" * 40)

    def run(self):
        """主运行循环"""
        print(f"欢迎使用万年历系统！当前日期: {self.current_date.strftime('%Y年%m月%d日')}")

        while True:
            self.show_menu()
            try:
                choice = keyboard.get_input("请选择操作 (1-5): ")
                if choice == '1':
                    self.handle_display_month()
                elif choice == '2':
                    self.handle_display_year()
                elif choice == '3':
                    self.handle_lunar_today()
                elif choice == '4':
                    self.handle_solar_lunar_toggle()
                elif choice == '5':
                    print("感谢使用，再见！")
                    break
                else:
                    print("无效选择，请输入 1-5 之间的数字。")
            except KeyboardInterrupt:
                print("\n\n程序被用户中断。")
                break
            except Exception as e:
                print(f"发生未预期错误: {e}")

    def handle_display_month(self):
        """处理显示指定月份"""
        year = keyboard.get_input("请输入年份 (如 2025): ")
        month = keyboard.get_input("请输入月份 (1-12): ")
        try:
            year = int(year)
            month = int(month)
            if not (1 <= month <= 12):
                raise ValueError("月份必须在 1-12 之间")
            # 调用 display_month 模块展示日历
            display_month.show(year, month)
        except ValueError as ve:
            print(f"输入错误: {ve}")
        except Exception as e:
            print(f"显示月份时出错: {e}")

    def handle_display_year(self):
        """处理显示整年日历"""
        year = keyboard.get_input("请输入年份: ")
        try:
            year = int(year)
            display_year.show(year)
        except ValueError:
            print("请输入有效的年份。")
        except Exception as e:
            print(f"显示年份时出错: {e}")

    def handle_lunar_today(self):
        """显示今天的农历信息"""
        today = datetime.now().date()
        lunar_info = lunar.LunarDate.from_solar(today.year, today.month, today.day)
        print(f"\n今天是公历: {today.strftime('%Y年%m月%d日')}")
        print(f"农历: {lunar_info.year}年{lunar_info.chinese_month}月{lunar_info.chinese_day}")
        print(f"生肖: {lunar_info.animal}")
        print(f"干支纪年: {lunar_info.ganzhi_year}年")

    def handle_solar_lunar_toggle(self):
        """模拟农历与阳历转换功能"""
        print("\n农历 ↔ 阳历转换工具")
        mode = keyboard.get_input("选择转换方式:\n1. 阳历转农历\n2. 农历转阳历\n请输入 (1 或 2): ")
        try:
            if mode == '1':
                y = int(keyboard.get_input("请输入阳历年: "))
                m = int(keyboard.get_input("请输入阳历月: "))
                d = int(keyboard.get_input("请输入阳历日: "))
                lunar_date = lunar.LunarDate.from_solar(y, m, d)
                print(f"对应的农历为: {lunar_date}")
            elif mode == '2':
                y = int(keyboard.get_input("请输入农历年: "))
                is_leap = keyboard.get_input("是否为闰月? (y/n): ").lower() == 'y'
                m = int(keyboard.get_input("请输入农历月: "))
                d = int(keyboard.get_input("请输入农历日: "))
                solar_date = lunar.LunarDate.to_solar(y, m, d, is_leap)
                if solar_date:
                    print(f"对应的阳历为: {solar_date.year}年{solar_date.month}月{solar_date.day}日")
                else:
                    print("无法计算对应阳历日期（可能超出支持范围）")
            else:
                print("无效选择。")
        except Exception as e:
            print(f"转换过程中出现错误: {e}")


if __name__ == "__main__":
    app = CalendarApp()
    app.run()
