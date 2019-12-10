# -*- coding: utf-8 -*-

from psychopy import core, data, event, gui, logging, visual
import random
import sys
import os

BLOCKS_NUMBER = 3
TRIALS_NUMBER = 3

# Add a global key for exit
event.globalKeys.clear()
event.globalKeys.add(key='z', modifiers=['ctrl'], func=core.quit, name='shutdown')

# Add a Display and get its framerate (specifically, how many ms 1 frame takes)
win = visual.Window(size=[1920, 1080], units='height', color=[1, 1, 1], fullscr=True)
framerate = win.getMsPerFrame()[2]
# Some visuals

cross_hori = visual.Line(win, units='height',  start=(-0.05, 0), end=(0.05, 0), lineColor='black', lineWidth=2.5, name='line_hori')
cross_vert = visual.Line(win, units='height',  start=(0, -0.05), end=(0, 0.05), lineColor='black', lineWidth=2.5, name='line_vert')

cue = visual.ShapeStim(win, units='norm', vertices=[(-0.25, -0.5), (-0.25, 0.5), (0.25, 0.5), (0.25, -0.5)], size=0.2, fillColor='black', name='cue')
up_arrow = visual.ShapeStim(win, units='norm', vertices=[(-0.05, -0.5), (-0.05, 0.1), (-0.2, 0.1), (0, 0.5), (0.2, 0.1), (0.05, 0.1), (0.05, -0.5)], 
                            size=0.2, fillColor='black', name='upward_arrow')
right_arrow = visual.ShapeStim(win, units='norm', vertices=[(-0.5, 0.05), (0.1, 0.05), (0.1, 0.2), (0.5, 0), (0.1, -0.2), (0.1, -0.05), (-0.5, -0.05)],
                               size=0.2, fillColor='black', name='rightward_arrow')
left_arrow = visual.ShapeStim(win, units='norm', vertices=[(0.5, 0.05), (-0.1, 0.05), (-0.1, 0.2), (-0.5, 0), (-0.1, -0.2), (-0.1, -0.05), (0.5, -0.05)],
                              size=0.2, fillColor='black', name='leftward_arrow')

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
    exp_info['experiment_name'] = 'Pro-/Antisacc'
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
Instructions ryba.\n
В начале каждого задания смотрите на фиксационный крест в центре экрана.
После его исчезновения появится сигнальный прямоугольник, который сменится стрелкой.
Ваша цель — следить за появлением стрелки на экране и нажимать соответствующую стрелку на клавиатуре.\n
В эксперименте несколько условий, каждое из которых будет повторяться несколько раз.\n
После первых нескольких заданий в каждом блоке вам будет предоставлена обратная связь.\n
Нажмите ПРОБЕЛ, чтобы начать.\n
"""
instructions.draw()
win.flip()
# Wait for response
event.waitKeys(keyList=['space'])

mother = data.ExperimentHandler(name="experiment_handler", extraInfo=exp_info, dataFileName=f'data/{filename}')
blocks_list = [{'condition': b} for b in ['prosaccade', 'antisaccade']] # 2 blocks, 3 times each
blocks = data.TrialHandler(trialList=blocks_list, nReps=BLOCKS_NUMBER) 
trials_list = [{'side': side, 'target_ori': ori} for side in ['left', 'right'] for ori in ['left', 'up', 'right']] # 2 places (left, right) * 3 targets (l, u, r), 3 times each

mother.addLoop(blocks)

responses = []
for block in blocks:
    block_condition = blocks_list[blocks.thisIndex] # dictionary of current block condition
    cross_times = [1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500]
    random.shuffle(cross_times)
    if block['condition'] == 'prosaccade':
        cond = "Одноместные стимулы"
    else:
        cond = "Разноместные стимулы"
    visual.TextStim(win, font='arial', color='black', text=cond, units='norm', height=0.075, wrapWidth=None, ori=0, pos=[0.6, 0]).draw()
    win.flip()
    core.wait(2.0)
    trials = data.TrialHandler(trialList=trials_list, nReps=TRIALS_NUMBER) 
    mother.addLoop(trials)
    for trial in trials:
        trial_condition = trials_list[trials.thisIndex] # dictionary of current trial condition
        # Ready
        for frame in range(int(1000 // framerate) + 1):  
            visual.TextStim(win, font='arial', color='black', text='Ready', units='norm', height=0.075, wrapWidth=None, ori=0, pos=[0.9, 0]).draw()
            win.flip()
        # Cross
        try:
            cross_time = cross_times.pop()
        except IndexError:
            cross_times = [1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500]
            random.shuffle(cross_times)
            cross_time = cross_times.pop()
        for frame in range(int(cross_time // framerate) + 1):
            cross_hori.draw()
            cross_vert.draw()
            win.flip()
        # Blank
        for frame in range(int(200 // framerate) + 1):
            win.flip()
        # Cue
        if block_condition['condition'] == 'prosaccade':
            cue_side = trial_condition['side']
        else:
            cue_side = ['left', 'right'][1 - ['left', 'right'].index(trial_condition['side'])]
        for frame in range(int(250 // framerate) + 1):
            cue.pos = (0.75 * (-1 + 2 * ['left', 'right'].index(cue_side)), 0)
            cue.draw()
            win.flip()
        # Stimulus
        arrow = eval(f'{trial_condition["target_ori"]}_arrow')
        arrow.pos = (0.75 * (-1 + 2 * ['left', 'right'].index(trial_condition['side'])), 0) # changing x-axis value; if left, 0.75 * (-1 + 2 * 0) = -0.75, if right, 0.75 * (-1 + 2 * 1) = 0.75
        for frame in range(int(150 // framerate) + 1):
            arrow.draw()
            win.flip()
        # Response
        clock = core.Clock()
        win.flip()
        key_press = event.waitKeys(keyList=['left', 'up', 'right'], timeStamped=clock, maxWait=5)
        try:
            resp, rt = key_press[0]
            acc = int(resp == trial_condition["target_ori"])
        except TypeError:
            resp, rt = None, None
            acc = 0
        # Data Logging
        mother.addData('Response', resp)
        mother.addData('Accuracy', acc)
        mother.addData('Reaction Time', rt)

        # Feedback
        if trials.thisRepN == 0:
            feedback = ['wrong', 'right'][acc] # If no answer given, it'd still be marked as 'wrong'. Is it desirable?
            visual.TextStim(win, font='arial', color='black', text=f'Feedback: {feedback}\nPress space', units='norm', height=0.075, wrapWidth=None, ori=0, pos=[0.7, 0]).draw()
            win.flip()
            event.waitKeys(keyList=['space'], maxWait=5)

        mother.nextEntry()

# Thanks
visual.TextStim(win, text='Thanks, bruh', font='arial', color='black', units='norm', height=0.05, wrapWidth=None, ori=0, pos=[0.5, 0]).draw()
win.flip()
core.wait(4.0)

mother.saveAsWideText(filename, delim=',')
win.close()
