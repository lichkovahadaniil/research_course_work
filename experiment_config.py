from dataclasses import dataclass


DOMAIN_TYPES = ["logistics"]
TASK_NAMES = ["alpha"]
PROBLEM_IDS = [f"p{index}" for index in range(1, 21)]
MODEL_NAMES = [
    "deepseek-v4-flash",
    "glm-4.7-flash",
]


@dataclass(frozen=True, order=True)
class ProblemRef:
    task: str
    problem: str

    @property
    def label(self) -> str:
        return f"{self.task}/{self.problem}"


PROBLEM_TYPE_BY_ID = {
    "p1": "s01_l08",
    "p2": "s01_l15",
    "p3": "s18_l22",
    "p4": "s24_l30",
    "p5": "s01_l35",
    "p6": "s01_l47",
    "p7": "s01_l53",
    "p8": "s10_l06",
    "p9": "s43_l09",
    "p10": "s09_l10",
    "p11": "s18_l12",
    "p12": "s18_l14",
    "p13": "s22_l17",
    "p14": "s19_l19",
    "p15": "s19_l24",
    "p16": "s27_l27",
    "p17": "s16_l32",
    "p18": "s16_l38",
    "p19": "s10_l41",
    "p20": "s09_l45",
}
PROBLEM_TYPE_ORDER = [PROBLEM_TYPE_BY_ID[problem_id] for problem_id in PROBLEM_IDS]
PROBLEM_TYPE_LABELS = {
    problem_type: problem_type.upper()
    for problem_type in PROBLEM_TYPE_ORDER
}
PROBLEM_REFS = [
    ProblemRef(task_name, problem_id)
    for task_name in TASK_NAMES
    for problem_id in PROBLEM_IDS
]
