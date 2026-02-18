import psutil
import time

class SystemMonitor:
    def __init__(self):
        # Master Plan 2.1: Sistem verilerini toplama hazırlığı [cite: 15, 16]
        pass

    def get_stats(self):
        """CPU ve Pil bilgilerini sözlük (JSON dostu) yapısında döndürür[cite: 22]."""
        return {
            "cpu_usage": psutil.cpu_percent(),
            "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else 100,
            "timestamp": time.ctime()
        }