import pygame


class Label:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.label_box = pygame.Surface((300, 40))
        self.background = pygame.Rect(0, 0, 200, 40)
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption('Box Test')

    def add_to_scene(self, label):
        self.label_box.blit(self.font.render(label, True, (211, 47, 47)), (0, 0))
        self.screen.blit(self.label_box, (self.x, self.y))

    def hide_label(self):
        self.label_box.fill((0, 0, 0))
        self.screen.blit(self.label_box, (self.x, self.y))
