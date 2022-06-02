import pygame


class Button:
    def __init__(self, size_x, size_y, x, y, string, value, action, group):
        self.size_x = size_x
        self.size_y = size_y
        self.x = x
        self.y = y
        self.value = value
        self.button_box = pygame.Surface((size_x, size_y))
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 25)
        self.text = self.font.render(string, True, (207, 216, 220))
        pygame.display.set_caption('Box Test')
        self.button_box.blit(self.text, (10, 5))
        self.on_click = action
        self.group = group

    def add_to_scene(self, screen):
        self.button_box.blit(self.text, (10, 5))
        screen.blit(self.button_box, (self.x, self.y))

    def handle_click(self, engine):
        self.on_click(engine, self.value)
        if self.group is not None:
            if self.group.selected is not None:
                self.group.selected.unselect_button()
            self.select_button()
            self.group.selected = self

    def select_button(self):
        self.button_box.fill((211, 47, 47))
        self.button_box.blit(self.text, (10, 5))

    def unselect_button(self):
        self.button_box.fill((0, 0, 0))
        self.button_box.blit(self.text, (10, 5))

    def hide_button(self, screen):
        self.button_box.fill((0, 0, 0))
        screen.blit(self.button_box, (self.x, self.y))
