import json
import time
from utils.logger import iris_logger

class StateMachine:
    def __init__(self, config_path="config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.current_state = "IDLE"
        self.last_app = ""
        self.potential_new_mode = None
        self.last_app_change_time = 0
        self.mode_delay = self.config["settings"].get("mode_switch_delay", 3.0)

    def update(self, data, is_connected=True):
        if not is_connected: 
            return self._change_state("SLEEP", data), False

        current_app = data.get("active_app", "").lower()
        reflex_event = False

        # 1. ANLIK REFLEKS (Görsel tepki için)
        if current_app != self.last_app:
            reflex_event = True
            self.last_app = current_app

        # 2. ZEKİ TAHMİN MEKANİZMASI (Heuristic Inference)
        target_mode = self._infer_target_mode(current_app, data)

        # 3. GECİKMELİ KARAR (Debounce - Stabilite için)
        now = time.time()
        final_state = self.current_state

        if target_mode != self.current_state:
            if target_mode != self.potential_new_mode:
                self.potential_new_mode = target_mode
                self.last_app_change_time = now
            
            if (now - self.last_app_change_time) >= self.mode_delay:
                final_state = self._change_state(target_mode, data)
        else:
            self.potential_new_mode = None

        return final_state, reflex_event

    def _infer_target_mode(self, app_name, data):
        # 1. KRİTİK: Batarya
        if data['battery'] < self.config["thresholds"]["battery_alert"]:
            return "ALERT"

        # 2. OTOMATİK TESPİT: Uzantılar (Zaten eklemiştik)
        coding_exts = [".py", ".cpp", ".js", ".java", ".sql", ".html", ".css", ".go", ".rs", ".ts"]
        if any(ext in app_name for ext in coding_exts):
            return "CODING"

        # 3. KATEGORİ REHBERİ (Daha geniş kapsamlı anahtar kelime taraması)
        for mode, keywords in self.config.get("categories", {}).items():
            # Sadece kelimeyi değil, içinde geçip geçmediğini daha esnek kontrol et
            if any(kw in app_name for kw in keywords):
                return mode

        # 4. AKTİF ÇALIŞMA TESPİTİ (Eğer hiçbir kategoriye girmiyorsa)
        # Orta düzey CPU kullanımı ve herhangi bir uygulama açıksa BUSY sayılabilir
        # IDLE sadece gerçekten hiçbir şey yapılmadığında (Masaüstü vb.) gözüksün
        if data['cpu_usage'] > self.config["thresholds"]["cpu_busy"]:
            return "BUSY"
        
        # Eğer bir uygulama ismi varsa ama kategorize edilemiyorsa 'ACTIVE' gibi ara bir mod da uydurabiliriz
        # Ama şimdilik IDLE kalsın, sadece kategorileri config'den artıracağız.
        return "IDLE"

    def _change_state(self, new_state, data):
        if new_state != self.current_state:
            iris_logger.info(f"MOD DEĞİŞTİ: {new_state} | Sebep: {data.get('active_app')}")
            self.current_state = new_state
        return self.current_state