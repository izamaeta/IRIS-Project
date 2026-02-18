import time
import os
from agents.system_monitor import SystemMonitor
from core.display_manager import DisplayManager
from core.state_machine import StateMachine

def main():
    # 1. Başlangıç (Donanım ve Mantık Katmanları)
    monitor = SystemMonitor()
    display = DisplayManager()
    state_machine = StateMachine()

    print("--- IRIS Başlatıldı ---")
    print("İpucu: Farklı uygulamalara geçerek Refleks sistemini test et.")

    # Simülasyon için: Bağlantı durumu (True=Açık, False=Deep Sleep)
    is_connected = True 

    try:
        while True:
            # A. Kullanıcı etkileşimlerini kontrol et (Kapatma tuşu vb.)
            display.check_events()
            
            # B. Veri Toplama (Sensör Layer)
            stats = monitor.get_stats()
            
            # C. Karar Mekanizması (Logic Layer)
            # state_machine artık hem MOD'u hem de anlık REFLEKS'i döndürüyor
            current_state, reflex_trigger = state_machine.update(stats, is_connected)
            
            # Veriye güncel durumu ekle
            stats["STATE"] = current_state
            
            # D. Görselleştirme (Display Layer)
            display.update_display(stats, reflex_trigger)
            
            # E. DEBUG Paneli (Terminalde anlık ne gördüğünü izle)
            # Eğer her şey IDLE ise buradaki 'active_app' ismine bakıp config'e ekleme yapabilirsin.
            if reflex_trigger:
                print(f"[!] REFLEKS: Yeni uygulama algılandı -> {stats['active_app']}")
                print(f"[?] TAHMİN EDİLEN MOD: {current_state}")

            # Akıcılık için kısa bekleme (60 FPS hedefi için 0.01s yeterli)
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nIRIS kapatılıyor. Loglar kaydedildi.")

if __name__ == "__main__":
    main()