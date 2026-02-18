import psutil
import time

class SystemMonitor:
    def get_stats(self):
        return {
            "cpu_usage": psutil.cpu_percent(),
            "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else 100,
            "timestamp": time.strftime("%H:%M:%S | %d.%m.%Y")
        }