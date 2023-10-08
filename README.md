# camina-drummer
A drum loop player in Python.

This will eventually run on CircuitPython on one of these: https://www.adafruit.com/product/802

![Screenshot](screenshot.png)

Keys:

```
Q or Esc - quit
Left arrow - previous pattern
Right arrow - next pattern
Spacebar - play/pause
Plus - increase tempo
Minus - decrease tempo
A/B/T - switch to a different measure style, A and B styles, plus "T" for a transition or break.
```

The samples are from https://github.com/jstrait/beats and patterns are from https://github.com/montoyamoraga/drum-machine-patterns, using my script to convert them to YAML at https://github.com/tgerla/drum-machine-patterns. 

TODO:

- deal with A/B patterns
- a button to queue up a break
- swing
