from typing import List, Tuple
from src.proceso import Proceso  # Importación corregida
from src.scheduler import Scheduler, GanttEntry

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