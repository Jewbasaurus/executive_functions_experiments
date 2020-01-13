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

1. Place texts better on screen
2. Code frames (0.5 rounding?) | DONE
3. Check for missing frames | KINDA DONE
4. Check data logging | SEEMS TO BE WORKING

## Number-letter

A 2x2 grid on the screen. A stimulus (letter+number) appears in one of the cells. Depending on whether it is a top or bottom row, a person attends to either the letter or the number, making a judgement. After that a new stimulus appears in the next cell (rotating clockwise).

3 blocks: only top row (32 trials), only bottom row (32 trials), full rotation (128 trials) + 12 train trials per block with feedback.

Measurements: Accuracy, RT

#### TODO:

1. Place texts better on screen
