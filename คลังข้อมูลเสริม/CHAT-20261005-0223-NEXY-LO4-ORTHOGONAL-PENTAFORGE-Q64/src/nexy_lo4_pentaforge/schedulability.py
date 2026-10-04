from __future__ import annotations

from dataclasses import dataclass

from .q64 import Q64


@dataclass(frozen=True)
class RealtimeTask:
    task_id: str
    priority: int
    period: Q64
    wcet: Q64
    deadline: Q64


@dataclass(frozen=True)
class TaskResponseReport:
    task_id: str
    response_time: Q64
    deadline: Q64
    schedulable: bool
    iterations: int


@dataclass(frozen=True)
class SchedulabilityReport:
    schedulable: bool
    task_reports: tuple[TaskResponseReport, ...]
    utilization: Q64
    reasons: tuple[str, ...]


def analyze_fixed_priority(tasks: tuple[RealtimeTask, ...], max_iterations: int = 256) -> SchedulabilityReport:
    if not tasks:
        raise ValueError("at least one task is required")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations <= 0:
        raise ValueError("max_iterations must be a positive int")
    ids = [task.task_id for task in tasks]
    if any(not task_id for task_id in ids) or len(set(ids)) != len(ids):
        raise ValueError("task ids must be non-empty and unique")
    priorities = [task.priority for task in tasks]
    if any(isinstance(priority, bool) or not isinstance(priority, int) for priority in priorities):
        raise TypeError("priority must be int")
    if len(set(priorities)) != len(priorities):
        raise ValueError("priorities must be unique")
    zero = Q64.zero()
    for task in tasks:
        if task.period <= zero or task.wcet < zero or task.deadline <= zero:
            raise ValueError("period/deadline must be positive and wcet nonnegative")
    ordered = tuple(sorted(tasks, key=lambda item: (item.priority, item.task_id)))
    utilization = Q64.zero()
    for task in ordered:
        utilization = utilization + (task.wcet / task.period)
    reports: list[TaskResponseReport] = []
    reasons: list[str] = []
    for index, task in enumerate(ordered):
        higher = ordered[:index]
        response = task.wcet
        iteration = 0
        schedulable = True
        failure_reason: str | None = None
        while True:
            iteration += 1
            interference = Q64.zero()
            for hp in higher:
                jobs = response.ceil_ratio_positive(hp.period)
                interference = interference + (hp.wcet * Q64.from_int(jobs))
            next_response = task.wcet + interference
            if next_response == response:
                break
            response = next_response
            if response > task.deadline:
                schedulable = False
                failure_reason = "DEADLINE_MISS"
                break
            if iteration >= max_iterations:
                schedulable = False
                failure_reason = "ITERATION_LIMIT"
                break
        if response > task.deadline:
            schedulable = False
            failure_reason = "DEADLINE_MISS"
        if failure_reason is not None:
            reasons.append(f"{task.task_id}:{failure_reason}")
        reports.append(
            TaskResponseReport(
                task_id=task.task_id,
                response_time=response,
                deadline=task.deadline,
                schedulable=schedulable,
                iterations=iteration,
            )
        )
    return SchedulabilityReport(
        schedulable=all(report.schedulable for report in reports),
        task_reports=tuple(reports),
        utilization=utilization,
        reasons=tuple(sorted(set(reasons))),
    )
