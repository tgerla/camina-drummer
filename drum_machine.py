import simpleaudio as sa
import threading

from pattern_loader import PatternLoader, SOUNDS


class DrumMachine:
    def __init__(self):
        self.state = "stopped"
        self.current_pattern_idx = 1
        self.pattern_length = 0
        self.current_measure = "Measure A"
        self.tempo = 120

        self.beat = 0
        self.interval = 60 / self.tempo / 4 
        self._sounds = {}
        self._beat_timer = None
        self._pattern_loader = None
        self._current_pattern = None

        for sound in SOUNDS:
            self._sounds[sound] = sa.WaveObject.from_wave_file("samples/" + SOUNDS[sound])

    def start(self):
        self.state = "playing"
        self._start_timer()

    def stop(self):
        self.state = "stopped"
        self._stop_timer()

    def load_patterns(self):
        self.pattern_loader = PatternLoader()
        self.pattern_loader.load()
        self.switch_pattern(self.current_pattern_idx)

    def switch_pattern(self, new_pattern_idx):
        self.current_pattern_idx = new_pattern_idx
        self._current_pattern = self.pattern_loader.get_pattern(self.current_pattern_idx)
        self.pattern_length = self._current_pattern["length"]
        self.pattern_signature = self._current_pattern.get("time_signature", "n/a")
        print("Current pattern: [%r] %r (%d measures long)" % (self.current_pattern_idx, self.get_current_pattern_name(), self.pattern_length))

    def get_current_pattern_name(self):
        return self._current_pattern["name"]

    def set_tempo(self, tempo):
        self.tempo = tempo
        self.interval = 60 / self.tempo / 4  # 1/16th of the set tempo (in seconds)

    def _start_timer(self):
        def timer_callback():
            if self.state == "playing":
                # Code to trigger the event every 1/16th of a beat
                self.beat += 1
                if self.beat == self.pattern_length:
                    self.beat = 0

                drums = self._current_pattern["measures"][self.current_measure]
                for drum in drums:
                    drumIdx = self.beat % len(drums[drum])
                    if drums[drum][drumIdx] == "X":
                        self._sounds[drum].play()
                threading.Timer(self.interval, timer_callback).start()

        self._beat_timer = threading.Timer(self.interval, timer_callback)
        self._beat_timer.start()

    def _stop_timer(self):
        if self._beat_timer is not None:
            self._beat_timer.cancel()
