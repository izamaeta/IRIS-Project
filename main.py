import time
from agents.system_monitor import SystemMonitor
from core.display_manager import DisplayManager
from core.state_machine import StateMachine

def main():
    monitor = SystemMonitor()
    display = DisplayManager()
    state_machine = StateMachine()

    # Simülasyon için: Bağlantı durumu (True=Açık, False=Sleep Modu)
    is_connected = True

    while True:
        display.check_events()
        
        stats = monitor.get_stats()
        current_state = state_machine.update(stats, is_connected)
        stats["STATE"] = current_state
        
        display.update_display(stats)
        time.sleep(0.01) # Akıcılık için kısa bekleme

if __name__ == "__main__":
    main()