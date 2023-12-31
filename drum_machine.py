# Copyright (C) 2023 Timothy Gerla
# Distributed under the MIT license, see LICENSE.md

# import simpleaudio as sa
import time
import pygame

from pattern_loader import PatternLoader, SOUNDS


class DrumMachine:
    def __init__(self):
        self.state = "stopped"
        self.current_pattern_idx = 1
        self.pattern_length = 0
        self.current_measure = "A"
        self.tempo = 120
        self.measure_changing = False

        self.last_taps = []

        self.beat = 0
        self.interval = 60 / self.tempo / 4 * 1000
        self._sounds = {}
        self._time_since_last_beat = 0
        self._pattern_loader = None
        self._current_pattern = None
        self._playing_pattern = None
        self._prior_measure = "A"

        try:
            pygame.mixer.init(buffer=1024)
            for sound in SOUNDS:
                self._sounds[sound] = pygame.mixer.Sound("kits/1/" + SOUNDS[sound])

        except pygame.error as e:
            print("Could not initialize sound system:", e)
            for sound in SOUNDS:
                self._sounds[sound] = None

    def start(self):
        self._time_since_last_beat = 0
        self.state = "playing"
        print("Starting drum machine")

    def stop(self):
        self.state = "stopped"
        print("Stopping drum machine")

    def load_patterns(self):
        self.pattern_loader = PatternLoader()
        self.pattern_loader.load()
        self.switch_pattern(self.current_pattern_idx)

    def switch_pattern(self, new_pattern_idx):
        self.current_pattern_idx = new_pattern_idx
        self._current_pattern = self.pattern_loader.get_pattern(
            self.current_pattern_idx
        )
        self.current_measure = "A"
        self._playing_pattern = self._current_pattern["measures"][self.current_measure]
        self.pattern_length = self._current_pattern["length"]
        self.pattern_signature = self._current_pattern.get("time_signature", "n/a")
        print(
            "Current pattern: [%r] %r (%d measures long)"
            % (
                self.current_pattern_idx,
                self.get_current_pattern_name(),
                self.pattern_length,
            )
        )

    def switch_measure(self, new_measure):
        self.measure_changing = True
        if new_measure == "T":
            self._prior_measure = self.current_measure
        self.current_measure = new_measure

    def get_current_pattern_name(self):
        return self._current_pattern["name"]

    def set_tempo(self, tempo):
        self.tempo = tempo
        self.interval = 60 / self.tempo / 4 * 1000

    def tap_tempo(self):
        now = time.time()
        self.last_taps.append(now)
        if len(self.last_taps) > 5:
            self.last_taps.pop(0)

        if len(self.last_taps) >= 2:
            deltas = [
                self.last_taps[i] - self.last_taps[i - 1]
                for i in range(1, len(self.last_taps))
            ]
            new_tempo = 60 / (sum(deltas) / len(deltas))
            average_tempo = (self.tempo + new_tempo) / 2
            self.set_tempo(round(average_tempo))

    def _play_beat(self):
        self.beat += 1
        if self.beat == self.pattern_length:
            self.beat = 0
            # this is so that if we switch measures while playing, the new measure style will
            # only kick in at the top of the beat.
            self._playing_pattern = self._current_pattern["measures"][
                self.current_measure
            ]
            if self.current_measure == "T":
                self.current_measure = self._prior_measure
                self.measure_changing = True
            else:
                self.measure_changing = False

        drums = self._playing_pattern
        for drum in drums:
            drumIdx = self.beat % len(drums[drum])
            if drums[drum][drumIdx] == "X" and self._sounds[drum] is not None:
                self._sounds[drum].play()

    def loop(self, delta_time):
        if self.state == "playing":
            self._time_since_last_beat += delta_time
            if self._time_since_last_beat >= self.interval:
                self._time_since_last_beat = 0
                self._play_beat()
