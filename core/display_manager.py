import pygame
import sys
import json

class DisplayManager:
    def __init__(self, width=480, height=320):
        pygame.init()
        with open("config.json", 'r') as f:
            self.config = json.load(f)
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("Consolas", 20)
        self.clock = pygame.time.Clock()
        self.visual_cpu = 0.0
        self.overlay_alpha = 0
        self.state_colors = {k: tuple(v) for k, v in self.config["colors"].items()}

    def draw_bar(self, x, y, width, height, percent, label, color):
        pygame.draw.rect(self.screen, (150, 150, 150), (x, y, width, height), 1)
        fill_width = (percent / 100) * (width - 2)
        pygame.draw.rect(self.screen, color, (x + 1, y + 1, fill_width, height - 2))
        lbl = self.font.render(f"{label}: {int(percent)}%", True, (255, 255, 255))
        self.screen.blit(lbl, (x, y - 22))

    def update_display(self, data):
        dt = self.clock.tick(60) / 1000.0
        current_state = data.get("STATE", "IDLE")

        # 1. Animasyon Yumuşatma (Lerp)
        self.visual_cpu += (data.get("cpu_usage", 0) - self.visual_cpu) * (5.0 * dt)
        
        # 2. Deep Sleep Kararma (Master Plan 31)
        if current_state == "SLEEP":
            self.overlay_alpha = min(255, self.overlay_alpha + 200 * dt)
        else:
            self.overlay_alpha = max(0, self.overlay_alpha - 200 * dt)

        # 3. Çizimler
        self.screen.fill(self.state_colors.get(current_state, (0, 0, 0)))
        self.screen.blit(self.font.render(data.get("timestamp", ""), True, (200, 200, 200)), (20, 10))
        self.draw_bar(50, 80, 380, 25, self.visual_cpu, "CPU LOAD", (0, 200, 255))
        self.draw_bar(50, 160, 380, 25, data.get("battery", 0), "BATTERY", (0, 255, 100))
        
        # Footer
        pygame.draw.line(self.screen, (80, 80, 80), (20, 240), (460, 240), 1)
        self.screen.blit(self.font.render(f"SYSTEM STATE: {current_state}", True, (255, 255, 255)), (20, 260))

        # 4. Fade Overlay
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