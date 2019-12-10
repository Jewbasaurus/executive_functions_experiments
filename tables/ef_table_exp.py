# -*- coding: utf-8 -*-

from psychopy import core, data, event, gui, logging, visual
import random
import sys
import os

BLOCKS_NUMBER = 1
TRAINING_LEN = 12
UR_CELL = (1.07, 0.39)
UL_CELL = (0.65, 0.39)
BR_CELL = (1.07, -0.38)
BL_CELL = (0.65, -0.38)
STIMULI = ['2А', '2М', '2П', '2Р', '3А', '3К', '3О', '3У', '4Е', '4Е', '4У',
           '5А', '5К', '5Р', '5У', '6А', '6Е', '6К', '6Р', '7О', '7О', '7П',
           '7Р', '8М', '8М', '8П', '9Е', '9М', '9О', '9П']

# Add a global key for exit
event.globalKeys.clear()
event.globalKeys.add(key='z', modifiers=['ctrl'], func=core.quit, name='shutdown')

# Add a Display and get its framerate (specifically, how many ms 1 frame takes)
win = visual.Window(size=[1920, 1080], units='norm', color=[1, 1, 1], fullscr=True)
framerate = win.getMsPerFrame()[2]

# Some visuals
line_hori = visual.Line(win, units='norm',  start=(-0.42, 0), end=(0.42, 0), lineColor='black', lineWidth=2.5, name='line_hori')
line_vert = visual.Line(win, units='norm',  start=(0, -0.75), end=(0, 0.75), lineColor='black', lineWidth=2.5, name='line_vert')
border_up = visual.Line(win, units='norm',  start=(-0.42, 0.75), end=(0.42, 0.75), lineColor='black', lineWidth=2.5, name='border_up')
border_down = visual.Line(win, units='norm',  start=(-0.42, -0.75), end=(0.42, -0.75), lineColor='black', lineWidth=2.5, name='border_down')
border_left = visual.Line(win, units='norm',  start=(-0.42, 0.75), end=(-0.42, -0.75), lineColor='black', lineWidth=2.5, name='border_left')
border_right = visual.Line(win, units='norm',  start=(0.42, 0.75), end=(0.42, -0.75), lineColor='black', lineWidth=2.5, name='border_right')

# Dialog box before an experiment session
win.winHandle.set_visible(False) # in FS experiment window overlays all others. We rend it invisible...
dlg = gui.Dlg(title='Experiment')
dlg.addField('ID', initial='0')
dlg.addField('Sex', choices=['male', 'female', 'not defined'])
dlg.addField('Age')
ok = dlg.show()
# If subject presses okay
if ok:
    exp_info = {a.lower(): b for a, b in zip(dlg.inputFieldNames, dlg.data)} # Save subject's info into a dic
    exp_info['date'] = data.getDateStr() # Add current data
    exp_info['experiment_name'] = 'Table'
    exp_info['framerate'] = framerate
# If subject presses Cancel
else:
    core.quit()
win.winHandle.set_visible(True) # ... and visible again

filename = f"{exp_info['id']}_{exp_info['date']}"

#logging
logging.LogFile(f=f'./data/{filename}_log.txt', level=10)

# Instructions
# instructions = visual.TextBox(win, units='norm', size=(1.75, 1.5), pos=(0, 0), font_size=24, font_color=(1, 1, 1), name='Instructions')
instructions = visual.TextStim(win, font='arial', color='black', units='norm', height=0.05, wrapWidth=None, ori=0, pos=[0.5, 0])
instructions.text = """
На экране — таблица 2х2. В случайной ячейке будет появляться стимул — цифра и буква.\n
Если пара появилась в верхних клетках, вам необходимо ответить, нечётная цифра или чётная.
Нажмите левый Ctrl, если цифра нечётная, или правый Ctrl, если цифра чётная.\n
Если пара появилась в нижних клетках, вам необходимо ответить, согласная буква или гласная.
Нажмите левый Ctrl, если буква согласная, или правый Ctrl, если буква гласная.\n
Нажмите ПРОБЕЛ, чтобы начать.\n
"""
instructions.draw()
win.flip()
# Wait for response
event.waitKeys(keyList=['space'])

mother = data.ExperimentHandler(name="experiment_handler", extraInfo=exp_info, dataFileName=f'data/{filename}')
blocks_list = [{'trials_number' : tn, 'condition' : cond} for tn, cond in  [(32, 'top'), (32, 'bot'), (128, 'both')]] # 3 blocks
blocks = data.TrialHandler(trialList=blocks_list, nReps=BLOCKS_NUMBER, method='sequential') 

mother.addLoop(blocks)

responses = []
for block in blocks:
    block_condition = blocks_list[blocks.thisIndex] # dictionary of current block condition
    if block['condition'] == 'top':
        trials_list = [{'cell' : cell} for cell in [UL_CELL, UR_CELL]]
    elif block['condition'] == 'bot':
        trials_list = [{'cell' : cell} for cell in [BL_CELL, BR_CELL]]
    else:
        trials_list = [{'cell' : cell} for cell in [BR_CELL, BL_CELL, UL_CELL, UR_CELL]]
    trials_number = block['trials_number'] // len(trials_list)
    test_trials_number = TRAINING_LEN // block['trials_number']
    trials = data.TrialHandler(trialList=trials_list, nReps=trials_number, method='sequential')
    train_trials = data.TrialHandler(trialList=trials_list, nReps=test_trials_number, method='sequential')
    mother.addLoop(trials)
    mother.addLoop(train_trials)
    # The Matrix
    line_vert.autoDraw = True
    line_hori.autoDraw = True
    border_right.autoDraw = True
    border_left.autoDraw = True
    border_up.autoDraw = True
    border_down.autoDraw = True
    win.flip()
    for train_trial in train_trials:
        # Stimulus
        stimulus = random.choice(STIMULI)
        while True:
            visual.TextStim(win, text=stimulus, font='arial', color='black', units='norm', 
                            height=0.3, wrapWidth=None, alignHoriz='center', alignVert='center', ori=0, pos=train_trial['cell']).draw()
            win.flip()
            clock = core.Clock()
            key_press = event.waitKeys(keyList=['lctrl', 'rctrl'], timeStamped=clock)
            break
        win.flip()
        core.wait(0.15)
        mother.nextEntry()
    for trial in trials:
        # Stimulus
        stimulus = random.choice(STIMULI)
        while True:
            visual.TextStim(win, text=stimulus, font='arial', color='black', units='norm', 
                            height=0.3, wrapWidth=None, alignHoriz='center', alignVert='center', ori=0, pos=trial['cell']).draw()
            win.flip()
            clock = core.Clock()
            key_press = event.waitKeys(keyList=['lctrl', 'rctrl'], timeStamped=clock)
            break
        resp, rt = key_press[0]
        if trial['cell'][1] > 0: # Depending on y coordinate -- above or below -- we address different parts of a stimulus
            target = int(stimulus[0]) % 2  # if it was even, the result is 0, 1 otherwise
        else:
            target = stimulus[1] in ['А', 'Е', 'Ё', 'И', 'О', 'У', 'Ы', 'Ю', 'Я'] # if consonant, 0, 1 otherwise
        acc = int(resp == ['lctrl', 'rctrl'][target])
        # Data Logging
        mother.addData('Response', resp)
        mother.addData('Accuracy', acc)
        mother.addData('Reaction Time', rt)
        mother.addData('Stimulus', stimulus)
        win.flip()
        core.wait(0.15)

        mother.nextEntry()

line_vert.autoDraw = False
line_hori.autoDraw = False
border_right.autoDraw = False
border_left.autoDraw = False
border_up.autoDraw = False
border_down.autoDraw = False
win.flip()

# Thanks
visual.TextStim(win, text='Спасибо за участие', font='arial', color='black', units='height', height=0.2, wrapWidth=None, ori=0, pos=[0, 0]).draw()
win.flip()
core.wait(4.0)

mother.saveAsWideText(f'data/{filename}', delim=',')
win.close()
