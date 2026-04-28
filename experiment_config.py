from dataclasses import dataclass


DOMAIN_TYPES = ["logistics"]
TASK_NAMES = ["alpha", "north", "cold", "port"]
PROBLEM_IDS = [f"p{index}" for index in range(1, 8)]
MODEL_NAMES = [
    "grok-4.1-fast",
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


PROBLEM_TYPE_ORDER = [
    "prefix_8",
    "prefix_15",
    "slice_22",
    "slice_30",
    "prefix_35",
    "prefix_47",
    "full_53",
]
PROBLEM_TYPE_LABELS = {
    "prefix_8": "Prefix 8",
    "prefix_15": "Prefix 15",
    "slice_22": "Slice 22",
    "slice_30": "Slice 30",
    "prefix_35": "Prefix 35",
    "prefix_47": "Prefix 47",
    "full_53": "Full 53",
}
PROBLEM_TYPE_BY_ID = dict(zip(PROBLEM_IDS, PROBLEM_TYPE_ORDER, strict=True))
PROBLEM_REFS = [
    ProblemRef(task_name, problem_id)
    for task_name in TASK_NAMES
    for problem_id in PROBLEM_IDS
]
