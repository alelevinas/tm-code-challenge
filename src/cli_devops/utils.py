from typing import List, NamedTuple, Dict
from enum import Enum

CONFIG = {}


class Status(Enum):
    HEALTHY = "Healthy"
    UNHEALTHY = "Unhealthy"

    def __str__(self) -> str:
        return self.value


class ServerStatus(NamedTuple):
    ip: str
    service: str
    status: Status
    cpu: float
    mem: float


class ServiceStatus(NamedTuple):
    service: str
    status: Status
    avg_cpu: float
    avg_mem: float


def resolve_status(cpu: int, memory: int) -> Status:
    if cpu > CONFIG['CPU_THRESHOLD'] or memory > CONFIG['MEM_THRESHOLD']:
        return Status.UNHEALTHY
    return Status.HEALTHY
