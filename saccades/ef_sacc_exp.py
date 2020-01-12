# -*- coding: utf-8 -*-

from psychopy import core, data, event, gui, logging, visual
import random
import sys
import os

# 3 blocks; 2 trials + 1 training trial
BLOCKS_NUMBER = 3
TRIALS_NUMBER = 3

# TIMES
READY_TITLE_FRAME = 60 # 1000 ms
# FIX_CROSS TIME is randomized in every block later on
BLANK_FRAMES = 12 # 200 ms
CUE_FRAMES =  15 # 250 ms
STIMULUS_FRAMES =  6# 100 ms

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
instructions = visual.TextStim(win, font='arial', color='black', units='norm', height=0.037, wrapWidth=None, ori=0, pos=[0.5, 0])
ready_prompt = visual.TextStim(win, font='arial', color='black', units='norm', height=0.075, wrapWidth=None, ori=0, pos=[0.85, 0])
condition_title = visual.TextStim(win, font='arial', color='black', units='norm', height=0.075, wrapWidth=None, ori=0, pos=[0.6, 0])
feedback = visual.TextStim(win, font='arial', color='black', units='norm', height=0.075, wrapWidth=None, ori=0, pos=[0.7, 0])

# Dialog box before an experiment session
win.winHandle.set_visible(False) # in FS experiment window overlays all others. We rend it invisible...
dlg = gui.Dlg(title='Experiment')
dlg.addField('ID', initial='0')
dlg.addField('Sex', choices=['male', 'female', 'not defined'])
dlg.addField('Age')
dlg.addField('Language', choices=['Русский', 'English'], initial='Русский')
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
    стрелка будет появляться там же, где и квадрат, а в других — с
    противоположной стороны. Ваша задача — ответить, куда была
    направлена стрелка, нажимая на клавиши стрелок вверх, вправо или
    влево на клавиатуре.\n
    Нажмите ПРОБЕЛ, чтобы перейти к первой части.
    """
    instructions_finale = 'Вы завершили тест. Спасибо!'
    ready_prompt.text = 'Приготовьтесь'
    feedback_options = ['Неверно', 'Правильно']
    feedback_continue = 'Нажмите ПРОБЕЛ'
else:
    instructions.text = """
    In this test you must carefully monitor the objects on the screen. The test is
    divided into several parts. Instructions will be repeated before the beginning
    of each part. Please read the instructions carefully as they will vary.\n
    At the beginning of each task, a cross will appear in the center of the
    screen. Fix your gaze on it. Then a square will appear on the right or left of
    the screen, and after it an arrow will appear. In some cases the arrow will
    appear in the same place as the square, and on the opposite side in others. 
    Your task is to answer where the arrow was directed by pressing the
    arrow keys up, left or right on the keyboard.\n
    Press the SPACEBAR to go to the first part.
    """
    instructions_finale = 'You have completed the test. Thank you!'
    ready_prompt.text = 'Ready'
    feedback_options = ['Wrong', 'Right']
    feedback_continue = 'Press SPACEBAR'
instructions.draw()
win.flip()
# Wait for response
event.waitKeys(keyList=['space'])

mother = data.ExperimentHandler(name="experiment_handler", extraInfo=exp_info, dataFileName=f'data/{filename}')
blocks_list = [{'condition': b} for b in ['prosaccade', 'antisaccade']] # 2 blocks, 3 times each
blocks = data.TrialHandler(trialList=blocks_list, nReps=BLOCKS_NUMBER) 
trials_list = [{'side': side, 'target_ori': ori} for side in ['left', 'right'] for ori in ['left', 'up', 'right']] # 2 places (left, right) * 3 targets (l, u, r), 3 times each
responses = []

mother.addLoop(blocks)
# Start blocks
for block in blocks:
    block_condition = blocks_list[blocks.thisIndex] # dictionary of current block condition
    cross_times = [1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500]
    random.shuffle(cross_times)
    if block['condition'] == 'prosaccade':
        if exp_info['language'] == 'Русский':
            instructions_start_text = """
            В этой части стрелка будет появляться там же, где и квадрат. Ваша
            задача – как можно быстрее перевести взгляд с крестика на квадрат, а
            затем ответить, куда была направлена стрелка.\n
            Сейчас начнется тренировка, во время которой вам будет
            сообщаться, верно ли выполняете задание.\n
            Нажмите ПРОБЕЛ, чтобы начать тренировку.
            """
            instructions_end_text = """
            Тренировка окончена, сейчас начнется тест.\n
            Помните, в этой части стрелка будет появляться там же, где и
            квадрат. Ваша задача – как можно быстрее перевести взгляд с
            крестика на квадрат, а затем ответить, куда была направлена стрелка,
            нажимая на клавиши на клавиатуре.\n
            Нажмите ПРОБЕЛ, чтобы начать тест.
            """
            # condition_title.text = "Одноместные стимулы"
        else:
            instructions_start_text = """
            In this part, the arrow will appear in the same place as the square. Your
            task is to quickly look from the cross to the square, and then answer where
            the arrow was directed.\n
            Now the training will begin, during which you will be informed whether you
            are completing the task correctly.\n
            Press the SPACEBAR to start your training.
            """
            instructions_end_text = """
            The training is over, the test will begin now.\n
            Remember, in this part the arrow will appear in the same place as the
            square. Your task is to quickly move your eyes from the cross to the
            square, and then answer where the arrow was directed by pressing the
            keys on the keyboard.\n
            Press the SPACEBAR to start the test.
            """
            # condition_title.text = "One-place Stimuli"
    else:
        if exp_info['language'] == 'Русский':
            instructions_start_text = """
            В этой части стрелка будет появляться с противоположной стороны от
            квадрата. Ваша задача – как можно быстрее перевести взгляд с
            крестика в противоположную от квадрата сторону, а затем ответить,
            куда была направлена стрелка.\n
            Сейчас начнется тренировка, во время которой вам будет
            сообщаться, верно ли выполняете задание.\n
            Нажмите ПРОБЕЛ, чтобы начать тренировку.
            """
            instructions_end_text = """
            Тренировка окончена, сейчас начнется тест.\n
            Помните, в этой части стрелка будет появляться с противоположной
            стороны от квадрата. Ваша задача – как можно быстрее перевести
            взгляд с крестика в противоположную от квадрата сторону, а затем
            ответить, куда была направлена стрелка, нажимая на клавиши на
            клавиатуре.\n
            Нажмите ПРОБЕЛ, чтобы начать тест.
            """
            # condition_title.text = "Разноместные стимулы"
        else:
            instructions_start_text = """
            In this part, an arrow will appear on the opposite side from the square. Your
            task is to quickly move your eyes from the cross to the opposite direction of
            the square.\n
            Now the training will begin, during which you will be informed whether you
            are completing the task correctly.\n
            Press the SPACEBAR to start your training.
            """
            instructions_end_text = """
            The training is over, the test will begin now.\n
            Remember, in this part the arrow will appear on the opposite side of the
            square. Your task is to quickly quickly move your eyes from the cross to the
            opposite direction of the square, and then answer where the arrow was
            directed by pressing the keys on the keyboard.\n
            Press the SPACEBAR to start the test.
            """
            # condition_title.text = "Different-place Stimuli"
    # Condition Header
    # condition_title.draw()
    win.flip()
    core.wait(2.0)
    trials = data.TrialHandler(trialList=trials_list, nReps=TRIALS_NUMBER) 
    mother.addLoop(trials)
    # Training Instructions
    instructions.text = instructions_start_text
    instructions.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    # Start training
    for trial in trials:
        trial_condition = trials_list[trials.thisIndex] # dictionary of current trial condition
        # Ready
        for frame in range(READY_TITLE_FRAME):  
            ready_prompt.draw()
            win.flip()
        # Cross
        try:
            cross_time = cross_times.pop() # Pick one at random and remove it
        except IndexError: # If there are no times left, reinitialize the list
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
            cue_side = trial_condition['side']
        else:
            cue_side = ['left', 'right'][1 - ['left', 'right'].index(trial_condition['side'])]
        for frame in range(CUE_FRAMES):
            cue.pos = (0.75 * (-1 + 2 * ['left', 'right'].index(cue_side)), 0)
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
            acc = int(resp == trial_condition["target_ori"])
        except TypeError:
            resp, rt = None, None
            acc = 0
        # Data Logging
        mother.addData('Response', resp)
        mother.addData('Accuracy', acc)
        mother.addData('Reaction Time', rt)

        # Feedback if this is the first big Trial (first 6 smoll-trials)
        if trials.thisRepN == 0:
            # feedback: If no answer given, it'd still be marked as 'wrong'. Is it desirable?
            feedback.text = f'{feedback_options[acc]}\n{feedback_continue}'
            feedback.draw()
            win.flip()
            event.waitKeys(keyList=['space'], maxWait=5)
            if trials.thisTrialN == len(trials_list) - 1:
                    instructions.text = instructions_end_text
                    instructions.draw()
                    win.flip()
                    event.waitKeys(keyList=['space'])

        mother.nextEntry()

# Finale Message
instructions.text = instructions_finale
instructions.draw()
win.flip()
core.wait(4.0)

mother.saveAsWideText(filename, delim=',')
win.close()
