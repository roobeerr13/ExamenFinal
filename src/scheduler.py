from abc import ABC, abstractmethod
from typing import List
from src.proceso import procesos

GanttEntry = tuple[str, int, int]

class Scheduler(ABC):
    @abstractmethod
    def planificar(self, procesos: List[procesos]) -> List[GanttEntry]:
        pass