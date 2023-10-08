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

    def get_patterns(self, idx):
        return self.patterns["patterns"][idx]




class DrumMachine:
    def __init__(self):
        self.state = "stopped"
        self.current_pattern = None
        self.current_measure = "Measure A"
        self.tempo = 120
        self.beat_timer = None
        self.change_timer = None
        self.beat = 0
        self.interval = 60 / self.tempo / 4 

        self.sounds = {}

        for sound in SOUNDS:
            self.sounds[sound] = sa.WaveObject.from_wave_file("samples/" + SOUNDS[sound])

    def start(self):
        self.state = "playing"
        self._start_timer()

    def stop(self):
        self.state = "stopped"
        self._stop_timer()

    def set_tempo(self, tempo):
        self.tempo = tempo
        self.interval = 60 / self.tempo / 4  # 1/16th of the set tempo (in seconds)

    def _start_timer(self):
        def timer_callback():
            if self.state == "playing":
                # Code to trigger the event every 1/16th of a beat
                self.beat += 1
                if self.beat == 16:
                    self.beat = 0

                drums = self.current_pattern["measures"][self.current_measure]
                for drum in drums:
                    if drums[drum][self.beat] == "X":
                        self.sounds[drum].play()

                threading.Timer(self.interval, timer_callback).start()

        self.beat_timer = threading.Timer(self.interval, timer_callback)
        self.beat_timer.start()

    def _stop_timer(self):
        if self.beat_timer is not None:
            self.beat_timer.cancel()


current_pattern = 0
pl = PatternLoader()
pl.load()
pattern = pl.get_patterns(current_pattern)
print(pattern["name"])

# process keyboard input to switch patterns with left and right arrow keys
import sys
import tty
import termios


# Example usage:
drum_machine = DrumMachine()
drum_machine.current_pattern = pattern
drum_machine.start()



def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.buffer.raw.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

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
        current_pattern += 1
        drum_machine.current_pattern = pl.get_patterns(current_pattern)
        print("Current pattern: ", drum_machine.current_pattern["name"])
    elif char == b'[':
        if current_pattern > 0:
            current_pattern -= 1
            drum_machine.current_pattern = pl.get_patterns(current_pattern)
            print("Current pattern: ", drum_machine.current_pattern["name"])
    elif char == b'+':
        drum_machine.set_tempo(drum_machine.tempo + 1)
        print("Tempo: ", drum_machine.tempo)
    elif char == b'-':
        drum_machine.set_tempo(drum_machine.tempo - 1)
        print("Tempo: ", drum_machine.tempo)

# This will print "Timer event!" approximately every 1/16th of a beat.
# To stop the timer, you can call drum_machine.stop().

