import psutil
import time
import win32gui

class SystemMonitor:
    def __init__(self):
        self.last_external_app = "Desktop"

    def get_active_window_name(self):
        try:
            window = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(window)
            
            # Yoksayılacak pencere başlıkları
            ignored = ["pygame window", "IRIS Virtual Display", "Task Switching", "Görev Geçişi"]
            
            if not title or any(x in title for x in ignored):
                return self.last_external_app
            
            self.last_external_app = title
            return title
        except Exception:
            return self.last_external_app

    def get_stats(self):
        return {
            "cpu_usage": psutil.cpu_percent(),
            "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else 100,
            "timestamp": time.strftime("%H:%M:%S | %d.%m.%Y"),
            "active_app": self.get_active_window_name()
        }