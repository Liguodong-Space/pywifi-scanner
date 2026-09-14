# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from plyer import wifi
import time

# 设置窗口背景色为深色，护眼且极客风
Window.clearcolor = (0.1, 0.1, 0.15, 1)


class WiFiScannerApp(App):
    def build(self):
        self.title = "PyWiFi Scanner"

        # 主布局
        root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 顶部状态栏
        self.status_label = Label(text="点击下方按钮开始扫描...", size_hint_y=0.1, color=(0, 1, 0, 1))
        root_layout.add_widget(self.status_label)

        # 扫描按钮
        self.scan_btn = Button(text="🔍 扫描周围 WiFi", size_hint_y=0.15, background_color=(0.2, 0.6, 1, 1))
        self.scan_btn.bind(on_press=self.start_scan)
        root_layout.add_widget(self.scan_btn)

        # 列表区域 (ScrollView + GridLayout)
        scroll_view = ScrollView(size_hint=(1, 0.75))
        self.list_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        scroll_view.add_widget(self.list_layout)
        root_layout.add_widget(scroll_view)

        return root_layout

    def start_scan(self, instance):
        self.scan_btn.disabled = True
        self.status_label.text = "正在扫描... (请确保手机GPS已开启)"
        self.list_layout.clear_widgets()

        # 在安卓上，wifi扫描是异步的或者需要时间，这里用Clock调度避免卡UI
        Clock.schedule_once(self.do_scan, 0.5)

    def do_scan(self, dt):
        try:
            # 启用WiFi并扫描
            wifi.enable()
            time.sleep(1)  # 等待硬件就绪

            # 获取扫描结果
            # plyer 的 wifi.facilities 或类似方法在不同版本有差异
            # 这里使用标准的 networks 属性尝试获取
            networks = wifi.networks

            if not networks:
                self.status_label.text = "未找到任何网络 (请检查定位权限/GPS)"
                self.add_info_row("提示", "Android 10+ 需要开启位置服务才能扫描WiFi")
            else:
                self.status_label.text = f"扫描完成! 发现 {len(networks)} 个网络"

                # 按信号强度排序
                sorted_networks = sorted(networks, key=lambda x: x.get('level', -100), reverse=True)

                for net in sorted_networks:
                    ssid = net.get('ssid', 'Unknown')
                    bssid = net.get('bssid', 'N/A')
                    level = net.get('level', -100)
                    capabilities = net.get('capabilities', 'N/A')

                    # 计算信号质量百分比 (粗略估算)
                    quality = min(max(2 * (level + 100), 0), 100)

                    # 根据信号强度决定颜色
                    if level > -50:
                        color = (0, 1, 0, 1)  # 绿
                    elif level > -70:
                        color = (1, 1, 0, 1)  # 黄
                    else:
                        color = (1, 0.3, 0.3, 1)  # 红

                    info_text = (
                        f"[b]SSID:[/b] {ssid}\n"
                        f"[b]信号:[/b] {level} dBm ({quality}%)\n"
                        f"[b]加密:[/b] {'WPA/WPA2' if 'WPA' in capabilities else 'Open'}\n"
                        f"[b]MAC:[/b] {bssid}"
                    )
                    self.add_info_row(ssid, info_text, color)

        except Exception as e:
            self.status_label.text = f"错误: {str(e)}"
            # 注意：在PC上运行会报错，这是正常的，必须在安卓真机上运行
        finally:
            self.scan_btn.disabled = False

    def add_info_row(self, title, content, color=(1, 1, 1, 1)):
        btn = Button(
            text=content,
            markup=True,
            size_hint_y=None,
            height=120,
            background_color=(0.2, 0.2, 0.25, 1),
            color=color,
            halign='left',
            valign='middle'
        )
        btn.bind(size=btn.setter('text_size'))
        self.list_layout.add_widget(btn)


if __name__ == '__main__':
    WiFiScannerApp().run()