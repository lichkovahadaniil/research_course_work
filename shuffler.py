import pddlpy

def actions_list(domain, problem):
    dp = pddlpy.DomainProblem(domain, problem)
    return list(dp.operators()) # list of actions

