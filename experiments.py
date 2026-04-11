from domain_generation import *
from api_call import *

if __name__ == '__main__':
    for d in DOMAIN_TYPES:

        src_path = Path(f'materials/{d}')
        for i in range(1, 21):
            name = f'p{i:02d}'
            curr_path = src_path / name 
            domains = ['domain_canonical.pddl', 'domain_dispersion.pddl', 'domain_frequency.pddl',
                       'domain_optimal.pddl'] + [f'domain_random_{j:02d}.pddl' for j in range(1, 11)]
            problem = curr_path / f'p{i:02d}.pddl'

            for t in domains:
                domain = curr_path / t
                res = call_openrouter(domain, problem)