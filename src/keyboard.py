# 键盘控制模块（叶玮韬负责） 
"""
万年历键盘操作模块 - 专用于小组作业
作者：叶玮韬
功能：
1. 处理键盘输入：上下箭头键改变年份，左右箭头键改变月份
2. 切换月视图与年视图
3. 提供回调接口，通知主程序状态变化。
"""
import sys
import time
from typing import Callable

try:
    from pynput import keyboard

    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("请安装: pip install pynput")
    sys.exit(1)


class SimpleKeyboardController:
    """键盘控制器"""

    def __init__(self, callback: Callable):
        """
        初始化

        Args:
            callback: 回调函数，接收一个字典参数：
                {
                    'year': int,    # 年份
                    'month': int,   # 月份
                    'view': str,    # 'month'或'year'
                    'action': str   # 操作类型
                }
        """
        self.callback = callback

        # 初始状态
        import datetime
        today = datetime.date.today()
        self.year = today.year
        self.month = today.month
        self.view = 'month'  # 默认月视图

        self.is_running = False
        self.listener = None

    def _on_key_press(self, key):
        """处理按键"""
        try:
            # 获取按键名称
            if hasattr(key, 'char') and key.char:
                key_name = key.char.lower()
            elif hasattr(key, 'name'):
                key_name = key.name.lower()
            else:
                key_name = str(key).replace("'", "").lower()

            # 处理方向键
            if key_name == 'up':
                self.year += 1
                action = 'year_up'
            elif key_name == 'down':
                self.year -= 1
                if self.year < 1:
                    self.year = 1
                action = 'year_down'
            elif key_name == 'left':
                self.month -= 1
                if self.month < 1:
                    self.month = 12
                    self.year -= 1
                action = 'month_left'
            elif key_name == 'right':
                self.month += 1
                if self.month > 12:
                    self.month = 1
                    self.year += 1
                action = 'month_right'

            # 处理视图切换
            elif key_name == 'v':
                # 切换视图
                self.view = 'year' if self.view == 'month' else 'month'
                action = 'toggle_view'

            # 其他按键
            elif key_name == ' ' or key_name == 'space':
                # 回到今天
                import datetime
                today = datetime.date.today()
                self.year, self.month = today.year, today.month
                action = 'go_today'
            elif key_name == 'q':
                self.stop()
                return
            else:
                return  # 忽略其他按键

            # 调用回调函数
            self.callback({
                'year': self.year,
                'month': self.month,
                'view': self.view,
                'action': action
            })

        except Exception as e:
            print(f"键盘错误: {e}")

    def start(self):
        """启动键盘监听"""
        self.is_running = True
        self.listener = keyboard.Listener(on_press=self._on_key_press)
        self.listener.start()
        print("键盘控制器已启动")

    def stop(self):
        """停止键盘监听"""
        if self.listener:
            self.listener.stop()
        self.is_running = False
        print("键盘控制器已停止")


# ==================== 使用示例 ====================

def example_usage():
    """展示如何在主程序中使用"""

    # 1. 定义回调函数
    def handle_keyboard_event(state):
        """处理键盘事件"""
        print(f"\n收到键盘事件:")
        print(f"  操作: {state['action']}")
        print(f"  年份: {state['year']}")
        print(f"  月份: {state['month']}")
        print(f"  视图: {state['view']}")

        # 这里应该调用显示函数
        # display_calendar(state['year'], state['month'], state['view'])

    # 2. 创建键盘控制器
    keyboard_ctrl = SimpleKeyboardController(handle_keyboard_event)

    # 3. 启动键盘监听
    keyboard_ctrl.start()

    print("键盘操作说明:")
    print("  ↑/↓ : 改变年份")
    print("  ←/→ : 改变月份")
    print("  v   : 切换视图")
    print("  空格 : 回到今天")
    print("  q   : 退出")
    print("-" * 30)

    # 4. 保持程序运行
    try:
        while keyboard_ctrl.is_running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n程序被中断")
    finally:
        keyboard_ctrl.stop()


if __name__ == "__main__":
    example_usage()