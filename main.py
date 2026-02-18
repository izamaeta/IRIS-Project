import time
from agents.system_monitor import SystemMonitor
from core.display_manager import DisplayManager
from core.state_machine import StateMachine # Yeni katman

def main():
    monitor = SystemMonitor()
    display = DisplayManager()
    state_machine = StateMachine() # Beyni başlattık

    while True:
        display.check_events()
        
        # 1. Ham veriyi al (Sensor Layer)
        stats = monitor.get_stats()
        
        # 2. Veriyi yorumla ve durumu belirle (Logic Layer)
        current_state = state_machine.update(stats)
        
        # 3. Veriye durumu da ekle ki ekranda görelim
        stats["STATE"] = current_state
        
        # 4. Çiz (Communication Layer)
        display.update_display(stats)

        time.sleep(0.01) 

if __name__ == "__main__":
    main()