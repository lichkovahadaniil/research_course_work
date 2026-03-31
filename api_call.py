from dotenv import load_dotenv
from groq import Groq
import os
import re

load_dotenv()

DOMAIN = 'domains/original/blocksworld/domain.pddl'
PROBLEM = 'domains/original/blocksworld/instances/instance-1.pddl'
PLAN = 'plans/plan_1.txt'

def call(domain=DOMAIN, problem=PROBLEM, plan_path=PLAN):
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    def read_pddl(path):
        with open(path, 'r') as f:
            return f.read()
        
    domain_text = read_pddl(domain)
    problem_text = read_pddl(problem)

    prompt = f"""
    You are an expert in PDDL planning.

    Given the following domain and problem, generate only a valid plan.

    Domain:
    {domain_text}

    Problem:
    {problem_text}

    Format example:
    (move a b c)
    (stack a b)
    ...

    Return ONLY the plan as a sequence of actions, one per line.
    """

    response = client.chat.completions.create(
        model='openai/gpt-oss-20b',
        messages = [
            {'role': 'user', 'content': prompt}
        ],
        temperature=0,
    )

    plan = response.choices[0].message.content

    def cleaning(plan):
        actions = re.findall(r"\(.*?\)", plan)
        return "\n".join(actions)

    plan = cleaning(plan)

    with open(plan_path, "w") as f:
        f.write(plan)

    return plan