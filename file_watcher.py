import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path
        self.process = None
        self.restart_script()

    def restart_script(self):
        """重启Python脚本"""
        if self.process:
            print("终止现有进程...")
            self.process.terminate()
            self.process.wait()

        print(f"启动脚本: {self.script_path}")
        self.process = subprocess.Popen([sys.executable, self.script_path])

    def on_modified(self, event):
        """当文件被修改时调用"""
        if event.src_path.endswith(".py"):
            print(f"检测到文件变化: {event.src_path}")
            self.restart_script()


def main():
    # 要监控的脚本路径
    script_to_watch = "main.py"

    # 要监控的目录（当前目录）
    path_to_watch = "."

    # 创建事件处理器
    event_handler = FileChangeHandler(script_to_watch)

    # 创建观察者
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=True)

    # 启动观察者
    print(f"开始监控目录: {path_to_watch}")
    print(f"监控脚本: {script_to_watch}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n停止监控...")

    observer.join()

    # 清理进程
    if event_handler.process:
        event_handler.process.terminate()
        event_handler.process.wait()


if __name__ == "__main__":
    main()
