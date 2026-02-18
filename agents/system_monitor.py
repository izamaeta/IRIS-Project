import psutil
import time
import win32gui
import win32process
import os
from PIL import ImageGrab

class SystemMonitor:
    def __init__(self):
        self.last_external_app = "MASAÜSTÜ"
        self.last_stats = {"cpu_usage": 0, "battery": 100}
        self.last_stats_time = 0
        self.my_pid = os.getpid()
        self.current_dynamic_color = [100, 100, 100]

    def _get_dominant_color(self):
        try:
            img = ImageGrab.grab(bbox=(10, 10, 60, 60))
            img = img.resize((1, 1))
            return list(img.getpixel((0, 0)))
        except:
            return [40, 40, 60]

    def get_active_window_name(self):
        try:
            window = win32gui.GetForegroundWindow()
            if not window: return self.last_external_app

            _, pid = win32process.GetWindowThreadProcessId(window)
            
            # 1. Kendi işlemimizse veya geçersizse yoksay
            if pid == self.my_pid: return self.last_external_app

            try:
                proc = psutil.Process(pid)
                exe_name = proc.name().lower()
            except:
                return self.last_external_app

            title = win32gui.GetWindowText(window)
            
            # 2. Windows Sistem Arayüzlerini Filtrele (Takılmayı önleyen kritik liste)
            system_triggers = [
                "explorer.exe", "searchhost.exe", "shellexperiencehost.exe", 
                "startmenuexperiencehost.exe", "taskmgr.exe"
            ]
            
            ignored_titles = [
                "görev geçişi", "task switching", "cortana", "ara", 
                "action center", "işlem merkezi", "date and time", "saat ve tarih"
            ]

            # Eğer explorer.exe ise ama masaüstü değilse (Alt-Tab gibi bir arayüzse) yoksay
            if exe_name == "explorer.exe" and title != "":
                if any(x in title.lower() for x in ignored_titles):
                    return self.last_external_app

            if exe_name in system_triggers and not title:
                return self.last_external_app

            # 3. Her şey temizse veriyi güncelle
            clean_exe = exe_name.replace(".exe", "").upper()
            display_info = f"{clean_exe} | {title[:30]}"
            
            # Dinamik renk analizini sadece gerçek uygulama değişiminde yap
            if display_info != self.last_external_app:
                self.current_dynamic_color = self._get_dominant_color()
            
            self.last_external_app = display_info
            return display_info

        except Exception:
            return self.last_external_app

    def get_stats(self):
        now = time.time()
        active_app = self.get_active_window_name()

        if now - self.last_stats_time > 2.0:
            try:
                self.last_stats = {
                    "cpu_usage": psutil.cpu_percent(),
                    "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else 100
                }
            except: pass
            self.last_stats_time = now

        return {
            "cpu_usage": self.last_stats["cpu_usage"],
            "battery": self.last_stats["battery"],
            "active_app": active_app,
            "dynamic_color": self.current_dynamic_color
        }