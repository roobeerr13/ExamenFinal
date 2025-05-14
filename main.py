import gradio as gr
from src.proceso import Proceso  # Importación corregida
from src.repositorio import RepositorioProcesos
from src.fcfs_scheduler import FCFSScheduler
from src.round_robin_scheduler import RoundRobinScheduler
from src.metrics import Metrics
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Inicializar el repositorio
repo = RepositorioProcesos()

def agregar_proceso(pid, duracion, prioridad):
    try:
        proceso = proceso(pid, int(duracion), int(prioridad))
        repo.agregar_proceso(proceso)
        return "Proceso agregado exitosamente."
    except ValueError as e:
        return f"Error: {e}"

def listar_procesos():
    procesos = repo.listar_procesos()
    if not procesos:
        return "No hay procesos registrados."
    data = [[p.pid, p.duracion, p.prioridad, p.tiempo_llegada] for p in procesos]
    df = pd.DataFrame(data, columns=["PID", "Duración", "Prioridad", "Tiempo de Llegada"])
    return df

def eliminar_proceso(pid):
    if repo.obtener_proceso(pid):
        repo.eliminar_proceso(pid)
        return f"Proceso {pid} eliminado."
    return f"Error: No se encontró el proceso con PID {pid}."

def guardar_json():
    repo.guardar_json("data/procesos.json")
    return "Procesos guardados en JSON."

def cargar_json():
    repo.cargar_json("data/procesos.json")
    return "Procesos cargados desde JSON."

def guardar_csv():
    repo.guardar_csv("data/procesos.csv")
    return "Procesos guardados en CSV."

def cargar_csv():
    repo.cargar_csv("data/procesos.csv")
    return "Procesos cargados desde CSV."

def planificar_fcfs():
    procesos = repo.listar_procesos()
    if not procesos:
        return "No hay procesos para planificar.", None
    scheduler = FCFSScheduler()
    gantt = scheduler.planificar(procesos)
    metricas = Metrics.calcular_metricas(procesos, gantt)
    return format_resultados(metricas), generar_gantt(gantt)

def planificar_round_robin(quantum):
    try:
        quantum = int(quantum)
        procesos = repo.listar_procesos()
        if not procesos:
            return "No hay procesos para planificar.", None
        scheduler = RoundRobinScheduler(quantum)
        gantt = scheduler.planificar(procesos)
        metricas = Metrics.calcular_metricas(procesos, gantt)
        return format_resultados(metricas), generar_gantt(gantt)
    except ValueError as e:
        return f"Error: {e}", None

def format_resultados(metricas):
    return (
        f"Diagrama de Gantt: {metricas['gantt']}\n"
        f"Respuesta promedio: {metricas['respuesta_promedio']:.2f}\n"
        f"Retorno promedio: {metricas['retorno_promedio']:.2f}\n"
        f"Espera promedio: {metricas['espera_promedio']:.2f}"
    )

def generar_gantt(gantt):
    if not gantt:
        return None
    fig, ax = plt.subplots(figsize=(10, 4))
    y = 0
    for pid, inicio, fin in gantt:
        ax.broken_barh([(inicio, fin - inicio)], (y - 0.4, 0.8), facecolors='skyblue')
        ax.text(inicio + (fin - inicio) / 2, y, pid, ha='center', va='center')
        y += 1
    ax.set_ylim(-0.5, len(gantt) - 0.5)
    ax.set_xlim(0, max(fin for _, _, fin in gantt))
    ax.set_yticks(range(len(gantt)))
    ax.set_yticklabels([f"Tramo {i+1}" for i in range(len(gantt))])
    ax.set_xlabel("Tiempo")
    ax.set_title("Diagrama de Gantt")
    
    # Convertir la figura a una imagen
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return f'<img src="data:image/png;base64,{img_str}"/>'

# Crear la interfaz Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Simulador de Planificación de Procesos")
    
    with gr.Tabs():
        with gr.TabItem("Gestionar Procesos"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Agregar Proceso")
                    pid_input = gr.Textbox(label="PID")
                    duracion_input = gr.Number(label="Duración")
                    prioridad_input = gr.Number(label="Prioridad")
                    agregar_btn = gr.Button("Agregar Proceso")
                    agregar_output = gr.Textbox(label="Resultado")
                with gr.Column():
                    gr.Markdown("### Eliminar Proceso")
                    pid_eliminar_input = gr.Textbox(label="PID")
                    eliminar_btn = gr.Button("Eliminar Proceso")
                    eliminar_output = gr.Textbox(label="Resultado")
            gr.Markdown("### Lista de Procesos")
            listar_btn = gr.Button("Listar Procesos")
            procesos_output = gr.DataFrame(label="Procesos Registrados")
            
            agregar_btn.click(
                fn=agregar_proceso,
                inputs=[pid_input, duracion_input, prioridad_input],
                outputs=agregar_output
            )
            eliminar_btn.click(
                fn=eliminar_proceso,
                inputs=pid_eliminar_input,
                outputs=eliminar_output
            )
            listar_btn.click(
                fn=listar_procesos,
                outputs=procesos_output
            )
        
        with gr.TabItem("Persistencia"):
            with gr.Row():
                with gr.Column():
                    guardar_json_btn = gr.Button("Guardar JSON")
                    cargar_json_btn = gr.Button("Cargar JSON")
                    json_output = gr.Textbox(label="Resultado")
                with gr.Column():
                    guardar_csv_btn = gr.Button("Guardar CSV")
                    cargar_csv_btn = gr.Button("Cargar CSV")
                    csv_output = gr.Textbox(label="Resultado")
            
            guardar_json_btn.click(fn=guardar_json, outputs=json_output)
            cargar_json_btn.click(fn=cargar_json, outputs=json_output)
            guardar_csv_btn.click(fn=guardar_csv, outputs=csv_output)
            cargar_csv_btn.click(fn=cargar_csv, outputs=csv_output)
        
        with gr.TabItem("Planificación"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### FCFS")
                    fcfs_btn = gr.Button("Ejecutar FCFS")
                    fcfs_output = gr.Textbox(label="Resultados")
                    fcfs_gantt = gr.HTML(label="Diagrama de Gantt")
                with gr.Column():
                    gr.Markdown("### Round-Robin")
                    quantum_input = gr.Number(label="Quantum", value=2)
                    rr_btn = gr.Button("Ejecutar Round-Robin")
                    rr_output = gr.Textbox(label="Resultados")
                    rr_gantt = gr.HTML(label="Diagrama de Gantt")
            
            fcfs_btn.click(fn=planificar_fcfs, outputs=[fcfs_output, fcfs_gantt])
            rr_btn.click(
                fn=planificar_round_robin,
                inputs=quantum_input,
                outputs=[rr_output, rr_gantt]
            )

# Lanzar la interfaz
demo.launch()
