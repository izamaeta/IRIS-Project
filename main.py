import time
import sys
from agents.system_monitor import SystemMonitor
from core.display_manager import DisplayManager
from core.state_machine import StateMachine

def main():
    # 1. Başlatma (Sistem, Karakter ve Mantık)
    monitor = SystemMonitor()
    display = DisplayManager()
    state_machine = StateMachine()

    print("--- IRIS Core Aktif ---")
    print("[LOG] Bukalemun modülü devrede: Renkler ekran içeriğine göre belirlenecek.")

    # Simülasyon Değişkeni
    is_connected = True 

    try:
        while True:
            # A. Pygame Olaylarını Kontrol Et (Kapatma tuşu vb.)
            display.check_events()
            
            # B. Veri Toplama (Uygulama Adı + Dinamik Renk)
            stats = monitor.get_stats()
            
            # C. Karar Mekanizması (State, Reflex ve Glitch tespiti)
            current_state, reflex_trigger, glitch_trigger = state_machine.update(stats, is_connected)
            
            # Durum bilgisini stats içine mühürle
            stats["STATE"] = current_state
            
            # D. Görselleştirme
            # stats içinde gelen 'dynamic_color' artık DisplayManager tarafından kullanılıyor.
            display.update_display(stats, reflex_trigger, glitch_trigger)
            
            # E. Terminal Bilgilendirme (Sadece değişimlerde)
            if glitch_trigger:
                print(f"[!] HIZLI GEÇİŞ: IRIS'in başı döndü!")
            elif reflex_trigger:
                print(f"[*] ODAK: {stats['active_app']}")

            # Performans ve akıcılık için döngü süresi (Config polling_interval'e uygun)
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n[!] IRIS uyku moduna alınıyor...")
    except Exception as e:
        print(f"\n[X] Beklenmedik bir hata oluştu: {e}")
    finally:
        # Kaynakları temizle
        sys.exit()

if __name__ == "__main__":
    main()