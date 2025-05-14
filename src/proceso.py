from dataclasses import dataclass
from typing import Optional

@dataclass
class Proceso:
    pid: str
    duracion: int
    prioridad: int
    tiempo_llegada: int = 0
    tiempo_restante: Optional[int] = None
    tiempo_inicio: Optional[int] = None
    tiempo_fin: Optional[int] = None

    def __post_init__(self):
        if not self.pid or not isinstance(self.pid, str):
            raise ValueError("PID debe ser una cadena no vacía")
        if not isinstance(self.duracion, int) or self.duracion <= 0:
            raise ValueError("Duración debe ser un entero positivo")
        if not isinstance(self.prioridad, int):
            raise ValueError("Prioridad debe ser un entero")
        self.tiempo_restante = self.duracion if self.tiempo_restante is None else self.tiempo_restante