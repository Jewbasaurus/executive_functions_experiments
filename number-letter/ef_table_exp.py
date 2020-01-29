# -*- coding: utf-8 -*-

from psychopy import core, data, event, gui, logging, visual
import random
import sys
import os


BLOCKS_NUMBER = 1
TRAINING_LEN = 12
UR_CELL = (1.07, 0.39) # Upper right
UL_CELL = (0.65, 0.39) # Upper left
BR_CELL = (1.07, -0.38) # Bottom right
BL_CELL = (0.65, -0.38) # Bottom left

# Add a global key for exit
event.globalKeys.clear()
event.globalKeys.add(key='z', modifiers=['ctrl'], func=core.quit, name='shutdown')

# Add a Display and get its framerate (specifically, how many ms 1 frame takes)
win = visual.Window(size=[1920, 1080], units='norm', color=[1, 1, 1], fullscr=True)
framerate = win.getMsPerFrame()[2]

# Some visuals
line_hori = visual.Line(win, units='norm', start=(-0.42, 0), end=(0.42, 0), lineColor='black', lineWidth=2.5, name='line_hori')
line_vert = visual.Line(win, units='norm', start=(0, -0.75), end=(0, 0.75), lineColor='black', lineWidth=2.5, name='line_vert')
border_up = visual.Line(win, units='norm', start=(-0.42, 0.75), end=(0.42, 0.75), lineColor='black', lineWidth=2.5, name='border_up')
border_down = visual.Line(win, units='norm', start=(-0.42, -0.75), end=(0.42, -0.75), lineColor='black', lineWidth=2.5, name='border_down')
border_left = visual.Line(win, units='norm', start=(-0.42, 0.75), end=(-0.42, -0.75), lineColor='black', lineWidth=2.5, name='border_left')
border_right = visual.Line(win, units='norm', start=(0.42, 0.75), end=(0.42, -0.75), lineColor='black', lineWidth=2.5, name='border_right')
instructions = visual.TextStim(win, font='arial', color='black', units='norm', height=0.037, wrapWidth=1, ori=0, pos=[0.5, 0])
inter_instructions = visual.TextStim(win, font='arial', color='black', units='norm', height=0.065, wrapWidth=1.1, ori=0, pos=[0.6 , 0])
stimulus = visual.TextStim(win, font='arial', color='black', units='norm', 
                            height=0.3, wrapWidth=None, alignHoriz='center', alignVert='center', ori=0)
feedback = visual.TextStim(win, font='arial', color='black', units='norm', height=0.15, wrapWidth=0.25, ori=0, pos=[0.065, 0])

# Dialog box to choose language
win.winHandle.set_visible(False)
dlg = gui.Dlg(title='Язык/Language')
dlg.addField('Язык/Language', choices=['Русский', 'English'], initial='Русский')
ok = dlg.show()
# If subject presses okay
if ok:
    exp_info = {'language' : dlg.data[0]}
    # exp_info = {a.lower(): b for a, b in zip(dlg.inputFieldNames, dlg.data)}
# If subject presses Cancel
else:
    core.quit()
win.winHandle.set_visible(True)

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
    instructions_start_text = """
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
    instructions_end_text = """
Тренировка окончена, сейчас начнется тест.\nНажмите ПРОБЕЛ, чтобы начать тест.
"""
    instructions_finale = 'Вы завершили тест. Спасибо!'
    STIMULI = ['2Е', '2М', '2Р', '2У', '3О', '3Р', '3Т', '3У', 
               '4А', '4К', '4М', '4У', '5А', '5М', '5О', '5Т',
               '6Е', '6К', '6О', '6Т', '7Е', '7М', '7Р', '7У',
               '8А', '8Е', '8К', '8Т', '9А', '9К', '9О', '9Р']
    FEEDBACK_OPTIONS = ['Неверно', 'Верно']
    FEEDBACK_CONTINUE = 'Нажмите ПРОБЕЛ'
else:
    instructions_start_text = """
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
    instructions_end_text = """
The training is over, the test will begin now.\nPress the SPACEBAR to start the test.
"""
    instructions_finale = 'You have completed the test. Thank you!'
    STIMULI = ['2E', '2M', '2P', '2U', '3O', '3P', '3T', '3U', 
               '4A', '4K', '4M', '4U', '5A', '5M', '5O', '5T',
               '6E', '6K', '6O', '6T', '7E', '7M', '7P', '7U',
               '8A', '8E', '8K', '8T', '9A', '9K', '9O', '9P'] 
    FEEDBACK_OPTIONS = ['Wrong', 'Right']
    FEEDBACK_CONTINUE = 'Press SPACEBAR'

mother = data.ExperimentHandler(name="experiment_handler", extraInfo=exp_info, dataFileName=f'data/{filename}')
blocks_list = [{'trials_number' : tn, 'condition' : cond} for tn, cond in  [(32, 'top'), (32, 'bot'), (128, 'both')]] # 3 blocks
blocks = data.TrialHandler(trialList=blocks_list, nReps=BLOCKS_NUMBER, method='sequential') 

mother.addLoop(blocks)

responses = []
for block in blocks:
    # Instructions before every block
    line_vert.autoDraw = False
    line_hori.autoDraw = False
    border_right.autoDraw = False
    border_left.autoDraw = False
    border_up.autoDraw = False
    border_down.autoDraw = False
    win.flip()
    instructions.text = instructions_start_text
    instructions.draw()
    win.flip()
    # Wait for response
    event.waitKeys(keyList=['space'])

    # block_condition = blocks_list[blocks.thisIndex] # dictionary of current block condition
    # Choose which cells to use
    if block['condition'] == 'top':
        trials_list = [{'cell' : cell} for cell in [UL_CELL, UR_CELL]]
    elif block['condition'] == 'bot':
        trials_list = [{'cell' : cell} for cell in [BL_CELL, BR_CELL]]
    else:
        trials_list = [{'cell' : cell} for cell in [BR_CELL, BL_CELL, UL_CELL, UR_CELL]]
    # A trial is a sequence of all possible cells for the block, e.g. Trial = [UpRight, Upleft]; here we calculate the number of repetitions
    trials_number = block['trials_number'] // len(trials_list) 
    test_trials_number = TRAINING_LEN // len(trials_list)
    train_trials = data.TrialHandler(trialList=trials_list, nReps=test_trials_number, method='sequential')
    trials = data.TrialHandler(trialList=trials_list, nReps=trials_number, method='sequential')
    mother.addLoop(train_trials)
    mother.addLoop(trials)
    # The Matrix; ALWAYS on screen
    line_vert.autoDraw = True
    line_hori.autoDraw = True
    border_right.autoDraw = True
    border_left.autoDraw = True
    border_up.autoDraw = True
    border_down.autoDraw = True
    win.flip()
    for train_trial in train_trials:
        # Stimulus
        stimulus.text = random.choice(STIMULI)
        stimulus.pos = train_trial['cell']
        # Present a stimulus untill the subject reacts
        while True:
            stimulus.draw()
            win.flip()
            clock = core.Clock()
            key_press = event.waitKeys(keyList=['lctrl', 'rctrl'], timeStamped=clock)
            print(key_press)
            break
        # TRAIN FEEDBACK
        resp, rt = key_press[0]
        if train_trial['cell'][1] > 0: # Depending on y coordinate -- above or below -- we address different parts of a stimulus
            target = int(stimulus.text[0]) % 2  # if it was even, the result is 0, 1 otherwise
        else:
            target = stimulus.text[1] not in ['А', 'Е', 'Ё', 'И', 'О', 'У', 'Ы', 'Ю', 'Я',
                                     'A', 'E', 'I', 'O', 'U', 'Y'] # if consonant, 0, 1 otherwise
        acc = int(resp == ['rctrl', 'lctrl'][target])
        line_vert.autoDraw = False
        line_hori.autoDraw = False
        border_right.autoDraw = False
        border_left.autoDraw = False
        border_up.autoDraw = False
        border_down.autoDraw = False
        win.flip()
        feedback.text = f'{FEEDBACK_OPTIONS[acc]}'
        feedback.draw()
        win.flip()
        core.wait(2)
        win.flip()
        core.wait(0.15)
        win.flip()
        line_vert.autoDraw = True
        line_hori.autoDraw = True
        border_right.autoDraw = True
        border_left.autoDraw = True
        border_up.autoDraw = True
        border_down.autoDraw = True
        win.flip()
        mother.nextEntry() # since this is training, we don't care about rt and stuff
    line_vert.autoDraw = False
    line_hori.autoDraw = False
    border_right.autoDraw = False
    border_left.autoDraw = False
    border_up.autoDraw = False
    border_down.autoDraw = False
    win.flip()
    inter_instructions.text = instructions_end_text
    inter_instructions.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    line_vert.autoDraw = True
    line_hori.autoDraw = True
    border_right.autoDraw = True
    border_left.autoDraw = True
    border_up.autoDraw = True
    border_down.autoDraw = True
    win.flip()
    for trial in trials:
        # Stimulus
        stimulus.text = random.choice(STIMULI)
        stimulus.pos = trial['cell']
        while True:
            stimulus.draw()
            win.flip()
            clock = core.Clock()
            key_press = event.waitKeys(keyList=['lctrl', 'rctrl'], timeStamped=clock)
            break
        resp, rt = key_press[0]
        if trial['cell'][1] > 0: # Depending on y coordinate -- above or below -- we address different parts of a stimulus
            target = int(stimulus.text[0]) % 2  # if it was even, the result is 0, 1 otherwise
        else:
            target = stimulus.text[1] not in ['А', 'Е', 'Ё', 'И', 'О', 'У', 'Ы', 'Ю', 'Я',
                                     'A', 'E', 'I', 'O', 'U', 'Y'] # if consonant, 0, 1 otherwise
        acc = int(resp == ['rctrl', 'lctrl'][target])
        # Data Logging
        mother.addData('True Response', ['rctrl', 'lctrl'][target])
        mother.addData('Response', resp)
        mother.addData('Accuracy', acc)
        mother.addData('Reaction Time', rt)
        mother.addData('Stimulus', stimulus.text)
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
inter_instructions.pos = [0.75, 0]
inter_instructions.text = instructions_finale
inter_instructions.draw()
win.flip()
core.wait(4.0)

mother.saveAsWideText(f'data/{filename}', delim=',')
win.close()
