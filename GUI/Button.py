import pygame


class Button:
    def __init__(self, size_x, size_y, x, y, string, value, action):
        self.size_x = size_x
        self.size_y = size_y
        self.x = x
        self.y = y
        self.value = value
        self.button_box = pygame.Surface((size_x, size_y))
        self.background = pygame.Rect(0, 0, size_x, size_y)
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption('Box Test')
        self.button_box.blit(self.font.render(string, True, (255, 255, 0)), (0, 0))
        self.on_click = action

    def add_to_scene(self, screen):
        screen.blit(self.button_box, (self.x, self.y))

    def handle_click(self, engine):
        self.on_click(engine, self.value)

    def hide_button(self):
        self.button_box.fill((0, 0, 0))