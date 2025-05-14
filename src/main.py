from src.procesos import procesos
from src.repositorio import RepositorioProcesos
from src.fcfs_scheduler import FCFSScheduler
from src.round_robin_scheduler import RoundRobinScheduler
from src.metrics import Metrics

def main():
    repo = RepositorioProcesos()
    while True:
        print("\n1. Agregar proceso")
        print("2. Listar procesos")
        print("3. Eliminar proceso")
        print("4. Guardar (JSON)")
        print("5. Cargar (JSON)")
        print("6. Guardar (CSV)")
        print("7. Cargar (CSV)")
        print("8. Planificar (FCFS)")
        print("9. Planificar (Round-Robin)")
        print("10. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            pid = input("PID: ")
            duracion = int(input("Duración: "))
            prioridad = int(input("Prioridad: "))
            try:
                repo.agregar_proceso(procesos(pid, duracion, prioridad))
                print("Proceso agregado")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "2":
            for p in repo.listar_procesos():
                print(f"PID: {p.pid}, Duración: {p.duracion}, Prioridad: {p.prioridad}")

        elif opcion == "3":
            pid = input("PID a eliminar: ")
            repo.eliminar_proceso(pid)
            print("Proceso eliminado")

        elif opcion == "4":
            repo.guardar_json("data/procesos.json")
            print("Guardado en JSON")

        elif opcion == "5":
            repo.cargar_json("data/procesos.json")
            print("Cargado desde JSON")

        elif opcion == "6":
            repo.guardar_csv("data/procesos.csv")
            print("Guardado en CSV")

        elif opcion == "7":
            repo.cargar_csv("data/procesos.csv")
            print("Cargado desde CSV")

        elif opcion == "8":
            scheduler = FCFSScheduler()
            gantt = scheduler.planificar(repo.listar_procesos())
            metricas = Metrics.calcular_metricas(repo.listar_procesos(), gantt)
            print("Gantt:", metricas["gantt"])
            print(f"Respuesta promedio: {metricas['respuesta_promedio']}")
            print(f"Retorno promedio: {metricas['retorno_promedio']}")
            print(f"Espera promedio: {metricas['espera_promedio']}")

        elif opcion == "9":
            quantum = int(input("Quantum: "))
            scheduler = RoundRobinScheduler(quantum)
            gantt = scheduler.planificar(repo.listar_procesos())
            metricas = Metrics.calcular_metricas(repo.listar_procesos(), gantt)
            print("Gantt:", metricas["gantt"])
            print(f"Respuesta promedio: {metricas['respuesta_promedio']}")
            print(f"Retorno promedio: {metricas['retorno_promedio']}")
            print(f"Espera promedio: {metricas['espera_promedio']}")

        elif opcion == "10":
            break

if __name__ == "__main__":
    main()