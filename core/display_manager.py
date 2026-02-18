import pygame
import sys

class DisplayManager:
    def __init__(self, width=480, height=320): # [cite: 9]
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("IRIS Virtual Display")
        self.font = pygame.font.SysFont("Consolas", 24)
        self.colors = {"BLACK": (0, 0, 0), "GREEN": (0, 255, 0)}

    def update_display(self, data):
        """Gelen veriyi ekrana çizer[cite: 12]."""
        self.screen.fill(self.colors["BLACK"])
        
        # Verileri alt alta yazdıralım
        y_offset = 20
        for key, value in data.items():
            text = self.font.render(f"{key}: {value}", True, self.colors["GREEN"])
            self.screen.blit(text, (20, y_offset))
            y_offset += 40
            
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()