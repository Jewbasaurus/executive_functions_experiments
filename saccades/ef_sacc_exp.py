# -*- coding: utf-8 -*-

from psychopy import core, data, event, gui, logging, visual
import random
import sys
import os


# 3 blocks; 2 trials + 1 training trial
BLOCKS_NUMBER = 3
TRIALS_NUMBER = 3

# TIMES | Note that it will only work on 60HZ Displays. For other refresh rates you gotta use other frame values, or divide ms/rate
READY_TITLE_FRAME = 60 # 1000 ms
# FIX_CROSS TIME is randomized in every block later on
BLANK_FRAMES = 12 # 200 ms
CUE_FRAMES =  15 # 250 ms
STIMULUS_FRAMES =  6 # 100 ms

# Add a global key for exit
event.globalKeys.clear()
event.globalKeys.add(key='z', modifiers=['ctrl'], func=core.quit, name='shutdown')

# Add a Display and get its framerate (specifically, how many ms 1 frame takes)
win = visual.Window(size=[1920, 1080], units='height', color=[1, 1, 1], fullscr=True)
framerate = win.getMsPerFrame()[2]

# Some visuals
cross_hori = visual.Line(win, units='height', start=(-0.05, 0), end=(0.05, 0), lineColor='black', lineWidth=2.5, name='line_hori')
cross_vert = visual.Line(win, units='height', start=(0, -0.05), end=(0, 0.05), lineColor='black', lineWidth=2.5, name='line_vert')

cue = visual.ShapeStim(win, units='norm', vertices=[(-0.25, -0.5), (-0.25, 0.5), (0.25, 0.5), (0.25, -0.5)], size=0.2, fillColor='black', name='cue')
up_arrow = visual.ShapeStim(win, units='norm', vertices=[(-0.025, -0.25), (-0.025, 0.05), (-0.1, 0.05), (0, 0.25), (0.1, 0.05), (0.025, 0.05), (0.025, -0.25)], 
                            size=0.2, fillColor='black', name='upward_arrow')
right_arrow = visual.ShapeStim(win, units='norm', vertices=[(-0.25, 0.025), (0.05, 0.025), (0.05, 0.1), (0.25, 0), (0.05, -0.1), (0.05, -0.025), (-0.25, -0.025)],
                               size=0.2, fillColor='black', name='rightward_arrow')
left_arrow = visual.ShapeStim(win, units='norm', vertices=[(0.25, 0.025), (-0.05, 0.025), (-0.05, 0.1), (-0.25, 0), (-0.05, -0.1), (-0.05, -0.025), (0.25, -0.025)],
                              size=0.2, fillColor='black', name='leftward_arrow')
instructions = visual.TextStim(win, font='arial', color='black', units='norm', height=0.0385, wrapWidth=1, ori=0, pos=[0.55, 0])
inter_instructions = visual.TextStim(win, font='arial', color='black', units='norm', height=0.04, wrapWidth=0.9, ori=0, pos=[0.5, 0])
ready_prompt = visual.TextStim(win, font='arial', color='black', units='norm', height=0.075, wrapWidth=None, ori=0, pos=[0.5, 0])
condition_title = visual.TextStim(win, font='arial', color='black', units='norm', height=0.075, wrapWidth=None, ori=0, pos=[0.6, 0])
feedback = visual.TextStim(win, font='arial', color='black', units='norm', height=0.075, wrapWidth=0.25, ori=0, pos=[0.1, 0])

# Dialog box to choose language
win.winHandle.set_visible(False) # Render the main experiment window invisible so that DBox is on top
dlg = gui.Dlg(title='Язык/Language') # Create a DBox
dlg.addField('Язык/Language', choices=['Русский', 'English'], initial='Русский')
ok = dlg.show()
# If subject presses okay
if ok:
    exp_info = {'language' : dlg.data[0]} # Add some data to the experiment info dic
    # exp_info = {a.lower(): b for a, b in zip(dlg.inputFieldNames, dlg.data)}
# If subject presses Cancel
else:
    core.quit()
win.winHandle.set_visible(True) # Make exp window visible again -- probably not needed since we make it invisible again just in a second

if exp_info['language'] == 'Русский':
    ID_FIELD = '№ участника'
    SEX_FIELD = 'Пол'
    SEX_CHOICE = ['мужской', 'женский', 'предпочитаю не отвечать']
    AGE_FIELD = 'Возраст'
else:
    ID_FIELD = 'ID'
    SEX_FIELD = 'Sex'
    SEX_CHOICE = ['male', 'female', 'prefer not to answer']
    AGE_FIELD = 'Age'

# Dialog box before an experiment session
win.winHandle.set_visible(False) # in FS experiment window overlays all others. We rend it invisible...
dlg = gui.Dlg(title='Experiment')
dlg.addField(ID_FIELD, initial='0')
dlg.addField(SEX_FIELD, choices=SEX_CHOICE)
dlg.addField(AGE_FIELD)
ok = dlg.show()
# If subject presses okay
if ok:
    exp_info.update({a : b for a, b in zip(['id', 'sex', 'age'], dlg.data)}) # Save subject's info into a dic
    exp_info['date'] = data.getDateStr() # Add current data
    exp_info['experiment_name'] = 'Pro-/Antisacc'
    exp_info['framerate'] = framerate
# If subject presses Cancel
else:
    core.quit()
win.winHandle.set_visible(True) # ... and visible again

filename = f"{exp_info['id']}_{exp_info['date']}"

#logging
try:
    logging.LogFile(f=f'./data/{filename}_log.txt', level=10)
except FileNotFoundError:
    os.mkdir('./data')
    logging.LogFile(f=f'./data/{filename}_log.txt', level=10)

# Instructions
# instructions = visual.TextBox(win, units='norm', size=(1.75, 1.5), pos=(0, 0), font_size=24, font_color=(1, 1, 1), name='Instructions')
if exp_info['language'] == 'Русский':
    instructions.text = """
В этом тесте необходимо внимательно наблюдать за объектами на
экране. Тест разделен на несколько частей. Инструкции будут
повторяться перед началом каждой части. Пожалуйста, внимательно
читайте инструкции, так как они будут различаться.\n
В начале каждого задания в центре экрана будет появляться крестик.
Зафиксируйте свой взгляд на нем. Затем справа или слева на экране
появится квадрат, а после него — стрелка. В некоторых случаях
стрелка будет появляться ТАМ ЖЕ, где и квадрат, а в других — с
ПРОТИВОПОЛОЖНОЙ стороны. Ваша задача — ответить, куда была
направлена стрелка, нажимая на клавиши стрелок вверх, вправо или
влево на клавиатуре.\n
Нажмите ПРОБЕЛ, чтобы перейти к первой части.
"""
    instructions_finale = 'Вы завершили тест. Спасибо!'
    ready_prompt.text = 'Приготовьтесь'
    FEEDBACK_OPTIONS = ['Неправильно', 'Правильно']
    FEEDBACK_CONTINUE = 'Нажмите ПРОБЕЛ'
else:
    instructions.text = """
In this test you must carefully monitor the objects on the screen. The test is
divided into several parts. Instructions will be repeated before the beginning
of each part. Please read the instructions carefully as they will vary.\n
At the beginning of each task, a cross will appear in the center of the
screen. Fix your gaze on it. Then a square will appear on the right or left of
the screen, and after it an arrow will appear. In some cases the arrow will
appear in the SAME PLACE as the square, and on the OPPOSITE side in others. 
Your task is to answer where the arrow was directed by pressing the
arrow keys up, left or right on the keyboard.\n
Press the SPACEBAR to go to the first part.
"""
    instructions_finale = 'You have completed the test. Thank you!'
    ready_prompt.text = 'Ready'
    FEEDBACK_OPTIONS =  ['Wrong', 'Right']
    FEEDBACK_CONTINUE = 'Press SPACEBAR'
instructions.draw()
win.flip()
# Wait for response
event.waitKeys(keyList=['space'])

# Data Handler object 
mother = data.ExperimentHandler(name="experiment_handler", extraInfo=exp_info, dataFileName=f'data/{filename}')
blocks_list = [{'condition': b} for b in ['prosaccade', 'antisaccade']] # 2 blocks, 3 times each
# Trial Handler object
blocks = data.TrialHandler(trialList=blocks_list, nReps=BLOCKS_NUMBER) 
trials_list = [{'side': side, 'target_ori': ori} for side in ['left', 'right'] for ori in ['left', 'up', 'right']] # 2 places (left, right) * 3 targets (l, u, r), 3 times each (2 + training)
responses = []

# instructions_start_text = """
# В этой части стрелка будет появляться ТАМ ЖЕ, где и квадрат.\n
# Ваша задача – как можно быстрее перевести взгляд с крестика на квадрат, а затем ответить, куда была направлена стрелка.\n
# Сейчас начнется тренировка, во время которой вам будет сообщаться, верно ли выполняете задание.\n
# Нажмите ПРОБЕЛ, чтобы начать тренировку.\n
# """
mother.addLoop(blocks) # Data Handler works in loops
# Start iterating over blocks
for block in blocks:
    block_condition = blocks_list[blocks.thisIndex] # dictionary of current block condition
    cross_times = [1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500]
    random.shuffle(cross_times)
    # Different messages depending on block condition and experiment language
    if block['condition'] == 'prosaccade':
        if exp_info['language'] == 'Русский':
            instructions_start_text = """
В этой части стрелка будет появляться ТАМ ЖЕ, где и квадрат.
Ваша задача – как можно быстрее перевести взгляд с крестика на квадрат, а затем ответить, куда была направлена стрелка.
Сейчас начнется тренировка, во время которой вам будет сообщаться, верно ли выполняете задание.\n
Нажмите ПРОБЕЛ, чтобы начать тренировку.\n
"""
            instructions_end_text = """
Тренировка окончена, сейчас начнется тест.\n
Помните, в этой части стрелка будет появляться ТАМ ЖЕ, где и квадрат.\n
Ваша задача – как можно быстрее перевести взгляд с крестика на квадрат, а затем ответить, куда была направлена стрелка, нажимая на клавиши на клавиатуре.\n
Нажмите ПРОБЕЛ, чтобы начать тест.\n
"""
            # condition_title.text = "Одноместные стимулы"
        else:
            instructions_start_text = """
In this part, the arrow will appear in the SAME PLACE as the square. 
Your task is to quickly look from the cross to the square, and then answer where the arrow was directed.
Now the training will begin, during which you will be informed whether you are completing the task correctly.\n
Press the SPACEBAR to start your training.\n
"""
            instructions_end_text = """
The training is over, the test will begin now.\n
Remember, in this part the arrow will appear in the SAME PLACE as the square.\n
Your task is to quickly move your eyes from the cross to the square, and then answer where the arrow was directed by pressing the keys on the keyboard.\n
Press the SPACEBAR to start the test.\n
"""
            # condition_title.text = "One-place Stimuli"
    else:
        if exp_info['language'] == 'Русский':
            instructions_start_text = """
В этой части стрелка будет появляться с ПРОТИВОПОЛОЖНОЙ стороны от квадрата.
Ваша задача – как можно быстрее перевести взгляд с крестика в противоположную от квадрата сторону, а затем ответить, куда была направлена стрелка.
Сейчас начнется тренировка, во время которой вам будет сообщаться, верно ли выполняете задание.\n
Нажмите ПРОБЕЛ, чтобы начать тренировку.\n
"""
            instructions_end_text = """
Тренировка окончена, сейчас начнется тест.\n
Помните, в этой части стрелка будет появляться с ПРОТИВОПОЛОЖНОЙ стороны от квадрата.\n
Ваша задача – как можно быстрее перевести взгляд с крестика в противоположную от квадрата сторону, а затем ответить, куда была направлена стрелка, нажимая на клавиши на клавиатуре.\n
Нажмите ПРОБЕЛ, чтобы начать тест.\n
"""
            # condition_title.text = "Разноместные стимулы"
        else:
            instructions_start_text = """
In this part, an arrow will appear on the OPPOSITE side from the square.
Your task is to quickly move your eyes from the cross to the opposite direction of the square.
Now the training will begin, during which you will be informed whether you are completing the task correctly.\n
Press the SPACEBAR to start your training.\n
"""
            instructions_end_text = """
The training is over, the test will begin now.\n
Remember, in this part the arrow will appear on the OPPOSITE side of the square.\n
Your task is to quickly quickly move your eyes from the cross to the opposite direction of the square, and then answer where the arrow was directed by pressing the keys on the keyboard.\n
Press the SPACEBAR to start the test.\n
"""
            condition_title.text = "Different-place Stimuli"
    win.flip()
    core.wait(2.0)
    trials = data.TrialHandler(trialList=trials_list, nReps=TRIALS_NUMBER) 
    mother.addLoop(trials)
    # Training Instructions
    inter_instructions.text = instructions_start_text
    inter_instructions.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    # Start trials, the first 6 are training
    for trial in trials:
        trial_condition = trials_list[trials.thisIndex] # dictionary of current trial condition
        # Cross
        try:
            cross_time = cross_times.pop() # Pick one at random and extract it it
        except IndexError: # If there are no times left, reinitialize and reshuffle the list
            cross_times = [1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500]
            random.shuffle(cross_times)
            cross_time = cross_times.pop()
        for frame in range(int(cross_time // framerate) + 1):
            cross_hori.draw()
            cross_vert.draw()
            win.flip()
        # Blank
        for frame in range(BLANK_FRAMES):
            win.flip()
        # Cue
        if block_condition['condition'] == 'prosaccade':
            cue_side = trial_condition['side'] # cue appears on the same side as the arrow
        else:
            cue_side = ['left', 'right'][1 - ['left', 'right'].index(trial_condition['side'])] # yeah, probably should rewrite to simple if-else
        for frame in range(CUE_FRAMES):
            cue.pos = (0.75 * (-1 + 2 * ['left', 'right'].index(cue_side)), 0) # either -0.75 for left, or 0.75 for right (coordinates). same as arrow below
            cue.draw()
            win.flip()
        # Stimulus
        arrow = eval(f'{trial_condition["target_ori"]}_arrow')
        arrow.pos = (0.75 * (-1 + 2 * ['left', 'right'].index(trial_condition['side'])), 0) # changing x-axis value; if left, 0.75 * (-1 + 2 * 0) = -0.75, if right, 0.75 * (-1 + 2 * 1) = 0.75
        for frame in range(STIMULUS_FRAMES):
            arrow.draw()
            win.flip()
        # Response
        clock = core.Clock()
        win.flip()
        key_press = event.waitKeys(keyList=['left', 'up', 'right'], timeStamped=clock, maxWait=5)
        try:
            resp, rt = key_press[0]
            acc = int(resp == trial_condition["target_ori"]) # Check if response is the same as expected
        except TypeError: # If no answer was given, the == above will fail
            resp, rt = None, None
            acc = 0
        # Data Logging
        mother.addData('Response', resp)
        mother.addData('Accuracy', acc)
        mother.addData('Reaction Time', rt)

        # Feedback if this is the first big Trial (first 6 smoll-trials), i.e. first out of 3 Trials loops, which has 6 trial instances
        if trials.thisRepN == 0:
            # feedback: If no answer given, it'd still be marked as 'wrong'. Is it desirable?
            feedback.text = f'{FEEDBACK_OPTIONS[acc]}'
            feedback.draw()
            win.flip()
            core.wait(3)
            if trials.thisTrialN == len(trials_list) - 1: # If this is the last smoll-trial in Training iteration (first iteration over Trials), we show iaaditional instructions
                    inter_instructions.text = instructions_end_text
                    inter_instructions.draw()
                    win.flip()
                    event.waitKeys(keyList=['space'])

        mother.nextEntry()

# Final Message
instructions.text = instructions_finale
instructions.draw()
win.flip()
core.wait(4.0)

mother.saveAsWideText(filename, delim=',')
win.close()
