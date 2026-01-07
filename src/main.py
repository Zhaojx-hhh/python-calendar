
"""
📅 Python 万年历系统 v1.0 - 主程序入口
开发团队：25组
功能：集成公历/农历/月视图/年视图/键盘控制
"""

import sys
import os
import time
from datetime import datetime


# ========== 🔧 路径初始化（最关键部分）==========
def setup_project_paths():
    """设置项目路径，确保可以导入本地模块和 vendor 依赖"""
    # 获取当前文件路径
    CURRENT_FILE = os.path.abspath(__file__)
    CURRENT_DIR = os.path.dirname(CURRENT_FILE)  # src/
    PROJECT_ROOT = os.path.dirname(CURRENT_DIR)  # 项目根目录
    VENDOR_DIR = os.path.join(PROJECT_ROOT, "vendor")

    print("🔧 项目路径设置:")
    print(f"  当前文件: {CURRENT_FILE}")
    print(f"  项目根目录: {PROJECT_ROOT}")
    print(f"  当前目录: {CURRENT_DIR}")

    # 添加 vendor 到搜索路径（优先）
    if os.path.exists(VENDOR_DIR):
        if VENDOR_DIR not in sys.path:
            sys.path.insert(0, VENDOR_DIR)
            print(f"✅ 已添加 vendor 路径: {VENDOR_DIR}")
    else:
        print(f"⚠️  vendor 目录不存在: {VENDOR_DIR}")

    # 添加项目根目录和当前目录
    for path in [PROJECT_ROOT, CURRENT_DIR]:
        if path not in sys.path:
            sys.path.insert(0, path)

    return CURRENT_DIR, PROJECT_ROOT


# 执行路径设置
current_dir, project_root = setup_project_paths()


# ========== 📦 模块导入调试工具 ==========
def debug_import(module_name, attr=None):
    """调试导入并返回模块或属性"""
    try:
        module = __import__(module_name, fromlist=[attr] if attr else None)
        if attr:
            return getattr(module, attr)
        return module
    except Exception as e:
        print(f"❌ 导入失败: {module_name} -> {e}")
        return None


# ========== 🚀 加载第三方库 pynput ==========
print("\n📦 正在加载核心依赖...")

try:
    import pynput
    from pynput import keyboard  # 验证关键子模块可用
    # 尝试获取版本号（安全方式）
    try:
        # 方法1：先看有没有 __version__
        version = getattr(pynput, '__version__', None)
        if version:
            pynput_version = version
        else:
            # 方法2：使用 importlib.metadata 获取安装版本
            from importlib.metadata import version as pkg_version
            pynput_version = pkg_version("pynput")
        print(f"✅ 成功导入 pynput，版本: {pynput_version}")
    except Exception:
        # 即使拿不到版本号也不影响运行
        print("✅ 成功导入 pynput（版本信息不可用）")
except ImportError as e:
    print(f"❌ 导入 pynput 失败: {e}")
    print("💡 请检查以下问题：")
    print("   1. 是否运行过: pip install --target='./vendor' pynput")
    print("   2. vendor 目录下是否有 pynput 文件夹？")
    print("   3. src/ 下是否有名为 pynput.py 的冲突文件？")
    sys.exit(1)



# == ======== 🧩 动态导入团队开发的模块 ==========
print("-" * 50)
print("🔄 正在加载团队开发模块...")

# 初始化模块变量
KeyboardController = debug_import('keyboard', 'KeyboardController')
SolarCalendar = debug_import('solar', 'SolarCalendar')
get_lunar_date = debug_import('lunar', 'get_lunar_date')
display_month_view = debug_import('views', 'display_month_view')
display_year_view = debug_import('views', 'display_year_view')

print("-" * 50)


# ========== 🖼️ 备用视图实现（当 views 模块缺失时）==========
def simple_month_view(year, month):
    """简单月视图（备用）"""
    from calendar import monthcalendar, month_name

    print(f"\n📅 {year}年 {month_name[month]}月")
    print("=" * 35)
    print(" 日   一   二   三   四   五   六")
    print("-" * 35)

    cal = monthcalendar(year, month)
    for week in cal:
        line = ""
        for day in week:
            if day == 0:
                line += "     "
            else:
                line += f"{day:2d}  "
        print(f" {line}")
    print("=" * 35)


def simple_year_view(year):
    """简单年视图（备用）"""
    print(f"\n📊 {year}年 全年概览")
    print("=" * 40)
    for m in range(1, 13):
        q = (m + 2) // 3  # 第几季度
        days = 31 if m in [1, 3, 5, 7, 8, 10, 12] else 30 if m != 2 else 29 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 28
        print(f"{m:2d}月 ({days:2d}天) | {'■' * 6}")
    print("=" * 40)


# ========== 👥 开发团队信息展示 ==========
def display_team_info():
    """显示团队成员信息"""
    print("\n" + "=" * 50)
    print("        📅 Python 万年历系统 v1.0")
    print("=" * 50)
    print("\n👥 开发团队 (25组):")
    print("  🎯 组长: 赵晶鑫")
    print("  📅 公历模块: 陈一帆")
    print("  🌙 农历模块: 许梓轩")
    print("  📊 月视图: 王康骏")
    print("  📈 年视图: 杨雨晨")
    print("  ⌨️  键盘控制: 叶玮韬")
    print("  🎨 测试美化: 曾博艺")
    print("\n" + "=" * 50)
    print("✅ 项目初始化完成！")
    print("💡 提示: 使用方向键/V/空格/Q 进行操作")
    print("=" * 50)


# ========== 🧠 主应用类 CalendarApp ==========
class CalendarApp:
    def __init__(self):
        now = datetime.now()
        self.state = {
            'year': now.year,
            'month': now.month,
            'view': 'month',
            'action': None
        }
        self.keyboard_controller = None
        self.is_running = False

    def keyboard_callback(self, new_state):
        """接收键盘控制器传来的状态更新"""
        self.state.update(new_state)
        self.display_current_view()

    def display_current_view(self):
        """根据当前状态显示视图"""
        os.system('cls' if os.name == 'nt' else 'clear')  # 清屏

        print("\n" + "=" * 50)
        print("        📅 Python 万年历系统")
        print("=" * 50)

        view_name = "月视图" if self.state['view'] == 'month' else "年视图"
        print(f"📍 当前位置: {self.state['year']}年{self.state['month']:02d}月 | 模式: {view_name}")
        print("-" * 50)

        # 显示内容
        if self.state['view'] == 'month':
            self._show_month()
        else:
            self._show_year()

        self.show_help()

    def _show_month(self):
        """显示月视图（优先使用模块，否则降级）"""
        year, month = self.state['year'], self.state['month']
        if display_month_view:
            try:
                display_month_view(year, month)
            except Exception as e:
                print(f"[警告] display_month_view 执行出错: {e}")
        else:
            simple_month_view(year, month)

        # 显示农历首日
        if get_lunar_date:
            try:
                lunar_info = get_lunar_date(year, month, 1)
                print(f"\n🌙 本月农历起始: {lunar_info}")
            except Exception as e:
                print(f"\n⚠️  农历数据获取失败: {e}")

    def _show_year(self):
        """显示年视图"""
        year = self.state['year']
        if display_year_view:
            try:
                display_year_view(year)
            except Exception as e:
                print(f"[警告] display_year_view 执行出错: {e}")
        else:
            simple_year_view(year)

        # 年度统计
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        print(f"\n📆 {year}年 统计:")
        print(f"  总天数: {366 if is_leap else 365}")
        print(f"  是否闰年: {'是' if is_leap else '否'}")

    def show_help(self):
        """操作提示"""
        print("\n" + "-" * 50)
        print("📋 操作指南:")
        print("  ↑↓ ←→ : 调整年月")
        print("  V      : 切换视图模式")
        print("  空格键 : 返回今天")
        print("  Q      : 退出程序")
        print("-" * 50)

    def setup_keyboard(self):
        """初始化键盘控制器"""
        if KeyboardController is None:
            print("❌ 错误: keyboard.py 未加载，请检查文件和依赖！")
            return False

        try:
            self.keyboard_controller = KeyboardController(self.keyboard_callback)
            print("✅ 键盘控制器已初始化")
            return True
        except Exception as e:
            print(f"❌ 初始化 KeyboardController 失败: {e}")
            return False

    def run(self):
        """启动主循环"""
        print("\n🚀 启动万年历系统...")

        if not self.setup_keyboard():
            print("🛑 无法启动键盘控制，程序退出。")
            return

        self.display_current_view()
        print("\n🎮 键盘监听已启动...")
        print("💡 使用方向键导航，按 Q 退出")

        try:
            self.keyboard_controller.start()
            self.is_running = True

            while self.is_running and self.keyboard_controller.is_running:
                time.sleep(0.1)  # 降低 CPU 占用

        except KeyboardInterrupt:
            print("\n\n🛑 用户中断")
        except Exception as e:
            print(f"\n❌ 运行时异常: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()

    def cleanup(self):
        """释放资源"""
        if self.keyboard_controller:
            self.keyboard_controller.stop()
        print("\n🎯 程序已安全退出")


# ========== ▶️ 主程序入口 ==========
if __name__ == "__main__":
    # 显示团队信息
    display_team_info()

    # 关键模块检查
    if KeyboardController is None:
        print("\n" + "!" * 50)
        print("🚨 致命错误：键盘控制模块未加载！")
        print("请检查以下几点：")
        print("  1. 文件是否存在？ → src/keyboard.py")
        print("  2. 是否安装了 pynput？ → pip install --target='./vendor' pynput")
        print("  3. vendor/pynput/__init__.py 是否存在？")
        print("!" * 50)
        sys.exit(1)

    # 创建并运行应用
    try:
        app = CalendarApp()
        app.run()
    except Exception as e:
        print(f"\n💀 程序崩溃: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

