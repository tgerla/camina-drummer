import sys
import tty
import termios
import pygame

from display import Display
from drum_machine import DrumMachine

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
    running = True

    display = Display()

    drum_machine = DrumMachine()
    drum_machine.load_patterns()
    drum_machine.start()

    while running:
        running = display.loop(drum_machine)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q)):
                running = False
                drum_machine.stop()
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if drum_machine.state == "playing":
                    drum_machine.stop()
                else:
                    drum_machine.start()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if drum_machine.current_pattern_idx < len(drum_machine.pattern_loader.patterns["patterns"]):
                    drum_machine.current_pattern_idx += 1
                drum_machine.switch_pattern(drum_machine.current_pattern_idx)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if drum_machine.current_pattern_idx > 1:
                    drum_machine.current_pattern_idx -= 1
                drum_machine.switch_pattern(drum_machine.current_pattern_idx)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                drum_machine.set_tempo(drum_machine.tempo + 1)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                drum_machine.set_tempo(drum_machine.tempo - 1)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                drum_machine.switch_measure("A")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                drum_machine.switch_measure("B")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                drum_machine.switch_measure("T")
    
    pygame.quit()

if __name__ == "__main__":
    main()
