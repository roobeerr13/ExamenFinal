import pytest
import os
from src.proceso import Proceso
from src.repositorio import RepositorioProcesos

def test_agregar_proceso():
    repo = RepositorioProcesos()
    p = Proceso("P1", 5, 1)
    repo.agregar_proceso(p)
    assert len(repo.listar_procesos()) == 1

def test_pid_duplicado():
    repo = RepositorioProcesos()
    repo.agregar_proceso(Proceso("P1", 5, 1))
    with pytest.raises(ValueError):
        repo.agregar_proceso(Proceso("P1", 3, 2))

def test_guardar_cargar_json(tmp_path):
    repo = RepositorioProcesos()
    repo.agregar_proceso(Proceso("P1", 5, 1))
    archivo = tmp_path / "procesos.json"
    repo.guardar_json(archivo)
    repo_nuevo = RepositorioProcesos()
    repo_nuevo.cargar_json(archivo)
    assert len(repo_nuevo.listar_procesos()) == 1
    assert repo_nuevo.listar_procesos()[0].pid == "P1"

def test_guardar_cargar_csv(tmp_path):
    repo = RepositorioProcesos()
    repo.agregar_proceso(Proceso("P1", 5, 1))
    archivo = tmp_path / "procesos.csv"
    repo.guardar_csv(archivo)
    repo_nuevo = RepositorioProcesos()
    repo_nuevo.cargar_csv(archivo)
    assert len(repo_nuevo.listar_procesos()) == 1
    assert repo_nuevo.listar_procesos()[0].pid == "P1"