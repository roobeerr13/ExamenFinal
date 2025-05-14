import pytest
from src.proceso import Proceso
from src.metrics import Metrics

def test_calcular_metricas():
    procesos = [
        Proceso("P1", 3, 1, tiempo_llegada=0, tiempo_inicio=0, tiempo_fin=3),
        Proceso("P2", 2, 2, tiempo_llegada=0, tiempo_inicio=3, tiempo_fin=5)
    ]
    gantt = [("P1", 0, 3), ("P2", 3, 5)]
    metricas = Metrics.calcular_metricas(procesos, gantt)
    assert metricas["respuesta_promedio"] == 1.5
    assert metricas["retorno_promedio"] == 4
    assert metricas["espera_promedio"] == 1.5