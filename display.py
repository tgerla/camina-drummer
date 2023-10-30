# Copyright (C) 2023 Timothy Gerla
# Distributed under the MIT license, see LICENSE.md

import pygame

try:
    import ST7789 as ST7789
except ImportError:
    print("ST7789 display not found")
    PLATFORM = "desktop"
else:
    PLATFORM = "pi"

from PIL import Image, ImageDraw, ImageFont

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240


# implement an abstract display class that will be used by the main loop
class Display:
    def __init__(self):
        self._setup_fonts()
        self._setup_display()

        self.background = Image.open("assets/background.png")
        self.background.putalpha(Image.new("1", self.background.size, 128))
        self.buffer = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0, 0))

    def _setup_display(self):
        raise NotImplementedError

    def _setup_fonts(self):
        self.regularFont = ImageFont.truetype("fonts/NotoSans-Regular.ttf", 24)
        self.boldFont = ImageFont.truetype("fonts/NotoSans-Bold.ttf", 32)
        self.smallBoldFont = ImageFont.truetype("fonts/NotoSans-Bold.ttf", 20)

    def flip(self, image):
        raise NotImplementedError

    def loop(self, drum_machine):
        self.buffer.paste(self.background)
        d = ImageDraw.Draw(self.buffer)

        self._draw_pattern_name(drum_machine, d)
        self._draw_tempo_display(drum_machine, d)
        self._draw_pattern_display(drum_machine, d)
        self._draw_measures(drum_machine, d)
        #        self._draw_beats(drum_machine, d)
        self.flip(None)

    def _draw_pattern_name(self, drum_machine, d):
        d.text(
            (10, 140),
            drum_machine.get_current_pattern_name(),
            font=self.smallBoldFont,
            fill=(255, 255, 255),
        )

    def _draw_tempo_display(self, drum_machine, d):
        d.text(
            (170, 18),
            "%d" % drum_machine.tempo,
            font=self.regularFont,
            fill=(255, 255, 255),
        )

        if not drum_machine.beat % 4 and drum_machine.state == "playing":
            tsColor = (255, 255, 0)
        else:
            tsColor = (128, 128, 128)

        d.text(
            (SCREEN_WIDTH / 2 - 8, 30),
            "%s" % drum_machine.pattern_signature,
            font=self.regularFont,
            fill=tsColor,
        )

    def _draw_pattern_display(self, drum_machine, d):
        d.text(
            (160, 190),
            "%d" % drum_machine.current_pattern_idx,
            font=self.boldFont,
            fill=(255, 255, 255),
        )

    def _draw_measures(self, drum_machine, d):
        for i, m in enumerate(drum_machine._current_pattern["measures"]):
            if m == drum_machine.current_measure:
                color = (255, 255, 255)
                if drum_machine.measure_changing and drum_machine.beat % 2:
                    color = (128, 128, 128)
            else:
                color = (128, 128, 128)

            d.text((i * 22 + 17, 189), "%s" % m, font=self.smallBoldFont, fill=color)

    def _draw_beats(self, drum_machine, d):
        for i in range(0, drum_machine.pattern_length):
            bar_width = 8
            bar_spacing = 6
            bar_height = 20
            bar_y_position = SCREEN_HEIGHT - bar_height - 10

            x = 8 + i * (bar_width + bar_spacing)
            y = bar_y_position
            x2 = x + bar_width
            y2 = y + bar_height
            d.rectangle([x, y, x2, y2], outline=(0, 0, 0), fill=(0, 0, 0))

            if i == drum_machine.beat:
                d.rectangle([x, y, x2, y2], outline=(0, 0, 0), fill=(0, 255, 255))

        if not drum_machine.beat % 4 and drum_machine.state == "playing":
            x1 = SCREEN_WIDTH / 2 - 4
            y1 = 32 - 4
            x2 = SCREEN_WIDTH / 2 + 4
            y2 = 32 + 4
            d.ellipse([x1, y1, x2, y2], outline=(255, 255, 0), fill=(255, 255, 0))


class ST7735RDisplay(Display):
    display = None
    app_group = None

    def _setup_display(self):
        self.display = ST7789.ST7789(
            height=SCREEN_HEIGHT,
            width=SCREEN_WIDTH,
            rotation=0,
            port=0,
            cs=0,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
            dc=25,
            rst=27,
            backlight=24,  # 18 for back BG slot, 19 for front BG slot.
            spi_speed_hz=80 * 1000 * 1000,
            offset_left=0,
            offset_top=0,
        )
        self.display.begin()

    def flip(self, drawingContext):
        self.display.display(drawingContext)


SIM_WIDTH = 595
SIM_HEIGHT = 280


class PyGameDisplay(Display):
    screen = None

    def _setup_display(self):
        print("pygame display")
        self.screen = pygame.display.set_mode((SIM_WIDTH, SIM_HEIGHT))
        pygame.display.set_caption("Camina Drummer")
        self.screen.blit(pygame.image.load("assets/sim-background.png"), (0, 0))

    def flip(self, drawingContext):
        img = pygame.image.frombuffer(
            self.buffer.tobytes(), self.buffer.size, self.buffer.mode
        )
        self.screen.blit(img, (175, 20))
        pygame.display.flip()

    def capture_screenshot(self):
        print("Screenshot saved")
        pygame.image.save(self.screen, "screenshot.png")
