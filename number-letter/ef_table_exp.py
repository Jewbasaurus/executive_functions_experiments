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
instructions = visual.TextStim(win, font='arial', color='black', units='norm', height=0.05, wrapWidth=None, ori=0, pos=[0.5, 0])

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
    exp_info['experiment_name'] = 'Table'
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
    В этом тесте необходимо быстро переключать внимание. На экране
    появится квадрат, разделенный на четыре части. В квадрате будут
    появляться пары из букв и цифр.\n
    Если пара появилась в верхней части квадрата, определите, четное
    или нечетное число в паре. Нажмите клавишу CTRL слева на
    клавиатуре, если цифра нечетная или CTRL справа на клавиатуре, если
    цифра четная.\n
    Если пара появилась в нижней части квадрата, определите, гласная
    или согласная буква в паре. Нажмите клавишу CTRL слева на
    клавиатуре, если буква согласная или CTRL справа на клавиатуре, если
    буква гласная.\n
    Итак, левый CTRL для нечетных чисел и согласных букв, правый CTRL для
    четных чисел и гласных букв.\n
    Нажмите ПРОБЕЛ, чтобы начать тест.
    """
    instructions_finale = 'Вы завершили тест. Спасибо!'
    STIMULI = ['2А', '2М', '2Р', '2У', '3О', '3Р', '3Е', '3У', 
               '4А', '4К', '4О', '4У', '5А', '5М', '5О', '5Т',
               '6Е', '6К', '6М', '6Т', '7Е', '7М', '7Р', '7У',
               '8Е', '8Е', '8К', '8Т', '9А', '9К', '9О', '9Р']
else:
    instructions.text = """
    In this test, you need to quickly switch attention. A square will appear on
    the screen, divided into four parts. Pairs of letters and numbers will appear
    in the square.\n
    If a pair appears at the top of the square, answer whether the odd or even
    number is in the pair. Press the CTRL key on the left of the keyboard if the
    number is odd or the CTRL on the right of the keyboard if the number is even.\n
    If a pair appears at the bottom of the square, answer whether a vowel or
    consonant is in the pair. Press the CTRL key on the left of the keyboard if the
    letter is consonant or the CTRL on the right of the keyboard if the letter is a
    vowel.\n
    Remember, left CTRL for odd numbers and consonants, right CTRL for even
    numbers and vowels.\n
    Press the SPACEBAR to start the test.
    """
    instructions_finale = 'You have completed the test. Thank you!'
    STIMULI = ['2A', '2M', '2P', '2U', '3O', '3P', '3T', '3U', 
               '4A', '4K', '4O', '4U', '5A', '5M', '5O', '5T',
               '6E', '6K', '6M', '6T', '7E', '7M', '7P', '7U',
               '8E', '8E', '8K', '8T', '9A', '9K', '9O', '9P']   
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
