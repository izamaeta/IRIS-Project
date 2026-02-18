import time
from agents.system_monitor import SystemMonitor
from core.display_manager import DisplayManager

def main():
    # Katmanları ayağa kaldırıyoruz
    monitor = SystemMonitor()      # Sensor Layer 
    display = DisplayManager()     # Communication/Visual Layer 

    while True:
        # 1. Olayları kontrol et
        display.check_events()

        # 2. Veriyi topla (Sensor Layer)
        stats = monitor.get_stats() # [cite: 16]

        # 3. Veriyi ekrana gönder (Communication Layer)
        display.update_display(stats) # [cite: 34]

        # Master Plan 4: Optimizasyon [cite: 30]
        time.sleep(1)

if __name__ == "__main__":
    main()