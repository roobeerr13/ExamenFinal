from typing import List
from src.proceso import Proceso
from src.scheduler import GanttEntry

class Metrics:
    @staticmethod
    def calcular_metricas(procesos: List[Proceso], gantt: List[GanttEntry]) -> dict:
        tiempos_respuesta = []
        tiempos_retorno = []
        tiempos_espera = []

        for proceso in procesos:
            tiempo_respuesta = proceso.tiempo_inicio - proceso.tiempo_llegada
            tiempo_retorno = proceso.tiempo_fin - proceso.tiempo_llegada
            tiempo_espera = tiempo_retorno - proceso.duracion

            tiempos_respuesta.append(tiempo_respuesta)
            tiempos_retorno.append(tiempo_retorno)
            tiempos_espera.append(tiempo_espera)

        n = len(procesos)
        return {
            "respuesta_promedio": sum(tiempos_respuesta) / n if n > 0 else 0,
            "retorno_promedio": sum(tiempos_retorno) / n if n > 0 else 0,
            "espera_promedio": sum(tiempos_espera) / n if n > 0 else 0,
            "gantt": gantt
        }