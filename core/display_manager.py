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
        self.font = pygame.font.SysFont("Consolas", 18)
        self.clock = pygame.time.Clock()
        
        # Animasyon Değişkenleri
        self.visual_cpu = 0.0
        self.visual_bat = 0.0
        self.eye_y_open = 0.7
        self.target_y_open = 0.7
        self.eye_animation_timer = 0
        self.overlay_alpha = 0
        self.state_colors = {k: tuple(v) for k, v in self.config["colors"].items()}

    def draw_eyes(self, x, y, size, state):
        """Daha dost canlısı, dijital/neon göz tasarımı (Rounded Rects)"""
        
        # 1. Duruma göre hedef açıklık ve renk belirle
        eye_color = (255, 255, 255) # Varsayılan Beyaz
        
        if state == "CODING" or state == "BUSY":
            self.target_y_open = 0.25 # Odaklanmış/Hacker modu
            eye_color = (0, 255, 255) # Cyan
        elif state == "ALERT":
            self.target_y_open = 1.1  # Şaşkın/Uyarı modu
            eye_color = (255, 100, 100) # Soft Kırmızı
        elif state == "SLEEP":
            self.target_y_open = 0.05 # Kapalı
            eye_color = (100, 100, 100) # Gri
        else:
            self.target_y_open = 0.6  # Standart bakış
            eye_color = (200, 255, 200) # Hafif Yeşilimsi

        # 2. Yumuşak Geçiş (Lerp) ve Göz Kırpma
        if self.eye_animation_timer > 0:
            current_eye_h = 0.05
        else:
            self.eye_y_open += (self.target_y_open - self.eye_y_open) * 0.1
            current_eye_h = self.eye_y_open

        # 3. Çizim (Dijital Bloklar)
        rect_width = size * 1.3
        rect_height = size * current_eye_h
        # Köşe yumuşatma (LVGL uyumlu)
        corner_radius = int(rect_height / 2) if rect_height > 10 else 2

        for offset in [-75, 75]: # Gözler arası mesafe
            eye_rect = pygame.Rect(x + offset - rect_width/2, y - rect_height/2, rect_width, rect_height)
            
            # Ana Neon Blok
            pygame.draw.rect(self.screen, eye_color, eye_rect, border_radius=corner_radius)
            
            # İç Parlama (Derinlik hissi için hafif açık renk çerçeve)
            if current_eye_h > 0.3:
                inner_color = (min(255, eye_color[0]+40), min(255, eye_color[1]+40), min(255, eye_color[2]+40))
                pygame.draw.rect(self.screen, inner_color, eye_rect.inflate(-4, -4), 1, border_radius=corner_radius)

    def draw_bar(self, x, y, width, height, percent, label, color):
        pygame.draw.rect(self.screen, (80, 80, 80), (x, y, width, height), 1)
        fill_w = (percent / 100) * (width - 2)
        pygame.draw.rect(self.screen, color, (x + 1, y + 1, fill_w, height - 2))
        lbl = self.font.render(f"{label}: {int(percent)}%", True, (255, 255, 255))
        self.screen.blit(lbl, (x, y - 22))

    def update_display(self, data, reflex_event):
        dt = self.clock.tick(60) / 1000.0
        
        if reflex_event:
            self.eye_animation_timer = 0.3

        # Değerleri yumuşat
        self.visual_cpu += (data.get("cpu_usage", 0) - self.visual_cpu) * (5.0 * dt)
        self.visual_bat += (data.get("battery", 0) - self.visual_bat) * (2.0 * dt)

        current_state = data.get("STATE", "IDLE")
        bg_color = list(self.state_colors.get(current_state, (0, 0, 0)))
        
        if self.eye_animation_timer > 0:
            self.eye_animation_timer -= dt

        self.screen.fill(bg_color)

        # 1. Gözler (Dijital Karakter)
        self.draw_eyes(240, 70, 45, current_state)

        # 2. Barlar (Veri Katmanı)
        self.draw_bar(50, 145, 380, 20, self.visual_cpu, "CPU LOAD", (0, 200, 255))
        self.draw_bar(50, 200, 380, 20, self.visual_bat, "BATTERY", (0, 255, 100))

        # 3. Bilgiler (Text Layer)
        self.screen.blit(self.font.render(data.get("timestamp", ""), True, (150, 150, 150)), (20, 10))
        self.screen.blit(self.font.render(f"MODE: {current_state}", True, (255, 255, 255)), (20, 250))
        
        app_name = data.get("active_app", "Desktop")
        self.screen.blit(self.font.render(f"APP: {app_name[:35]}", True, (120, 120, 120)), (20, 280))

        # 4. Deep Sleep Overlay
        if current_state == "SLEEP":
            self.overlay_alpha = min(255, self.overlay_alpha + 150 * dt)
        else:
            self.overlay_alpha = max(0, self.overlay_alpha - 150 * dt)

        if self.overlay_alpha > 0:
            fade = pygame.Surface((480, 320))
            fade.set_alpha(int(self.overlay_alpha))
            fade.fill((0, 0, 0))
            self.screen.blit(fade, (0, 0))

        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
