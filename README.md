# About the Repo

This repo contains 2 cognitive experiments on executive functions:
saccades and number-letter experiments.
Each directory contains a Python script and a .bat file to execute the script.

The experiments were created using Python 3.6 and Psychopy 3.2

## Saccades

Anti- and Prossacade tasks. Fix Cross -> blank -> Cue -> Arrow. Arrow appears
either in the same place as the cue, or on the opposite side. Arrow is the target.

6 blocks with 2 coniditions. 12 Trials per block + 6 training trials per block with feedback.

Measurements: Accuracy, RT.

#### TODO: 

1. Place texts better on screen |DONE
2. Code frames (0.5 rounding?) | DONE
3. Check for missing frames | DONE
4. Check data logging | DONE

## Number-letter

A 2x2 grid on the screen. A stimulus (letter+number) appears in one of the cells. Depending on whether it is a top or bottom row, a person attends to either the letter or the number, making a judgement. After that a new stimulus appears in the next cell (rotating clockwise).

3 blocks: only top row (32 trials), only bottom row (32 trials), full rotation (128 trials) + 12 train trials per block with feedback.

Measurements: Accuracy, RT

#### TODO:

1. Place texts better on screen | DONE

#### Ideas:
1. Explicitly prohibit/allow talking outloud.
2. "Odd/Even" differ more than "Чётный/Нечётный" -> easier to memorize?
3. Keys mapping (which key, left or right, should correspond to each answer, i.e. should even numbers be on right or on left etc.
4. 3 (three) looks too similar to з (z).

# Known Issues

1. The fullscreen might get cropped if Windows visual scaling is set to anything other than 100%. 
2. The Saccades experiments takes quite some time to boot up for some reason. Maybe there are lots of visual objects being created in the beggining. | Solved: there was a piece of code that put the program to sleep for 100s.
3. The texts are still not ideally in the center of the screen.
4. The upwards arrow in Saccades seems to be larger than the others even though the coordinates seem to be right.