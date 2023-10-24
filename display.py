# Copyright (C) 2023 Timothy Gerla
# Distributed under the MIT license, see LICENSE.md

import pygame
import time

import ST7789 as ST7789
from PIL import Image, ImageDraw, ImageFont

SCREEN_WIDTH = 240 
SCREEN_HEIGHT = 240

# implement an abstract display class that will be used by the main loop
class Display:
    def __init__(self, w = SCREEN_WIDTH, h = SCREEN_HEIGHT):
        self.SCREEN_WIDTH = w
        self.SCREEN_HEIGHT = h

    def loop(self, drum_machine):
        raise NotImplementedError

class ST7735RDisplay(Display):
    display = None
    app_group = None

    def __init__(self, w = SCREEN_WIDTH, h = SCREEN_HEIGHT):
        super().__init__(w, h)

        self.display = ST7789.ST7789(
            height = h,
            width = w,
            rotation=0,
            port=0,
            cs=0,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
            dc=25,
            rst=27,
            backlight=24,               # 18 for back BG slot, 19 for front BG slot.
            spi_speed_hz=80 * 1000 * 1000,
            offset_left=0,
            offset_top=0
        )

        self.regularFont = ImageFont.truetype("fonts/NotoSans-Regular.ttf", 24) 
        self.boldFont = ImageFont.truetype("fonts/NotoSans-Bold.ttf", 32)
        self.smallBoldFont = ImageFont.truetype("fonts/NotoSans-Bold.ttf", 20)

        self.background = Image.open("assets/background.png")
        self.background.putalpha(Image.new("1", self.background.size, 128))
        self.display.begin()
    
        self.display.display(self.background)

    def loop(self, drum_machine):
        i = Image.new("RGB", (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), (0, 0, 0))
        i.paste(self.background)
        d = ImageDraw.Draw(i)

        self._draw_pattern_name(drum_machine, d)
        self._draw_tempo_display(drum_machine, d)
        self._draw_pattern_display(drum_machine, d)
        self._draw_measures(drum_machine, d)
        self._draw_beats(drum_machine, d)
        self.display.display(i)

    def _draw_pattern_name(self, drum_machine, d):
        d.text((10, 150), drum_machine.get_current_pattern_name(), font=self.regularFont, fill=(255, 255, 255))

    def _draw_tempo_display(self, drum_machine, d):
        d.text((174, 14), "%d" % drum_machine.tempo, font=self.regularFont, fill=(255, 255, 255))

    def _draw_pattern_display(self, drum_machine, d):
        d.text((34, 30), "%d" % drum_machine.current_pattern_idx, font=self.boldFont, fill=(0, 0, 0))

    def _draw_measures(self, drum_machine, d):
        for i, m in enumerate(drum_machine._current_pattern["measures"]):
            if m == drum_machine.current_measure:
                color = (255, 255, 255)
                if drum_machine.measure_changing and drum_machine.beat % 2:
                    color = (128, 128, 128)
            else:
                color = (128, 128, 128)

            d.text((i*22+19, 85), "%s" % m, font=self.smallBoldFont, fill=color)

    def _draw_beats(self, drum_machine, d):
        for i in range(0, drum_machine.pattern_length):
            bar_width = 8
            bar_spacing = 6
            bar_height = 20
            bar_y_position = self.SCREEN_HEIGHT - bar_height - 10

            x = 8 + i * (bar_width+bar_spacing)
            y = bar_y_position
            x2 = x + bar_width
            y2 = y + bar_height
            d.rectangle([x, y, x2, y2], outline=(0, 0, 0), fill=(0, 0, 0))

            if i == drum_machine.beat:
                d.rectangle([x, y, x2, y2], outline=(0, 0, 0), fill=(0, 255, 255))
            
        # draw the time signature display
        d.text((self.SCREEN_WIDTH/2-18, 40), "%s" % drum_machine.pattern_signature, font=self.regularFont, fill=(225, 225, 225))

        if not drum_machine.beat % 4 and drum_machine.state == "playing":
            x1 = self.SCREEN_WIDTH/2 - 4
            y1 = 32 - 4
            x2 = self.SCREEN_WIDTH/2 + 4
            y2 = 32 + 4
            d.ellipse([x1, y1, x2, y2], outline=(255, 255, 0), fill=(255, 255, 0))

class PyGameDisplay(Display):
    BACKGROUND_BITMAP = "assets/background.png"
    SPLASH_BITMAP = None # "assets/splash.jpg"

    def __init__(self, w = SCREEN_WIDTH, h = SCREEN_HEIGHT):
        super().__init__(w, h)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.pattern_font = pygame.font.Font(None, 22)
        self.tempo_font = pygame.font.Font(None, 28)
        self.tempo_font.bold = True
        self.measure_font = pygame.font.Font(None, 18)
        self.measure_font.bold = True
        self.running = True

        self.background = pygame.image.load(self.BACKGROUND_BITMAP)

        if self.SPLASH_BITMAP:
            self.splash = pygame.image.load(self.SPLASH_BITMAP)
            self.startup_timer = 60
        else:
            self.startup_timer = 0


    def _draw_pattern_name(self, drum_machine):
        # draw text of the current pattern name
        text = self.pattern_font.render("%s" % drum_machine.get_current_pattern_name(), True, "white")
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT - 36))
        self.screen.blit(text, text_rect)

    def _draw_tempo_display(self, drum_machine):
        text = self.tempo_font.render("%r" % drum_machine.tempo, True, "white")
        text_rect = text.get_rect(topleft=(self.SCREEN_WIDTH-54, 16))
        self.screen.blit(text, text_rect)

    def _draw_pattern_display(self, drum_machine):
        text = self.tempo_font.render("%r" % drum_machine.current_pattern_idx, True, "black")
        text_rect = text.get_rect(center=(48/2+10, 44))
        self.screen.blit(text, text_rect)

    def _draw_measures(self, drum_machine):
        for i, m in enumerate(drum_machine._current_pattern["measures"]):
            if m == drum_machine.current_measure:
                color = "white"
                if drum_machine.measure_changing and drum_machine.beat % 2:
                    color = "darkgray"
            else:
                color = "darkgray"


            text = self.measure_font.render("%s" % m, True, color)
            text_rect = text.get_rect(topleft=(i*14+16, 63))
            self.screen.blit(text, text_rect)

    def _draw_beats(self, drum_machine):
        for i in range(0, drum_machine.pattern_length):
            bar_width = 6
            bar_spacing = 3
            bar_height = 10
            bar_y_position = self.SCREEN_HEIGHT - bar_height - 4

            pygame.draw.rect(self.screen, "black", pygame.Rect((8 + i * (bar_width+bar_spacing)), bar_y_position, bar_width, bar_height), border_radius=0)
            if i == drum_machine.beat:
                pygame.draw.rect(self.screen, "cyan", pygame.Rect((8 + i * (bar_width+bar_spacing)), bar_y_position, bar_width, bar_height), border_radius=0)
            
        # draw the time signature display
        text = self.pattern_font.render("%s" % drum_machine.pattern_signature, True, "white")
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH/2, 24))
        self.screen.blit(text, text_rect)

        if not drum_machine.beat % 4 and drum_machine.state == "playing":
            pygame.draw.circle(self.screen, "yellow", (self.SCREEN_WIDTH/2, 40), 4)

    def capture_screenshot(self):
        print("Screenshot saved")
        pygame.image.save(self.screen, "screenshot.png")

    def loop(self, drum_machine):
        if self.startup_timer:
            self.startup_timer -= 1
            self.screen.fill("black")
            if self.startup_timer < 20:
                self.splash.set_alpha((self.startup_timer * 12 + 1))
            self.screen.blit(self.splash, (0, 0))
        else:
            self.screen.blit(self.background, (0, 0))
            self._draw_pattern_name(drum_machine)
            self._draw_tempo_display(drum_machine)
            self._draw_pattern_display(drum_machine)
            self._draw_beats(drum_machine)
            self._draw_measures(drum_machine)

        pygame.display.flip()
