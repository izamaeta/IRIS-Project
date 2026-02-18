import json
import time
from utils.logger import iris_logger

class StateMachine:
    def __init__(self, config_path="config.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.current_state = "STARTUP"
        self.last_app = ""
        self.last_app_change_time = time.time()
        # Sekme geçişleri için gecikmeyi biraz daha kısalttık
        self.mode_delay = self.config["settings"].get("mode_switch_delay", 1.0)

    def update(self, data, is_connected=True):
        if not is_connected: return "SLEEP", False, False

        current_info = data.get("active_app", "").lower()
        now = time.time()
        reflex_event = False
        glitch_mode = False

        if current_info != self.last_app:
            if (now - self.last_app_change_time) < self.config["settings"].get("glitch_threshold", 0.3):
                glitch_mode = True
            reflex_event = True
            self.last_app = current_info
            self.last_app_change_time = now

        # Alt Uygulama/Sekme Analizi: Config'deki hiyerarşiye göre mod tespiti
        target_mode = self._infer_target_mode(current_info, data)

        if self.current_state == "STARTUP":
            if (now - self.last_app_change_time) > 3.0:
                self.current_state = "IDLE"
            return self.current_state, reflex_event, glitch_mode

        # Mod geçişi: Eğer hedef mod mevcut moddan farklıysa süre kontrolü yap
        if target_mode != self.current_state:
            if (now - self.last_app_change_time) >= self.mode_delay:
                self.current_state = target_mode
                iris_logger.info(f"MOD GEÇİŞİ: {target_mode}")

        return self.current_state, reflex_event, glitch_mode

    def _infer_target_mode(self, app_info, data):
        # 1. Kritik Durumlar (Pil vb.)
        if data['battery'] < self.config["thresholds"]["battery_alert"]:
            return "ALERT"

        # 2. Hiyerarşik Kategori Taraması
        # Config içindeki sıra çok önemli; özel uygulamalar her zaman üstte olmalı
        for mode, keywords in self.config.get("categories", {}).items():
            if any(kw in app_info for kw in keywords):
                return mode

        # 3. Varsayılan
        return "IDLE"