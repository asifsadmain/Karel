import sys

sys.path.append('.')

from prog_policies.karel import KarelDSL
from prog_policies.karel_tasks import get_task_cls
from prog_policies.search.utils import evaluate_program
from prog_policies.karel import KarelEnvironment

if __name__ == '__main__':
    
    dsl = KarelDSL()
    
    task_cls = get_task_cls('Seeder')
    
    env_args = {
        "env_height": 8,
        "env_width": 8,
        "crashable": True,
        "leaps_behaviour": False,
        "max_calls": 10000
    }
    
    task_envs = [task_cls(env_args, i) for i in range(8)]
    
    program_str = "DEF run m( REPEAT R=3 r( putMarker turnRight IF c( rightIsClear c) i( turnRight turnRight move move i) WHILE c( frontIsClear c) w( turnLeft putMarker turnRight move w) r) m)"
    
    program = dsl.parse_str_to_node(program_str)
    
    # reward = evaluate_program(program, dsl, task_envs)
    task_envs[0].reset_environment()
    # print(task_envs[0].environment.get_state())
    prev_prev_action = None
    prev_action = None
    SAR = ""

    for action in program.run_generator(task_envs[0].environment):
        state = task_envs[0].environment.get_hero_pos()
        reward = task_envs[0].get_reward(task_envs[0].environment)[1]
        
        if (reward > 0):
            if (prev_prev_action and prev_action):
                # print("Actions:", prev_prev_action.name, prev_action.name, action.name)
                SAR += f"Actions: {prev_prev_action.name} {prev_action.name} {action.name}\n"
            elif (prev_action):
                # print("Actions:", prev_action.name, action.name)
                SAR += f"Actions: {prev_action.name} {action.name}\n"
            else:
                # print("Action:", action.name)
                SAR += f"Actions: {action.name}\n"
            # print("Bot Position:", state[0:2])
            # print("Reward:", reward)
            # print()
            # SAR += "Bot Position:" + state[0:2] + '\n'
            SAR += f"Bot Position: {state[0:2]}\n"
            SAR += f"Reward: {reward}\n\n"
        # print(task_envs[0].get_reward(task_envs[0].environment)[1])
        prev_prev_action = prev_action
        prev_action = action
    
    print(SAR)
