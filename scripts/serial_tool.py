#!/usr/bin/env python3
"""
串口监听工具 - MCP工具
用于AI调用，后台监听串口数据并写入日志文件

用法:
    python serial_tool.py start <config_json>   # 启动监听
    python serial_tool.py stop                   # 停止监听
    python serial_tool.py status                 # 查看状态
    python serial_tool.py notify                 # 检查是否有新数据通知
"""

import sys
import json
import os
import threading
import time
from pathlib import Path

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("ERROR: pyserial not installed. Run: pip install pyserial")
    sys.exit(1)

try:
    import tkinter as tk
    from tkinter import scrolledtext
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False


class SerialListener:
    def __init__(self, config_path=None):
        self.running = False
        self.thread = None
        self.serial_port = None
        self.log_file = None
        self.status_file = ".emv2/logs/.serial_status.json"
        self.gui = None

        if config_path:
            self.load_config(config_path)
        else:
            self.config = self.default_config()

    def default_config(self):
        return {
            "serial": {
                "port": "COM5",
                "baudrate": 115200,
                "bytesize": 8,
                "parity": "N",
                "stopbits": 1,
                "timeout": 1
            },
            "end_marker": "DEBUG_TEST_END",
            "log_file": ".emv2/logs/serial.log",
            "keywords": {
                "debug": "[DBG]",
                "error": "[ERR]",
                "pass": "[PASS]",
                "fail": "[FAIL]"
            }
        }

    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    def save_status(self, status):
        """保存状态到共享文件，供AI读取"""
        os.makedirs(os.path.dirname(self.status_file), exist_ok=True)
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False)

    def start(self):
        if self.running:
            print("ALREADY_RUNNING")
            return

        try:
            ser_cfg = self.config["serial"]
            self.serial_port = serial.Serial(
                port=ser_cfg["port"],
                baudrate=int(ser_cfg["baudrate"]),
                bytesize=int(ser_cfg["bytesize"]),
                parity=ser_cfg["parity"],
                stopbits=int(ser_cfg["stopbits"]),
                timeout=float(ser_cfg["timeout"])
            )

            os.makedirs(os.path.dirname(self.config["log_file"]), exist_ok=True)
            self.log_file = open(self.config["log_file"], 'w', encoding='utf-8')

            self.running = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()

            self.save_status({
                "status": "running",
                "port": ser_cfg["port"],
                "baudrate": ser_cfg["baudrate"],
                "log_file": self.config["log_file"]
            })

            if HAS_TKINTER:
                self._start_gui()

            print("STARTED")

        except Exception as e:
            print(f"ERROR: {e}")
            self.running = False

    def _listen_loop(self):
        """监听循环"""
        end_marker = self.config.get("end_marker", "DEBUG_TEST_END")
        keywords = self.config.get("keywords", {})

        while self.running:
            try:
                if self.serial_port.in_waiting:
                    line = self.serial_port.readline().decode('utf-8', errors='replace')
                    if line:
                        self.log_file.write(line)
                        self.log_file.flush()

                        # 检查是否包含关键词
                        for key, marker in keywords.items():
                            if marker in line:
                                self.save_status({
                                    "status": "running",
                                    "last_keyword": key,
                                    "last_line": line.strip(),
                                    "has_new_data": True
                                })

                        # 检查结束标记
                        if end_marker in line:
                            self.save_status({
                                "status": "end_marker_received",
                                "end_marker": end_marker,
                                "last_line": line.strip(),
                                "has_new_data": True
                            })
                            print("END_MARKER_DETECTED")
                else:
                    time.sleep(0.1)

            except Exception as e:
                print(f"LISTEN_ERROR: {e}")
                break

    def stop(self):
        """停止监听"""
        self.running = False
        self.gui_alive = False

        if self.serial_port:
            try:
                self.serial_port.close()
            except:
                pass

        if self.log_file:
            try:
                self.log_file.close()
            except:
                pass

        self.save_status({
            "status": "stopped",
            "log_file": self.config.get("log_file", "")
        })

        if self.gui:
            try:
                self.gui.destroy()
            except:
                pass

        print("STOPPED")

    def get_status(self):
        """获取状态"""
        try:
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {"status": "not_running"}

    def check_notify(self):
        """AI调用：检查是否有新数据通知"""
        status = self.get_status()
        if status.get("has_new_data"):
            # 清除通知标记
            status["has_new_data"] = False
            self.save_status(status)
            return status
        return None

    def _start_gui(self):
        """启动GUI（可独立关闭，不影响监听）"""
        if not HAS_TKINTER:
            return

        def gui_loop():
            gui = tk.Tk()
            gui.title(f"串口监听")
            gui.geometry("500x500")

            # 配置区域
            config_frame = tk.LabelFrame(gui, text="串口配置", padx=10, pady=10)
            config_frame.pack(fill="x", padx=10, pady=5)

            # 端口
            tk.Label(config_frame, text="端口:").grid(row=0, column=0, sticky="w")
            port_var = tk.StringVar(value=self.config["serial"]["port"])
            port_entry = tk.Entry(config_frame, textvariable=port_var, width=15)
            port_entry.grid(row=0, column=1, padx=5)

            # 波特率
            tk.Label(config_frame, text="波特率:").grid(row=0, column=2, sticky="w")
            baudrate_var = tk.StringVar(value=str(self.config["serial"]["baudrate"]))
            baudrate_entry = tk.Entry(config_frame, textvariable=baudrate_var, width=10)
            baudrate_entry.grid(row=0, column=3, padx=5)

            # 数据位
            tk.Label(config_frame, text="数据位:").grid(row=1, column=0, sticky="w", pady=5)
            bytesize_var = tk.StringVar(value=str(self.config["serial"]["bytesize"]))
            bytesize_entry = tk.Entry(config_frame, textvariable=bytesize_var, width=15)
            bytesize_entry.grid(row=1, column=1, padx=5)

            # 校验位
            tk.Label(config_frame, text="校验位:").grid(row=1, column=2, sticky="w")
            parity_var = tk.StringVar(value=self.config["serial"]["parity"])
            parity_entry = tk.Entry(config_frame, textvariable=parity_var, width=10)
            parity_entry.grid(row=1, column=3, padx=5)

            # 停止位
            tk.Label(config_frame, text="停止位:").grid(row=2, column=0, sticky="w")
            stopbits_var = tk.StringVar(value=str(self.config["serial"]["stopbits"]))
            stopbits_entry = tk.Entry(config_frame, textvariable=stopbits_var, width=15)
            stopbits_entry.grid(row=2, column=1, padx=5)

            # 状态标签
            status_label = tk.Label(gui, text="未监听", fg="gray")
            status_label.pack(pady=5)

            # 日志显示
            text_area = scrolledtext.ScrolledText(gui, width=60, height=18)
            text_area.pack(pady=10)

            # 更新配置
            def apply_config():
                self.config["serial"]["port"] = port_var.get()
                self.config["serial"]["baudrate"] = int(baudrate_var.get())
                self.config["serial"]["bytesize"] = int(bytesize_var.get())
                self.config["serial"]["parity"] = parity_var.get()
                self.config["serial"]["stopbits"] = int(stopbits_var.get())
                status_label.config(text=f"配置已更新: {port_var.get()} @ {baudrate_var.get()}", fg="blue")

            # 按钮区域
            btn_frame = tk.Frame(gui)
            btn_frame.pack(pady=5)

            tk.Button(btn_frame, text="应用配置", command=apply_config).pack(side="left", padx=5)
            tk.Button(btn_frame, text="刷新日志", command=lambda: None).pack(side="left", padx=5)

            # 更新线程
            def update_gui():
                while self.running and self.gui_alive:
                    try:
                        with open(self.config["log_file"], 'r', encoding='utf-8') as f:
                            content = f.read()
                        text_area.delete(1.0, tk.END)
                        text_area.insert(tk.END, content)
                        text_area.see(tk.END)
                        if self.serial_port and self.serial_port.is_open:
                            status_label.config(
                                text=f"监听中: {self.config['serial']['port']} @ {self.config['serial']['baudrate']}",
                                fg="green"
                            )
                    except:
                        pass
                    time.sleep(0.5)

                status_label.config(text="GUI已关闭，监听继续后台运行", fg="blue")

            threading.Thread(target=update_gui, daemon=True).start()

            # 关闭窗口只是隐藏，不停止监听
            def on_close():
                self.gui_alive = False
                gui.destroy()

            gui.protocol("WM_DELETE_WINDOW", on_close)
            gui.mainloop()

        self.gui_alive = True
        threading.Thread(target=gui_loop, daemon=True).start()


def main():
    if len(sys.argv) < 2:
        print("Usage: serial_tool.py <start|stop|status|notify> [config_json]")
        sys.exit(1)

    command = sys.argv[1].lower()

    listener = SerialListener()

    if command == "start":
        config_path = sys.argv[2] if len(sys.argv) > 2 else None
        if config_path:
            listener.load_config(config_path)
        listener.start()

    elif command == "stop":
        listener.stop()

    elif command == "status":
        import json
        print(json.dumps(listener.get_status(), ensure_ascii=False))

    elif command == "notify":
        result = listener.check_notify()
        if result:
            import json
            print(json.dumps(result, ensure_ascii=False))
        else:
            print("NO_NOTIFY")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
