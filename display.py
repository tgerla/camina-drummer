import pygame

class Display:
    SCREEN_WIDTH = 160
    SCREEN_HEIGHT = 128

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.pattern_font = pygame.font.Font(None, 22)
        self.tempo_font = pygame.font.Font(None, 28)
        self.tempo_font.bold = True
        self.running = True

    def _draw_pattern_name(self, drum_machine):
        # draw text of the current pattern name
        text = self.pattern_font.render("%s" % drum_machine.get_current_pattern_name(), True, "white")
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT - 36))
        self.screen.blit(text, text_rect)

    def _draw_tempo_display(self, drum_machine):
        pygame.draw.rect(self.screen, "white", pygame.Rect(self.SCREEN_WIDTH-60, 12, 48, 44), border_radius=3)
        pygame.draw.rect(self.screen, "black", pygame.Rect(self.SCREEN_WIDTH-60, 12, 48, 28), border_radius=3)
        pygame.draw.rect(self.screen, "white", pygame.Rect(self.SCREEN_WIDTH-60, 12, 48, 28), width = 2, border_radius=3)
        text = self.tempo_font.render("%r" % drum_machine.tempo, True, "white")
        text_rect = text.get_rect(topleft=(self.SCREEN_WIDTH-54, 16))
        self.screen.blit(text, text_rect)
        text = self.pattern_font.render("bpm", True, "black")
        text_rect = text.get_rect(topleft=(self.SCREEN_WIDTH-52, 38))
        self.screen.blit(text, text_rect)

    def _draw_pattern_display(self, drum_machine):
        pygame.draw.rect(self.screen, "white", pygame.Rect(12, 12, 48, 44), border_radius=3)
        text = self.tempo_font.render("%r" % drum_machine.current_pattern_idx, True, "black")
        text_rect = text.get_rect(center=(48/2+10, 44))
        self.screen.blit(text, text_rect)
        text = self.pattern_font.render("PTN", True, "black")
        text_rect = text.get_rect(center=(48/2+10, 26))
        self.screen.blit(text, text_rect)

    def _draw_beats(self, drum_machine):
        for i in range(0, drum_machine.pattern_length):
            bar_width = 6
            bar_spacing = 3
            bar_height = 10
            bar_y_position = self.SCREEN_HEIGHT - bar_height -4 

            pygame.draw.rect(self.screen, "black", pygame.Rect((8 + i * (bar_width+bar_spacing)), bar_y_position, bar_width, bar_height), border_radius=0)
            if i == drum_machine.beat:
                pygame.draw.rect(self.screen, "white", pygame.Rect((8 + i * (bar_width+bar_spacing)), bar_y_position, bar_width, bar_height), border_radius=0)
            
        # draw the time signature display
        text = self.pattern_font.render("%s" % drum_machine.pattern_signature, True, "white")
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH/2, 24))
        self.screen.blit(text, text_rect)

        if not drum_machine.beat % 4 and drum_machine.state == "playing":
            pygame.draw.circle(self.screen, "green", (self.SCREEN_WIDTH/2, 40), 4)

    def loop(self, drum_machine):
        self.screen.fill("white")
        pygame.draw.rect(self.screen, "black", pygame.Rect(0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT-20),
                         border_radius=3, border_bottom_left_radius=0, border_bottom_right_radius=0)
        self._draw_pattern_name(drum_machine)
        self._draw_tempo_display(drum_machine)
        self._draw_pattern_display(drum_machine)
        self._draw_beats(drum_machine)

        pygame.display.flip()
        self.clock.tick(60)

        return self.running