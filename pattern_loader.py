import yaml

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


