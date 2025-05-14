import pytest
from src.procesos import procesos
from src.fcfs_scheduler import FCFSScheduler
from src.round_robin_scheduler import RoundRobinScheduler

def test_fcfs_scheduler():
    procesos = [
        procesos("P1", 3, 1),
        procesos("P2", 2, 2)
    ]
    scheduler = FCFSScheduler()
    gantt = scheduler.planificar(procesos)
    assert gantt == [("P1", 0, 3), ("P2", 3, 5)]
    assert procesos[0].tiempo_fin == 3
    assert procesos[1].tiempo_fin == 5

def test_round_robin_scheduler():
    procesos = [
        procesos("P1", 4, 1),
        procesos("P2", 3, 2)
    ]
    scheduler = RoundRobinScheduler(quantum=2)
    gantt = scheduler.planificar(procesos)
    assert gantt == [("P1", 0, 2), ("P2", 2, 4), ("P1", 4, 6), ("P2", 6, 7)]
    assert procesos[0].tiempo_fin == 6
    assert procesos[1].tiempo_fin == 7