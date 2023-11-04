import re

def insert_character(original_string, character, position):
    return original_string[:position] + character + original_string[position:]

def add_space_after_bracket(program):
    new_program = ''

    for i in range(len(program)):
        new_program += program[i]
        if program[i] == '(' and i+1 < len(program) and program[i+1] != ' ':
            new_program += ' '
        if i+1 < len(program) and program[i+1] == ')' and program[i] != ' ' and program[i-1] != ' ':
            new_program += ' '
    return new_program

def update_program(program, word, idx):
    if (word == "DEF") and program[idx-1] != 'm':
        program = insert_character(program, 'm', idx)
    elif (word == "CONDITION" and program[idx-1] != 'c'):
        program = insert_character(program, 'c', idx)
    elif (word == "WHILE" and program[idx-1] != 'w'):
        program = insert_character(program, 'w', idx)
    elif (word == "IFELSE" and program[idx-1] != 'i'):
        program = insert_character(program, 'i', idx)
    elif (word == "IF" and program[idx-1] != 'i'):
        program = insert_character(program, 'i', idx)
    elif (word == "ELSE" and program[idx-1] != 'e'):
        program = insert_character(program, 'e', idx)
    elif (word == "REPEAT" and program[idx-1] != 'r'):
        program = insert_character(program, 'r', idx)
    else:
        return program, idx

    return program, idx+1

def construct_valid_program(program):
    stack = []
    i = 0
    word_builder = ''
    word = ''
    count = 1

    while i < len(program):
        if program[i].isupper():
            word_builder += program[i]
        elif program[i] == ' ' and program[i-1].isupper():
            word = word_builder
            count = 1
        elif program[i] == '(':
            stack.append(word)
            word_builder = ''
            if ((word == "WHILE" or word == "IF" or word == "IFELSE") and count == 1):
                stack[-1] = "CONDITION"
                program, i = update_program(program, "CONDITION", i)
            else:
                program, i = update_program(program, word, i)
            # print("in =", stack[-1])
            # print("stack =", stack)
        elif program[i] == ')':
            w = stack.pop()
            # print("out =",w)
            # print("stack =", stack)
            program, i = update_program(program, w, i)
            word_builder = ''
            count += 1
        elif program[i] == ' ':
            word_builder = ''
        i += 1
    return program


program = f"""
DEF run m(
    IF c(frontIsClear) i(
        move
    )
    ELSE e(
        turnRight
    )
    REPEAT R=4 r(
        IF c(leftIsClear) i(
            turnLeft
        )
        ELSE e(
            putMarker
            move
        )
    )
    turnRight
    REPEAT R=4 r(
        move
    )
    IF c(markersPresent) i(
        pickMarker
    )
    move
)
"""

program = program.replace('\n', ' ').replace('\t', '').replace(';', '')
program = re.sub(' +', ' ', program)
program = add_space_after_bracket(program)
program = construct_valid_program(program.strip())
print(program)
