import json
import time # Zaman kontrolü için ekledik
from utils.logger import iris_logger # Log mekanizmasını içeri alıyoruz

class IrisState:
    IDLE = "IDLE"     # Sakin, düşük kaynak kullanımı
    BUSY = "BUSY"     # Yüksek performans, yoğun çalışma
    ALERT = "ALERT"   # Kritik durum (Düşük pil vb.)

class StateMachine:
    def __init__(self, config_path="config.json"):
        # Master Plan 4: Ayarların dış dosyadan okunması
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Dosya bulunamazsa varsayılan değerleri kullan
            self.config = {
                "thresholds": {"cpu_busy": 70, "battery_alert": 20}
            }
        
        self.current_state = IrisState.IDLE
        iris_logger.info("State Machine başlatıldı. İlk durum: IDLE")
        

class StateMachine:
    def __init__(self, config_path="config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.current_state = IrisState.IDLE
        self.last_state_change_time = 0
        self.min_state_duration = 2.0  # Bir durumun loglanması için en az 2 saniye sürmesi lazım

    def update(self, data):
        thresh = self.config["thresholds"]
        
        # 1. Ham hesaplama (O anki verilere göre olması gereken durum)
        if data['battery'] < thresh["battery_alert"]:
            calculated_state = IrisState.ALERT
        elif data['cpu_usage'] > thresh["cpu_busy"]:
            calculated_state = IrisState.BUSY
        else:
            calculated_state = IrisState.IDLE
            
        # 2. KARAR SÜZGECİ: Durum değişti mi?
        if calculated_state != self.current_state:
            now = time.time()
            # Anlık zıplamaları engellemek için zaman kontrolü
            if (now - self.last_state_change_time) > self.min_state_duration:
                iris_logger.info(
                    f"DURUM DEĞİŞTİ: {self.current_state} -> {calculated_state} | "
                    f"CPU: %{data['cpu_usage']} | Pil: %{data['battery']}"
                )
                self.current_state = calculated_state
                self.last_state_change_time = now

        return self.current_state