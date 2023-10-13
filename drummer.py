# Copyright (C) 2023 Timothy Gerla
# Distributed under the MIT license, see LICENSE.md

import pygame

from display import PyGameDisplay
from drum_machine import DrumMachine

def handle_events(drum_machine, display):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q)):
            drum_machine.stop()
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if drum_machine.state == "playing":
                drum_machine.stop()
            else:
                drum_machine.start()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if drum_machine.current_pattern_idx < len(drum_machine.pattern_loader.patterns["patterns"]):
                drum_machine.current_pattern_idx += 1
            else:
                drum_machine.current_pattern_idx = 1
            drum_machine.switch_pattern(drum_machine.current_pattern_idx)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if drum_machine.current_pattern_idx > 1:
                drum_machine.current_pattern_idx -= 1
            else :
                drum_machine.current_pattern_idx = len(drum_machine.pattern_loader.patterns["patterns"])
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
            if "T" in drum_machine._current_pattern["measures"]:
                drum_machine.switch_measure("T")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            display.capture_screenshot()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            drum_machine.tap_tempo()
    return True

def main():
    current_pattern = 1
    running = True

    pygame.init()
    clock = pygame.time.Clock()
    display = PyGameDisplay()

    drum_machine = DrumMachine()
    drum_machine.load_patterns()
    
    while running:
        delta_time = clock.tick(60)
        drum_machine.loop(delta_time)
        display.loop(drum_machine)
        running = handle_events(drum_machine, display)
        
    pygame.quit()

if __name__ == "__main__":
    main()