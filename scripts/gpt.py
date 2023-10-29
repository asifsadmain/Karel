import sys

sys.path.append('.')

from prog_policies.karel import KarelDSL
from prog_policies.karel_tasks import get_task_cls
from prog_policies.search.utils import evaluate_program

if __name__ == '__main__':
    
    dsl = KarelDSL()
    
    task_cls = get_task_cls('Harvester')
    
    env_args = {
        "env_height": 8,
        "env_width": 8,
        "crashable": True,
        "leaps_behaviour": False,
        "max_calls": 10000
    }
    
    task_envs = [task_cls(env_args, i) for i in range(8)]
    
    program_str = "DEF run m( REPEAT R=6 r(IF c( markerPresent c) i( pickMarker i) else e( move e) r) m)"
    
    program = dsl.parse_str_to_node(program_str)
    
    reward = evaluate_program(program, dsl, task_envs)
    
    print(reward)
