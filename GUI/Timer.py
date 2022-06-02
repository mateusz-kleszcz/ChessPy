import pygame


class Timer:
    def __init__(self, height, label):
        self.timer_box = pygame.Surface((200, 40))
        self.label = label
        self.height = height
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption('Box Test')

    def get_time(self, label, time):
        minutes = int(time / (60 * 1000))
        if minutes < 10: minutes = f"0{minutes}"
        seconds = int(time / 1000) % 60
        if seconds < 10: seconds = f"0{seconds}"
        return f"{label} {minutes}:{seconds}"

    def draw_timer(self, screen, time):
        self.timer_box = pygame.Surface((200, 40))
        self.timer_box.blit(self.font.render(self.get_time(self.label, time), True, (207, 216, 220)), (0, 0))
        screen.blit(self.timer_box, (800, self.height))

    def hide_timer(self, screen):
        self.timer_box.fill((0, 0, 0))
        screen.blit(self.timer_box, (800, self.height))
