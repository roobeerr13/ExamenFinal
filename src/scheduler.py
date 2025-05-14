from abc import ABC, abstractmethod
from typing import List, Tuple
from src.proceso import Proceso

GanttEntry = Tuple[str, int, int]

class Scheduler(ABC):
    @abstractmethod
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        pass

class FCFSScheduler(Scheduler):
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        gantt = []
        tiempo_actual = 0
        for proceso in procesos:
            proceso.tiempo_inicio = tiempo_actual
            proceso.tiempo_fin = tiempo_actual + proceso.duracion
            gantt.append((proceso.pid, proceso.tiempo_inicio, proceso.tiempo_fin))
            tiempo_actual = proceso.tiempo_fin
            proceso.tiempo_restante = 0
        return gantt

class RoundRobinScheduler(Scheduler):
    def __init__(self, quantum: int):
        if quantum <= 0:
            raise ValueError("Quantum debe ser positivo")
        self.quantum = quantum

    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        gantt = []
        tiempo_actual = 0
        cola = [(p, p.duracion) for p in procesos]
        for p in procesos:
            p.tiempo_restante = p.duracion

        while cola:
            proceso, duracion_original = cola.pop(0)
            if proceso.tiempo_inicio is None:
                proceso.tiempo_inicio = tiempo_actual
            tiempo_ejecucion = min(self.quantum, proceso.tiempo_restante)
            inicio = tiempo_actual
            tiempo_actual += tiempo_ejecucion
            proceso.tiempo_restante -= tiempo_ejecucion
            gantt.append((proceso.pid, inicio, tiempo_actual))
            if proceso.tiempo_restante > 0:
                cola.append((proceso, duracion_original))
            else:
                proceso.tiempo_fin = tiempo_actual
        return gantt