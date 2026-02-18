import pygame
import sys
import json

class DisplayManager:
    def __init__(self, width=480, height=320):
        pygame.init()
        with open("config.json", 'r') as f:
            self.config = json.load(f)
            
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("IRIS Virtual Display")
        self.font = pygame.font.SysFont("Consolas", 20)
        self.clock = pygame.time.Clock()
        
        # Animasyon için barların mevcut görsel değerleri (Hemen değişmemesi için)
        self.visual_cpu = 0.0
        self.visual_battery = 0.0
        
        self.state_colors = {k: tuple(v) for k, v in self.config["colors"].items()}

    def draw_bar(self, x, y, width, height, percent, label, color):
        """Master Plan 12: Akıcı barlar için yardımcı fonksiyon"""
        # Dış çerçeve
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, width, height), 2)
        # Doluluk kısmı
        fill_width = (percent / 100) * (width - 4)
        pygame.draw.rect(self.screen, color, (x + 2, y + 2, fill_width, height - 4))
        # Etiket
        text = self.font.render(f"{label}: {int(percent)}%", True, (255, 255, 255))
        self.screen.blit(text, (x, y - 25))

    def update_display(self, data):
        dt = self.clock.tick(60) / 1000.0 
        
        # Animasyon yumuşatma (Lerp)
        lerp_speed = 50.0 
        self.visual_cpu += (data.get("cpu_usage", 0) - self.visual_cpu) * (lerp_speed * dt / 10)
        self.visual_battery = data.get("battery", 0)

        # Arka plan rengi
        current_state = data.get("STATE", "IDLE")
        self.screen.fill(self.state_colors.get(current_state, (0, 0, 0)))

        # 1. Üst Bilgi Satırı (Tarih/Saat ve Durum) 
        timestamp = data.get("timestamp", "")
        time_text = self.font.render(f"{timestamp}", True, (200, 200, 200))
        self.screen.blit(time_text, (20, 10))

        # 2. Barlar (Orta Bölüm)
        # CPU Barı
        self.draw_bar(50, 80, 380, 25, self.visual_cpu, "CPU LOAD", (0, 200, 255))
        # Pil Barı 
        self.draw_bar(50, 160, 380, 25, self.visual_battery, "BATTERY", (0, 255, 100))

        # 3. Alt Bilgi Paneli (Durum ve Detaylar) 
        pygame.draw.line(self.screen, (100, 100, 100), (20, 240), (460, 240), 2)
        
        state_text = self.font.render(f"MODE: {current_state}", True, (255, 255, 255))
        self.screen.blit(state_text, (20, 260))
        
        # Ekstra bilgi (Opsiyonel: Master Plan 16'daki uygulama ismi için yer açtık)
        app_text = self.font.render("System: Healthy", True, (150, 150, 150))
        self.screen.blit(app_text, (20, 290))
            
        pygame.display.flip()
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()