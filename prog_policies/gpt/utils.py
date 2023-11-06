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

def is_balanced_parentheses(s):
    stack = []
    for char in s:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return not stack

def replace_keywords(program):
    keywords = ["IF", "WHILE", "IFELSE", "ELSE", "REPEAT", "DEF"]
    program_list = program.split()
    keyword_list = [word for word in program_list if word in keywords]
    for i in range(len(keyword_list) - 1):
        if keyword_list[i] == "IF" and keyword_list[i + 1] == "ELSE":
            keyword_list[i] = "IFELSE"
    new_program = []
    keyword_index = 0
    for word in program_list:
        if word in keywords:
            new_program.append(keyword_list[keyword_index])
            keyword_index += 1
        else:
            new_program.append(word)
    return ' '.join(new_program)

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
    prev_word = ''
    word = ''
    count = 1

    while i < len(program):
        if program[i].isupper():
            word_builder += program[i]
        elif program[i] == ' ' and program[i-1].isupper():
            prev_word = word
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

def parse_response(program):
    program = program.replace('\n', ' ').replace('\t', '').replace(';', '')
    program = re.sub(' +', ' ', program)
    program = add_space_after_bracket(program)
    program = replace_keywords(program)
    program = construct_valid_program(program.strip())
    
    return program

def indent(program_string):
    list_to_check = ["m(", "i(", "i)", "e(", "e)", "w(", "w)", "r(", "r)", "move", "turnLeft", "turnRight", "putMarker", "pickMarker"]

    i = 0
    while i < len(program_string):
        found_match = False
        for item in list_to_check:
            if program_string[i:i+len(item)] == item:
                new_program_string += item + '\n'
                i += len(item)
                found_match = True
                break
        if not found_match:
            new_program_string += program_string[i]
            i += 1

    return new_program_string

# program = f"""
# DEF run m(
#   REPEAT R=4 r(
#     IFELSE c(frontIsClear) i(
#       move
#       IFELSE c(rightIsClear) i(
#         turnRight
#         move
#         turnLeft
#         move
#       ) ELSE (
#         turnLeft
#         move
#         turnRight
#         move
#       )
#     ) ELSE (
#       turnRight
#       move
#       turnLeft
#       move
#     )
#     putMarker
#     turnRight
#     turnRight
#   )
# )
# """

# print(is_balanced_parentheses(program))
