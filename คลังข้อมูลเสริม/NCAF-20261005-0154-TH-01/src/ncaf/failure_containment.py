from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .common import ContractError, require_nonempty


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class Action(str, Enum):
    ATTEMPT = "ATTEMPT"
    BLOCK = "BLOCK"
    PROBE = "PROBE"


@dataclass(frozen=True)
class DependencyPolicy:
    failure_threshold: int = 3
    cooldown_ticks: int = 5

    def __post_init__(self) -> None:
        if self.failure_threshold <= 0 or self.cooldown_ticks <= 0:
            raise ContractError("failure_threshold and cooldown_ticks must be positive")


@dataclass
class _Circuit:
    state: CircuitState = CircuitState.CLOSED
    consecutive_failures: int = 0
    opened_at: int | None = None
    probe_in_flight: bool = False


class FailureContainmentEngine:
    """Per-dependency circuit breaker using logical ticks for deterministic tests and replay."""

    def __init__(self, policy: DependencyPolicy = DependencyPolicy()):
        self.policy = policy
        self._circuits: dict[str, _Circuit] = {}

    def _circuit(self, dependency: str) -> _Circuit:
        require_nonempty(dependency, "dependency")
        return self._circuits.setdefault(dependency, _Circuit())

    def before_call(self, dependency: str, *, tick: int) -> Action:
        if tick < 0:
            raise ContractError("tick must be non-negative")
        circuit = self._circuit(dependency)
        if circuit.state is CircuitState.CLOSED:
            return Action.ATTEMPT
        assert circuit.opened_at is not None
        if circuit.state is CircuitState.OPEN and tick - circuit.opened_at >= self.policy.cooldown_ticks:
            circuit.state = CircuitState.HALF_OPEN
            circuit.probe_in_flight = False
        if circuit.state is CircuitState.OPEN:
            return Action.BLOCK
        if circuit.probe_in_flight:
            return Action.BLOCK
        circuit.probe_in_flight = True
        return Action.PROBE

    def record_success(self, dependency: str) -> None:
        circuit = self._circuit(dependency)
        circuit.state = CircuitState.CLOSED
        circuit.consecutive_failures = 0
        circuit.opened_at = None
        circuit.probe_in_flight = False

    def record_failure(self, dependency: str, *, tick: int) -> None:
        if tick < 0:
            raise ContractError("tick must be non-negative")
        circuit = self._circuit(dependency)
        if circuit.state is CircuitState.HALF_OPEN:
            circuit.state = CircuitState.OPEN
            circuit.opened_at = tick
            circuit.probe_in_flight = False
            return
        circuit.consecutive_failures += 1
        if circuit.consecutive_failures >= self.policy.failure_threshold:
            circuit.state = CircuitState.OPEN
            circuit.opened_at = tick
            circuit.probe_in_flight = False

    def state(self, dependency: str) -> CircuitState:
        return self._circuit(dependency).state
