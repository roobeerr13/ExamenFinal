import json
import csv
import os
from typing import List, Optional
from src.proceso import Proceso

class RepositorioProcesos:
    def __init__(self):
        self.procesos: List[Proceso] = []

    def agregar_proceso(self, proceso: Proceso) -> None:
        if any(p.pid == proceso.pid for p in self.procesos):
            raise ValueError(f"PID {proceso.pid} ya existe")
        self.procesos.append(proceso)

    def listar_procesos(self) -> List[Proceso]:
        return self.procesos

    def eliminar_proceso(self, pid: str) -> None:
        self.procesos = [p for p in self.procesos if p.pid != pid]

    def obtener_proceso(self, pid: str) -> Optional[Proceso]:
        for proceso in self.procesos:
            if proceso.pid == pid:
                return proceso
        return None

    def guardar_json(self, archivo: str) -> None:
        datos = [{
            "pid": p.pid,
            "duracion": p.duracion,
            "prioridad": p.prioridad,
            "tiempo_llegada": p.tiempo_llegada
        } for p in self.procesos]
        with open(archivo, 'w') as f:
            json.dump(datos, f, indent=4)

    def cargar_json(self, archivo: str) -> None:
        if not os.path.exists(archivo):
            self.procesos = []
            return
        with open(archivo, 'r') as f:
            datos = json.load(f)
        self.procesos = [Proceso(
            pid=d["pid"],
            duracion=d["duracion"],
            prioridad=d["prioridad"],
            tiempo_llegada=d["tiempo_llegada"]
        ) for d in datos]

    def guardar_csv(self, archivo: str) -> None:
        with open(archivo, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["pid", "duracion", "prioridad", "tiempo_llegada"])
            for p in self.procesos:
                writer.writerow([p.pid, p.duracion, p.prioridad, p.tiempo_llegada])

    def cargar_csv(self, archivo: str) -> None:
        if not os.path.exists(archivo):
            self.procesos = []
            return
        with open(archivo, 'r') as f:
            reader = csv.DictReader(f, delimiter=';')
            self.procesos = [Proceso(
                pid=row["pid"],
                duracion=int(row["duracion"]),
                prioridad=int(row["prioridad"]),
                tiempo_llegada=int(row["tiempo_llegada"])
            ) for row in reader]