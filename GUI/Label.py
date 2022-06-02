import pygame


class Label:
    def __init__(self, screen, x, y, label):
        self.label_box = pygame.Surface((300, 40))
        self.background = pygame.Rect(0, 0, 200, 40)
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption('Box Test')
        self.label_box.blit(self.font.render(label, True, (48, 63, 159)), (0, 0))
        screen.blit(self.label_box, (x, y))
