import re

def add_space_after_bracket(program):
    new_program = ''
    for i in range(len(program)):
        new_program += program[i]
        if program[i] == '(' and i+1 < len(program) and program[i+1] != ' ':
            new_program += ' '
    return new_program

def transform_program(program):
    # Define the transformations
    transformations = {
        'w(': 'w(',
        'i(': 'i(',
        'e(': 'e(',
        'c(': 'c(',
        ') w': 'w)',
        ') i': 'i)',
        ') e': 'e)',
        ') c': 'c)',
    }

    # Apply the transformations
    for old, new in transformations.items():
        program = program.replace(old, new)

    return program


program = f"""
DEF run m(
    WHILE c(frontIsClear) w(
        pickMarker
    w)
    move
    IFELSE c(leftIsClear) i(
        turnLeft
    i) ELSE e(
        turnRight
    e)
    move
    REPEAT R=2 r(
        IF c(frontIsClear) i(
            putMarker
        i)
        turnRight
        move
    r)
m)
"""

program = program.replace('\n', ' ').replace('\t', '').replace(';', '')
program = re.sub(' +', ' ', program)
program = add_space_after_bracket(program)
# program = transform_program(program)
print(program)
