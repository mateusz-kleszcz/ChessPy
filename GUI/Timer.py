import pygame


class Timer:
    def __init__(self, screen, time, height):
        self.time = time
        self.timer_box = pygame.Surface((200, 40))
        self.background = pygame.Rect(0, 0, 200, 40)
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption('Box Test')
        self.timer_box.blit(self.font.render(self.get_time(), True, (255, 255, 0)), (0, 0))
        screen.blit(self.timer_box, (800, height))

    def get_time(self):
        minutes = int(self.time / (60 * 1000))
        if minutes < 10: minutes = f"0{minutes}"
        seconds = int(self.time / 1000) % 60
        if seconds < 10: seconds = f"0{seconds}"
        return f"{minutes}:{seconds}"
