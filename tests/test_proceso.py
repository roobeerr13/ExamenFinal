import pytest
from src.proceso import Proceso

def test_crear_proceso_valido():
    p = Proceso("P1", 5, 1)
    assert p.pid == "P1"
    assert p.duracion == 5
    assert p.prioridad == 1
    assert p.tiempo_restante == 5

def test_pid_invalido():
    with pytest.raises(ValueError):
        Proceso("", 5, 1)

def test_duracion_invalida():
    with pytest.raises(ValueError):
        Proceso("P1", 0, 1)