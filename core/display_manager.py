import pygame
import sys
import json
import random
import math
import time

class DisplayManager:
    def __init__(self, width=480, height=320):
        pygame.init()
        with open("config.json", 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("IRIS Core")
        
        try:
            self.font = pygame.font.SysFont("Consolas", 12, bold=True)
            self.matrix_font = pygame.font.SysFont("Consolas", 10)
        except:
            self.font = pygame.font.SysFont("Arial", 12, bold=True)
            self.matrix_font = pygame.font.SysFont("Arial", 10)
            
        self.clock = pygame.time.Clock()
        self.eye_h, self.target_h = 0.0, 0.35
        self.glitch_offset, self.shake_timer = [0, 0], 0
        self.blink_timer, self.is_blinking = 0, False
        self.micro_move = [0, 0]
        
        self.colors = {k: tuple(v) for k, v in self.config["colors"].items()}
        self.current_bg = list(self.colors["IDLE"])
        self.current_eye_color = list(self.colors["GLOW_WHITE"])
        
        # --- Border ve Kontrast Takibi ---
        self.border_color = list(self.colors["GLOW_WHITE"])
        self.last_state = "IDLE"
        
        self.is_scanning = False
        self.scan_timer = 0
        self.particles = [] 
        self.matrix_columns = [0] * (width // 10)

    def _lerp_color(self, cur, target, speed=0.025):
        return [cur[i] + (target[i] - cur[i]) * speed for i in range(3)]

    def _get_contrast_color(self, color):
        # RGB değerlerini 255'ten çıkararak hızlıca zıt rengi alır
        return [255 - color[0], 255 - color[1], 255 - color[2]]

    def trigger_scan(self):
        self.is_scanning = True
        self.scan_timer = 0

    def _update_particles(self):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= p['decay']
            if p['life'] <= 0: self.particles.remove(p)

    def _get_element_params(self, color):
        r, g, b = color
        if r > g + 50 and r > b + 50:
            return {'vx': (-0.3, 0.3), 'vy': (0.5, 1.2), 'decay': 0.02, 'type': 'drop'}
        if g > r + 50 and g > b + 50:
            return {'vx': (-1.5, 1.5), 'vy': (0.2, 0.6), 'decay': 0.03, 'type': 'leaf'}
        if b > r + 50 and b > g + 50:
            return {'vx': (-0.1, 0.1), 'vy': (1.5, 3.0), 'decay': 0.05, 'type': 'ice'}
        if r > 100 and b > 100 and g < 100:
            return {'vx': (-2.0, 2.0), 'vy': (-1.0, 1.0), 'decay': 0.04, 'type': 'plasma'}
        return {'vx': (-2.5, 2.5), 'vy': (-2.0, 0.5), 'decay': 0.06, 'type': 'spark'}

    def draw_eyes(self, state, glitch_mode, base_color):
        if random.random() < 0.05:
            self.micro_move = [random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8)]
            
        x, y = 240 + self.glitch_offset[0] + self.micro_move[0], 120 + self.glitch_offset[1] + self.micro_move[1]
        size_w, size_h = 75, 60
        
        height_map = {"STARTUP": 0.05, "CODING": 0.28, "VSCODE": 0.25, "GEMINI": 0.35, "YOUTUBE": 0.30, "SLEEP": 0.02, "ALERT": 0.75}
        self.target_h = height_map.get(state, 0.35)

        if not self.is_blinking and random.random() < 0.005:
            self.is_blinking, self.blink_timer = True, 0
        if self.is_blinking:
            self.blink_timer += 0.20
            current_h = self.eye_h * (1 - math.sin(self.blink_timer * math.pi))
            if self.blink_timer >= 1.0: self.is_blinking = False
        else:
            self.eye_h += (self.target_h - self.eye_h) * 0.12
            current_h = self.eye_h

        # --- GÜNCEL: Sert Patlama ve Yumuşak Dönüş Mantığı ---
        if state != self.last_state:
            # Durum değiştiği AN (ilk kare): Rengi zıt kutba fırlat (Sert Patlama)
            self.border_color = self._get_contrast_color(base_color)
            self.last_state = state
        else:
            # Takip eden karelerde: Yeni renge (base_color) yumuşakça süzül
            # Hızı 0.08'den 0.05'e çektim ki o süzülme daha belirgin olsun
            self.border_color = self._lerp_color(self.border_color, base_color, 0.05)

        pulse = (math.sin(time.time() * 2.5) + 1) * 6
        
        for offset in [-100, 100]:
            rect = pygame.Rect(x + offset - (size_w/2), y - (size_h * current_h)/2, size_w, max(2, size_h * current_h))
            
            if state != "SLEEP":
                # Patlama etkisini artırmak için border kalınlığını inflate ile biraz daha belirgin yaptık
                # border_color şu an patlama anında kontrast renkte, sonra base_color'a sönüyor.
                pygame.draw.rect(self.screen, self.border_color, rect.inflate(10, 10), width=3, border_radius=12)

                # Glow Efekti (Mevcut)
                for i in range(3, 0, -1):
                    alpha = 15 // i
                    glow_surf = pygame.Surface((rect.width + i*14, rect.height + i*14), pygame.SRCALPHA)
                    p_color = [min(255, max(0, int(c + pulse))) for c in base_color]
                    pygame.draw.rect(glow_surf, (*p_color, alpha), (0, 0, glow_surf.get_width(), glow_surf.get_height()), border_radius=15 + i*2)
                    self.screen.blit(glow_surf, (rect.x - i*7, rect.y - i*7))

            # Ana Göz Katmanı
            pygame.draw.rect(self.screen, base_color, rect, border_radius=8)

            # Tarama ve Parçacık Mantığı (Aynen korundu)
            if self.is_scanning and current_h > 0.1:
                scan_y = rect.y + (rect.height * self.scan_timer)
                scan_line = pygame.Rect(rect.x, scan_y - 1, rect.width, 2)
                laser_color = [min(255, c + 100) for c in base_color]
                pygame.draw.rect(self.screen, laser_color, scan_line, border_radius=1)
                
                e = self._get_element_params(base_color)
                if random.random() < 0.6:
                    self.particles.append({
                        'x': random.randint(rect.left, rect.right), 'y': scan_y,
                        'vx': random.uniform(*e['vx']), 'vy': random.uniform(*e['vy']),
                        'life': 1.0, 'decay': e['decay'], 'color': laser_color, 'type': e['type']
                    })

    def update_display(self, data, reflex_event, glitch_mode):
        self.clock.tick(60)
        state = data.get("STATE", "IDLE")
        
        if reflex_event: self.trigger_scan()
        if self.is_scanning:
            self.scan_timer += 0.05
            if self.scan_timer >= 1.0: self.is_scanning = False
        self._update_particles()

        brand_color = self.colors.get(state, data.get("dynamic_color", self.colors["IDLE"]))
        bg_target = [int(c * 0.20) for c in brand_color]
        eye_target = [min(255, int(c * 1.5)) for c in brand_color]

        self.current_bg = self._lerp_color(self.current_bg, bg_target)
        self.current_eye_color = self._lerp_color(self.current_eye_color, eye_target)
        
        self.screen.fill(self.current_bg)
        
        # Mevcut Matrix Arka Plan Efekti (Startup modu için)
        if state == "STARTUP":
            for i in range(len(self.matrix_columns)):
                char = random.choice("01")
                txt = self.matrix_font.render(char, True, [int(c*0.3) for c in self.current_eye_color])
                self.screen.blit(txt, (i * 10, self.matrix_columns[i] * 10))
                if self.matrix_columns[i] * 10 > 320 or random.random() > 0.96: self.matrix_columns[i] = 0
                else: self.matrix_columns[i] += 1

        self.draw_eyes(state, glitch_mode, self.current_eye_color)
        
        # Mevcut Parçacık Çizimi
        for p in self.particles:
            if p['type'] == 'plasma':
                pygame.draw.circle(self.screen, p['color'], (int(p['x']), int(p['y'])), random.randint(1, 3))
            else:
                pygame.draw.rect(self.screen, p['color'], (int(p['x']), int(p['y']), 2, 2))
        
        # Mevcut Uygulama Bilgisi Yazısı
        if state not in ["SLEEP", "STARTUP"]:
            app_info = data.get("active_app", "").upper()
            if app_info:
                txt_color = [int(c * 0.7) for c in self.current_eye_color]
                txt = self.font.render(app_info, True, txt_color)
                self.screen.blit(txt, (465 - txt.get_width(), 295))
                
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()