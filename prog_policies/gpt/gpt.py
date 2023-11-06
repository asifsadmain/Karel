import sys
sys.path.append('.')

import re
import openai
from prog_policies.karel import KarelDSL
from .utils import parse_response, indent, is_balanced_parentheses
from prog_policies.search.utils import evaluate_program
from prog_policies.karel_tasks import get_task_cls


openai.api_key = "OPENAI_API_KEY"

dsl = f"""
The following is the Context Free Grammar (CFG) for the Karel domain:

```
Program ρ := DEF run m( s m)
Repetition n := Number of repetitions
Perception h := frontIsClear | leftIsClear | rightIsClear | markersPresent | noMarkerPresent
Condition b := h | not h
Action a := move | turnLeft | turnRight | putMarker | pickMarker
Statement s := WHILE c( b c) w( s w) | s1;s2 | a | REPEAT R=n r( s r) | IF c( b c) i( s i) |
IFELSE c( b c) i(s1 i) ELSE e( s2 e)
```

"""

dsl_explanation = f"""
The CFG is explained below in the "CFG Explanation" section:

CFG Explanation:
```
Program ρ: The main program 'm' named as "run" which contains one or many statements 's'
Repetition n: A number that indicates the number of repetitions
Perception h: Some boolean variables that provide the idea of the environment.
Condition b: Perception h or not perception h that returns true or false
Action a: Some actions to be taken by the agent
Statement s: Consists of statements such as WHILE, IF, IFELSE, REPEAT.
```

"""

program_writing_guidelines = f"""
To write a program from the given CFG, the following "Program Writing Guidelines" must be followed:
Program Writing Guidelines:
```
1. Before the beginning of a statement, it should start with a letter indicating the statement. The ending should also be indicated by the same letter. For example, in "WHILE c( b c) w( s w)", "c(" indicates the starting of a condition and "c)" indicates the end of that condition. Then "w(" indicates the starting of a WHILE statement and "w)" indicates the end of that statement.
2. The program must be written inside a single "DEF run m(s m)"
3. Avoid writing semicolon after a line.
```

"""

environment_details = f"""
Here is the details of the environment and instructions about the goal in the "EnvironmentDetails" section:

EnvironmentDetails:
```
I have a 8x8 grid and a bot at the bottom left which will interact inside the grid. The whole grid is empty, \
i.e. it does not have any marker inside. There are reward signals that depend on the interactions of the bot \
inside the grid. Usually, the rewards depend on picking or putting markers in different circumstances. \
The interaction of the bot will be decided by the programs written by following the above DSL. \
The reward signals obtained from the program will be provided back once we evaluate the program in the \
environment, so you will be asked to generate other programs based on the feedback the environment provides. \
The name of the task is 'FourCorners' and the goal is to find a program that will maximize the reward. 
```

"""


def get_response_from_api(user_message):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": user_message}
        ],
    temperature=0.7
    )
    
    return response['choices'][0]['message']['content']

def generate_initial_program():
    tasks = f"""
    Now your tasks are the following 3:
    1. Read carefully about the details of the environment, the CFG and its explanation.
    2. Follow the CFG and the program writing guidelines and write a program without that will gain the maximum reward inside this given environment.
    3. Write the program inside <program></program> tag.
    """

    user_message = dsl + dsl_explanation + program_writing_guidelines + environment_details + tasks

    response = get_response_from_api(user_message)

    pattern = r'<program>(.*?)<\/program>'
    matches = re.findall(pattern, response, re.DOTALL)

    program = matches[0]
    program = parse_response(program)

    return program


def get_initial_program():
    dsl = KarelDSL()
    program = generate_initial_program()

    while True:
        try:
            dsl.parse_str_to_node(program)
            break
        except Exception:
            print("Sending another request...")
            program = generate_initial_program()

    print("Program from GPT =", program)
    return program


def generate_next_program(latest_program, latest_reward):
    latest_program = f"""
    The latest program obtained from the interactive system in this karel domain is:
    ```
    {latest_program}
    ```

    This program generates a reward of {latest_reward}.

    """

    tasks = f"""
    Your tasks are the following 2:
    1. Analyze the latest program and try to understand what is going on in the context of 'FourCorners' environment in Karel domain.
    2. Inside a <newProgram></newProgram> tag, write another program which can achieve a better reward than this one.
    """

    user_message = dsl + dsl_explanation + program_writing_guidelines + environment_details + latest_program + tasks

    valid_program_found = False
    program = ""
    matches = None

    while (not valid_program_found):
        response = get_response_from_api(user_message)
        # print(response)

        pattern = r'<newProgram>\n(.*?)\n<\/newProgram>'

        matches = re.findall(pattern, response, re.DOTALL)

        if (not matches):
            # print("///////////////")
            pattern = r'```\n(.*?)\n```'
            matches = re.findall(pattern, response, re.DOTALL)

        if (matches):
            if (is_balanced_parentheses(matches[0])):
                valid_program_found = True

    program = matches[0]
    # print("=====================")
    # print(program)

    return program

def get_next_program(latest_program, latest_reward):
    dsl = KarelDSL()
    program = generate_next_program(latest_program, latest_reward)
    program = parse_response(program)
    # print("Program from GPT =", program)

    while True:
        try:
            dsl.parse_str_to_node(program)
            break
        except Exception:
            # print("Program", program, " is not valid")
            print("Invalid program from GPT =", program)
            print("Sending another request...")
            program = generate_next_program(latest_program, latest_reward)
            program = parse_response(program)

    print("Program from GPT =", program)
    task_cls = get_task_cls('Seeder')
    env_args = {
        "env_height": 8,
        "env_width": 8,
        "crashable": True,
        "leaps_behaviour": False,
        "max_calls": 10000
    }
    task_envs = [task_cls(env_args, i) for i in range(8)]
    print("Reward =", evaluate_program(program, dsl, task_envs))

    return dsl.parse_str_to_node(program)
