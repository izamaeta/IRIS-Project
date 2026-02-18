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
        
        # Akıcı barlar için visual değerler
        self.visual_cpu = 0.0
        self.visual_bat = 0.0
        
        self.eye_animation_timer = 0
        self.overlay_alpha = 0
        self.state_colors = {k: tuple(v) for k, v in self.config["colors"].items()}

    def draw_bar(self, x, y, width, height, percent, label, color):
        """Barları çerçeveli ve etiketli çizer"""
        # Çerçeve
        pygame.draw.rect(self.screen, (120, 120, 120), (x, y, width, height), 1)
        # Doluluk
        fill_w = (percent / 100) * (width - 2)
        pygame.draw.rect(self.screen, color, (x + 1, y + 1, fill_w, height - 2))
        # Etiket ve Yüzde
        lbl = self.font.render(f"{label}: {int(percent)}%", True, (255, 255, 255))
        self.screen.blit(lbl, (x, y - 22))

    def update_display(self, data, reflex_event):
        dt = self.clock.tick(60) / 1000.0
        
        # 1. REFLEKS & ANIMASYON KONTROLÜ
        if reflex_event:
            self.eye_animation_timer = 0.4 # Refleks süresi

        # Barlar için pürüzsüz geçiş (Lerp)
        self.visual_cpu += (data.get("cpu_usage", 0) - self.visual_cpu) * (5.0 * dt)
        self.visual_bat += (data.get("battery", 0) - self.visual_bat) * (2.0 * dt)

        # Arka Plan ve Mod Rengi
        current_state = data.get("STATE", "IDLE")
        bg_color = list(self.state_colors.get(current_state, (0, 0, 0)))
        
        # Refleks anında arka planı anlık aydınlat
        if self.eye_animation_timer > 0:
            self.eye_animation_timer -= dt
            bg_color = [min(255, c + 40) for c in bg_color]

        self.screen.fill(bg_color)

        # 2. ÜST PANEL (Tarih & Saat)
        timestamp = data.get("timestamp", "")
        time_text = self.font.render(timestamp, True, (200, 200, 200))
        self.screen.blit(time_text, (20, 15))

        # 3. ORTA PANEL (Yağ gibi kayan barlar)
        self.draw_bar(50, 80, 380, 25, self.visual_cpu, "CPU LOAD", (0, 200, 255))
        self.draw_bar(50, 155, 380, 25, self.visual_bat, "BATTERY", (0, 255, 100))

        # 4. ALT PANEL (Mod ve Uygulama Bilgisi)
        pygame.draw.line(self.screen, (100, 100, 100), (20, 230), (460, 230), 1)
        
        state_text = self.font.render(f"STATUS: {current_state}", True, (255, 255, 255))
        self.screen.blit(state_text, (20, 245))
        
        app_name = data.get("active_app", "Desktop")
        if len(app_name) > 38: app_name = app_name[:35] + "..."
        app_text = self.font.render(f"APP: {app_name}", True, (170, 170, 170))
        self.screen.blit(app_text, (20, 275))

        # 5. REFLEKS UYARISI (Ekranın en altında küçük bir bildirim)
        if self.eye_animation_timer > 0:
            ref_msg = self.font.render(">> REFLEX: FOCUS CHANGED", True, (255, 255, 0))
            self.screen.blit(ref_msg, (20, 300))

        # 6. DEEP SLEEP OVERLAY
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