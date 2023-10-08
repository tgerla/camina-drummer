import threading
import time
import yaml
import simpleaudio as sa

PATTERNS_FILE = "patterns.yaml"


# AC: Accent
# BD: Bass drum
# SD: Snare Drum
# LT: Low tom
# MT: Medium tom
# HT: High tom
# CH: Closed hi-hat
# OH: Open hi-hat
# CY: Cymbal
# RS: Rim shot
# CP: Clap
# CB: Cowbell


SOUNDS = {
    "AC": "clave_low_stereo_16.wav",
    "BD": "bass_stereo_16.wav",
    "SD": "snare_stereo_16.wav",
    "LT": "tom1_stereo_16.wav",
    "MT": "tom2_stereo_16.wav",
    "HT": "tom3_stereo_16.wav",
    "CH": "hh_closed_stereo_16.wav",
    "OH": "hh_open_stereo_16.wav",
    "CY": "ride_stereo_16.wav",
    "RS": "rim_stereo_16.wav",
    "CP": "clave_high_stereo_16.wav",
    "CB": "cowbell_high_stereo_16.wav",
}

# a class to load a patterns object from yaml
class PatternLoader:
    def __init__(self, filename = PATTERNS_FILE):
        self.filename = filename
        self.patterns = None

    def load(self):
        with open(self.filename, 'r') as stream:
            try:
                self.patterns = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get_pattern(self, idx):
        return self.patterns["patterns"][idx]




class DrumMachine:
    def __init__(self):
        self.state = "stopped"
        self.current_pattern_idx = 1
        self.pattern_length = 0
        self.current_measure = "Measure A"
        self.tempo = 120
        self.beat_timer = None
        self.change_timer = None
        self.beat = 0
        self.interval = 60 / self.tempo / 4 

        self.sounds = {}
        self._pattern_loader = None
        self._current_pattern = None

        for sound in SOUNDS:
            self.sounds[sound] = sa.WaveObject.from_wave_file("samples/" + SOUNDS[sound])

    def start(self):
        self.state = "playing"
        self._start_timer()

    def stop(self):
        self.state = "stopped"
        self._stop_timer()

    def load_patterns(self, patterns_file = PATTERNS_FILE):
        self.pattern_loader = PatternLoader(patterns_file)
        self.pattern_loader.load()
        self.switch_pattern(self.current_pattern_idx)

    def switch_pattern(self, new_pattern_idx):
        self.current_pattern_idx = new_pattern_idx
        self._current_pattern = self.pattern_loader.get_pattern(self.current_pattern_idx)
        self.pattern_length = self._current_pattern["length"]
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
                        self.sounds[drum].play()
                threading.Timer(self.interval, timer_callback).start()

        self.beat_timer = threading.Timer(self.interval, timer_callback)
        self.beat_timer.start()

    def _stop_timer(self):
        if self.beat_timer is not None:
            self.beat_timer.cancel()



# process keyboard input to switch patterns with left and right arrow keys
import sys
import tty
import termios

drum_machine = DrumMachine()
drum_machine.load_patterns()

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.buffer.raw.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    current_pattern = 1
    drum_machine.start()


    while True:
        char = getch()
        if char == b'q':
            drum_machine.stop()
            sa.stop_all()
            break
        elif char == b' ':
            if drum_machine.state == "playing":
                drum_machine.stop()
            else:
                drum_machine.start()
        elif char == b']':
            if drum_machine.current_pattern_idx < len(drum_machine.pattern_loader.patterns["patterns"]):
                drum_machine.current_pattern_idx += 1
            drum_machine.switch_pattern(drum_machine.current_pattern_idx)
        elif char == b'[':
            if drum_machine.current_pattern_idx > 1:
                drum_machine.current_pattern_idx -= 1
                drum_machine.switch_pattern(drum_machine.current_pattern_idx)
        elif char == b'+':
            drum_machine.set_tempo(drum_machine.tempo + 1)
            print("Tempo: ", drum_machine.tempo)
        elif char == b'-':
            drum_machine.set_tempo(drum_machine.tempo - 1)
            print("Tempo: ", drum_machine.tempo)

if __name__ == "__main__":
    main()
