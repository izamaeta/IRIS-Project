import pygame
import sys
import json # JSON dosyasını okumak için şart

class DisplayManager:
    def __init__(self, width=480, height=320):
        pygame.init()
        
        # config.json dosyasını okuyoruz 
        with open("config.json", 'r') as f:
            self.config = json.load(f)
        
        # Master Plan'daki 3.5" ekran boyutlarını ayarlıyoruz [cite: 9]
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("IRIS Virtual Display")
        
        self.font = pygame.font.SysFont("Consolas", 24)
        self.clock = pygame.time.Clock() 
        
        self.bar_x = 0  
        
        # JSON'daki listeleri Pygame'in sevdiği tuple (demet) formatına çeviriyoruz
        self.state_colors = {k: tuple(v) for k, v in self.config["colors"].items()}

    def update_display(self, data):
        # 1. Delta Time Hesapla (milisaniyeyi saniyeye çeviriyoruz)
        # Bu değer, son kareden bu yana geçen süredir.
        dt = self.clock.tick(60) / 1000.0 

        # 2. Animasyon Mantığı (Master Plan 4: Pürüzsüz hareket)
        # Saniyede 100 piksel hızla sağa kayan bir çubuk
        self.bar_x += 100 * dt 
        if self.bar_x > 480: # Ekrandan çıkınca başa dön
            self.bar_x = 0

        # Geri kalan çizim işlemleri
        current_state = data.get("STATE", "IDLE")
        bg_color = self.state_colors.get(current_state, (0, 0, 0))
        self.screen.fill(bg_color)

        # Hareketli Çubuğu Çiz (Animasyonun kanıtı)
        pygame.draw.rect(self.screen, (255, 255, 255), (self.bar_x, 300, 50, 10))

        y_offset = 20
        for key, value in data.items():
            text = self.font.render(f"{key}: {value}", True, (255, 255, 255))
            self.screen.blit(text, (20, y_offset))
            y_offset += 40
            
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()