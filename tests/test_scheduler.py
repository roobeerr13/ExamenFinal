import pytest
from src.proceso import Proceso
from src.scheduler import FCFSScheduler, RoundRobinScheduler

def test_fcfs_scheduler():
    procesos = [
        Proceso("P1", 3, 1),
        Proceso("P2", 2, 2)
    ]
    scheduler = FCFSScheduler()
    gantt = scheduler.planificar(procesos)
    assert gantt == [("P1", 0, 3), ("P2", 3, 5)]
    assert procesos[0].tiempo_fin == 3
    assert procesos[1].tiempo_fin == 5

def test_round_robin_scheduler():
    procesos = [
        Proceso("P1", 4, 1),
        Proceso("P2", 3, 2)
    ]
    scheduler = RoundRobinScheduler(quantum=2)
    gantt = scheduler.planificar(procesos)
    assert gantt == [("P1", 0, 2), ("P2", 2, 4), ("P1", 4, 6), ("P2", 6, 7)]
    assert procesos[0].tiempo_fin == 6
    assert procesos[1].tiempo_fin == 7