# Copyright (C) 2023 Timothy Gerla
# Distributed under the MIT license, see LICENSE.md

import pygame

from display import ST7735RDisplay
from drum_machine import DrumMachine
from gpiozero import Button

class Controller:
    def __init__(self):
        self.jUp = Button(6)
        self.jDown = Button(19)
        self.jLeft = Button(5)
        self.jRight = Button(26)
        self.jPress = Button(13)
        self.key1 = Button(21)
        self.key2 = Button(20)
        self.key3 = Button(16)

def handle_events(drum_machine, display, controller):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drum_machine.stop()
            return False
        
    
    if controller.key3.is_pressed:
        if drum_machine.state == "playing":
            drum_machine.stop()
        else:
            drum_machine.start()
    if controller.jRight.is_pressed:
        if drum_machine.current_pattern_idx < len(drum_machine.pattern_loader.patterns["patterns"]):
            drum_machine.current_pattern_idx += 1
        else:
            drum_machine.current_pattern_idx = 1
        drum_machine.switch_pattern(drum_machine.current_pattern_idx)
    if controller.jLeft.is_pressed:
        if drum_machine.current_pattern_idx > 1:
            drum_machine.current_pattern_idx -= 1
        else :
            drum_machine.current_pattern_idx = len(drum_machine.pattern_loader.patterns["patterns"])
        drum_machine.switch_pattern(drum_machine.current_pattern_idx)
    if controller.jUp.is_pressed:
        drum_machine.set_tempo(drum_machine.tempo + 1)
    if controller.jDown.is_pressed:
        drum_machine.set_tempo(drum_machine.tempo - 1)

    return True

def main():
    current_pattern = 1
    running = True

    pygame.init()
    clock = pygame.time.Clock()
    display = ST7735RDisplay()
    controller = Controller()

    drum_machine = DrumMachine()
    drum_machine.load_patterns()
    drum_machine.start()
    
    while running:
        delta_time = clock.tick(60)
        drum_machine.loop(delta_time)
        display.loop(drum_machine)
        running = handle_events(drum_machine, display, controller)
        
    pygame.quit()

if __name__ == "__main__":
    main()
