"""
键盘控制模块 - 叶玮韬负责
使用项目vendor目录下的pynput库，无需安装
"""

import sys
import os
import time
from typing import Callable, Optional

# ============ 核心：设置正确的导入路径 ============
# 获取当前文件（my_keyboard.py）所在的绝对路径
current_file = os.path.abspath(__file__)  # 例如：/项目根目录/src/my_keyboard.py
current_dir = os.path.dirname(current_file)  # 例如：/项目根目录/src
project_root = os.path.dirname(current_dir)  # 例如：/项目根目录

# 构建vendor/pynput的完整路径
pynput_path = os.path.join(project_root, 'vendor', 'pynput')  # 例如：/项目根目录/vendor/pynput

# 只在直接运行时打印调试信息
if __name__ == "__main__":
    print(f"调试信息：")
    print(f"  当前文件：{current_file}")
    print(f"  当前目录：{current_dir}")
    print(f"  项目根目录：{project_root}")
    print(f"  pynput路径：{pynput_path}")

# 检查pynput文件夹是否存在
if not os.path.exists(pynput_path):
    print(f"❌ 错误：找不到pynput文件夹")
    sys.exit(1)

# 将pynput路径添加到Python搜索路径的最前面
if pynput_path not in sys.path:
    sys.path.insert(0, pynput_path)
    if __name__ == "__main__":
        print(f"✅ 已添加pynput路径到Python搜索路径")

# 现在导入pynput
try:
    from pynput import keyboard
    if __name__ == "__main__":
        print("✅ pynput库导入成功")
except ImportError as e:
    print(f"❌ 导入pynput失败：{e}")
    sys.exit(1)
# =================================================

class KeyboardController:
    """键盘控制器类"""

    def __init__(self, callback: Optional[Callable] = None):
        """
        初始化键盘控制器

        Args:
            callback: 回调函数（可选），当状态变化时调用
        """
        self.callback = callback

        # 初始状态
        import datetime
        today = datetime.date.today()
        self.year = today.year
        self.month = today.month
        self.view = 'month'  # 默认月视图（'month'或'year'）

        # 控制标志
        self.is_running = False
        self.listener = None

        print(f"键盘控制器初始化完成：{self.year}年{self.month}月 [{self.view}]")

    def _on_key_press(self, key):
        """处理按键事件"""
        try:
            # 获取按键名称
            if hasattr(key, 'char') and key.char:
                key_name = key.char.lower()
            elif hasattr(key, 'name'):
                key_name = key.name.lower()
            else:
                key_name = str(key).replace("'", "").lower()

            action = None

            # ===== 处理方向键 =====
            if key_name == 'up':
                self.year += 1
                action = 'year_up'
                print(f"↑ 年份+1 → {self.year}年")

            elif key_name == 'down':
                self.year -= 1
                if self.year < 1:
                    self.year = 1
                action = 'year_down'
                print(f"↓ 年份-1 → {self.year}年")

            elif key_name == 'left':
                self.month -= 1
                if self.month < 1:
                    self.month = 12
                    self.year -= 1
                action = 'month_left'
                print(f"← 月份-1 → {self.year}年{self.month}月")

            elif key_name == 'right':
                self.month += 1
                if self.month > 12:
                    self.month = 1
                    self.year += 1
                action = 'month_right'
                print(f"→ 月份+1 → {self.year}年{self.month}月")

            # ===== 处理视图切换 =====
            elif key_name == 'v':
                # 切换视图：月 ↔ 年
                if self.view == 'month':
                    self.view = 'year'
                    view_name = "年视图"
                else:
                    self.view = 'month'
                    view_name = "月视图"
                action = 'toggle_view'
                print(f"V 切换视图 → {view_name}")

            # ===== 其他功能键 =====
            elif key_name == ' ' or key_name == 'space':
                # 回到今天
                import datetime
                today = datetime.date.today()
                self.year, self.month = today.year, today.month
                action = 'go_today'
                print(f"空格 回到今天 → {self.year}年{self.month}月")

            elif key_name == 'esc':
                # ESC键返回菜单
                action = 'esc_exit'
                print("ESC 返回菜单")
                self.stop()
                return False  # 返回False停止监听器


            elif key_name == 'q':
                # 退出程序
                action = 'quit'
                print("Q 退出程序")
                self.stop()
                return False  # 返回False停止监听器

            elif key_name == 'enter':
                # 回车键确认
                action = 'confirm'
                print("Enter 确认选择")

            # ===== 通知状态变化 =====
            if action and self.callback:
                self.callback({
                    'year': self.year,
                    'month': self.month,
                    'view': self.view,
                    'action': action
                })

        except Exception as e:
            print(f"❌ 按键处理错误: {e}")

    def start(self):
        """启动键盘监听（后台运行）"""
        if self.is_running:
            print("键盘控制器已经在运行")
            return

        try:
            self.listener = keyboard.Listener(on_press=self._on_key_press)
            self.listener.start()
            self.is_running = True
            print("✅ 键盘监听已启动")
            print("   使用方向键控制年份和月份，V切换视图")

        except Exception as e:
            print(f"❌ 启动键盘监听失败: {e}")
            self.is_running = False

    def stop(self):
        """停止键盘监听"""
        if not self.is_running:
            return

        if self.listener:
            self.listener.stop()

        self.is_running = False
        print("键盘监听已停止")

    def demo(self):
        """演示键盘控制功能（组长的main.py会调用这个）"""
        print("\n" + "="*50)
        print("键盘控制演示")
        print("="*50)
        print("操作说明:")
        print("  ↑ : 增加年份")
        print("  ↓ : 减少年份")
        print("  ← : 减少月份")
        print("  → : 增加月份")
        print("  V : 切换视图（月视图 ↔ 年视图）")
        print("  空格 : 回到今天")
        print("  Enter : 确认选择")
        print("  ESC : 返回菜单")  # 新增
        print("  Q : 退出演示")
        print("="*50)
        print(f"当前: {self.year}年{self.month}月")
        print("请按键盘进行控制...")

        # 定义一个简单的回调函数用于演示
        def demo_callback(state):
            print(f"  状态: {state['year']}年{state['month']}月 | 视图: {state['view']} | 操作: {state['action']}")

        # 保存原来的回调函数，设置为演示回调
        original_callback = self.callback
        self.callback = demo_callback

        # 启动键盘监听
        self.start()

        print("\n（按 Q 退出演示，或按 Ctrl+C 中断）")
        try:
            while self.is_running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n演示被中断")
        finally:
            self.stop()
            # 恢复原来的回调函数
            self.callback = original_callback

        print("键盘控制演示结束")

    def get_current_state(self):
        """获取当前状态（其他模块可以调用）"""
        return {
            'year': self.year,
            'month': self.month, 'view': self.view,
            'is_running': self.is_running}
#======测试代码======	"
if __name__ == "__main__":
    print("测试键盘控制器模块...")

    def test_callback(state):
        print(f"[测试回调]{state}")

    controller = KeyboardController(test_callback)
    controller.demo()
