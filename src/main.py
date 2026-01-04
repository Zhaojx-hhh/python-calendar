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

# main.py
import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 先定义所有变量，避免未定义错误
SolarCalendar = None
get_lunar_date = None
display_month_view = None
display_year_view = None
KeyboardController = None

# 导入项目模块
try:
    from solar import SolarCalendar
    from lunar import get_lunar_date
    from display_month import display_month_view
    from display_year import display_year_view
    from keyboard import KeyboardController
    print("✅ 所有模块导入成功！")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    print("请确保以下文件存在:")
    print("  - solar.py (公历模块)")
    print("  - lunar.py (农历模块)")
    print("  - display_month.py (月视图)")
    print("  - display_year.py (年视图)")
    print("  - keyboard.py (键盘控制)")
    sys.exit(1)

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


def main():
    """主程序入口"""
    # 显示团队信息
    display_team_info()

    # 初始化组件
    print("初始化系统组件...")
    solar_cal = SolarCalendar()
    keyboard_ctrl = KeyboardController()

    # 获取当前日期
    import datetime
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month

    print(f"📅 当前日期: {current_year}年{current_month}月{today.day}日")

    # 主循环
    while True:
        print("\n" + "=" * 50)
        print("万年历系统菜单:")
        print("  1. 查看月视图")
        print("  2. 查看年视图")
        print("  3. 查看特定月份")
        print("  4. 查看特定年份")
        print("  5. 显示农历信息")
        print("  6. 键盘控制演示")
        print("  0. 退出系统")
        print("=" * 50)

        try:
            choice = input("请选择功能 (0-6): ").strip()

            if choice == '0':
                print("\n 感谢使用万年历系统，再见！")
                break

            elif choice == '1':
                # 月视图 - 当前月
                display_month_view(current_year, current_month)

            elif choice == '2':
                # 年视图 - 当前年
                display_year_view(current_year)

            elif choice == '3':
                # 查看特定月份
                try:
                    year = int(input("请输入年份 (如 2024): "))
                    month = int(input("请输入月份 (1-12): "))
                    if 1 <= month <= 12:
                        display_month_view(year, month)
                    else:
                        print("❌ 月份必须在 1-12 之间")
                except ValueError:
                    print("❌ 请输入有效的数字")

            elif choice == '4':
                # 查看特定年份
                try:
                    year = int(input("请输入年份 (如 2024): "))
                    display_year_view(year)
                except ValueError:
                    print("❌ 请输入有效的年份")

            elif choice == '5':
                # 显示农历信息
                try:
                    year = int(input("请输入年份: "))
                    month = int(input("请输入月份 (1-12): "))
                    day = int(input("请输入日期: "))

                    lunar_info = get_lunar_date(year, month, day)
                    print(f"\n农历信息:")
                    print(f"  公历: {year}年{month}月{day}日")
                    print(f"  农历: {lunar_info}")

                except ValueError:
                    print("❌ 请输入有效的日期")

            elif choice == '6':
                # 键盘控制演示
                print("\n⌨️ 键盘控制演示:")
                print("  使用方向键 ↑ ↓ ← → 导航")
                print("  按 Enter 键选择")
                print("  按 ESC 键返回")
                keyboard_ctrl.demo()

            else:
                print("❌ 无效选择，请重新输入 (0-6)")

        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")


if __name__ == "__main__":
    main()