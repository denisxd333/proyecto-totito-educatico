import tkinter as tk  
from tkinter import messagebox, simpledialog  
from collections import deque  
import random  

# Inicializar turnos de jugadores  
turno = deque(["Jugador 1", "Jugador 2"])  

# Crear el tablero 3x3 para "Totito"  
tablero = [["", "", ""], ["", "", ""], ["", "", ""]]  

# Preguntas de matemáticas simples  
preguntas_matematica = [  
    ("¿Cuánto es 2 + 2?", 4),  
    ("¿Cuánto es 3 + 5?", 8),  
    ("¿Cuánto es 10 - 4?", 6),  
    ("¿Cuánto es 6 / 2?", 3),  
    ("¿Cuánto es 4 * 2?", 8),  
    ("¿Cuánto es 9 * 5?", 45),  
]  

# Preguntas de lenguaje  
preguntas_lenguaje = [  
    ("¿Cuál es el opuesto de 'frío'?", "caliente","calor" "verano"),  
    ("¿Qué es un sinónimo de 'feliz'?", "contento","Alegre","Dichoso"),  
    ("¿Cuál es la capital de España?", "madrid"),  
    ("¿Qué palabra describe un lugar muy seco?", "árido"),  
    ("¿Cómo se llama el continente donde se encuentra Egipto?", "África"),  
    ("¿Quien era Sócrates?", "Un filósofo")  
]  


def rotar_turno():  
    turno.rotate()  
    return turno[0]  

def mostrar_tablero():  
    for fila in range(3):  
        for col in range(3):  
            boton_texto = tablero[fila][col]  
            botones[fila][col].config(text=boton_texto)  

def posicion_correcta(fila, columna):  
    return 0 <= fila <= 2 and 0 <= columna <= 2 and tablero[fila][columna] == ""  

def hacer_pregunta(pregunta, respuesta_correcta):  
    while True:  # Esto asegura que el jugador deba responder.  
        respuesta_usuario = simpledialog.askstring("Pregunta", pregunta)  
        if respuesta_usuario is None:  # Usuario cerró el diálogo  
            continue  
        if respuesta_usuario.strip().lower() == str(respuesta_correcta).lower():  
            return True  
        else:  
            messagebox.showinfo("Respuesta Incorrecta", "La respuesta es incorrecta. Intenta nuevamente.")  

def verificar_ganador():  
    for fila in tablero:  
        if fila[0] == fila[1] == fila[2] != "":  
            return fila[0]  

    for col in range(3):  
        if tablero[0][col] == tablero[1][col] == tablero[2][col] != "":  
            return tablero[0][col]  

    if tablero[0][0] == tablero[1][1] == tablero[2][2] != "":  
        return tablero[0][0]  

    if tablero[0][2] == tablero[1][1] == tablero[2][0] != "":  
        return tablero[0][2]  

    return None  

def boton_click(fila, col):  
    jugador = rotar_turno()  
    if posicion_correcta(fila, col):  
        tablero[fila][col] = "X" if jugador == "Jugador 1" else "O"  
        mostrar_tablero()  

        ganador = verificar_ganador()  
        if ganador:  
            messagebox.showinfo("Fin del Juego", f"¡{ganador} ha ganado el juego de Totito!")  
            reiniciar_juego()  
            return  

        # Pregunta de matemáticas con obligatoria respuesta.  
        if not gestionar_pregunta(jugador):  
            return  
        
        # Pregunta de lenguaje  
        if hacer_pregunta(*random.choice(preguntas_lenguaje)):  
            messagebox.showinfo("Respuesta Correcta", "¡Correcto! Puedes seguir jugando.")  
        else:  
            messagebox.showinfo("Fin del Juego", "Incorrecto. Has perdido. ¡Fin del juego!")  
            reiniciar_juego()  
            return  

        if all(cell != "" for row in tablero for cell in row):  
            messagebox.showinfo("Fin del Juego", "¡Es un empate!")  
            reiniciar_juego()  

def gestionar_pregunta(jugador):  
    if hacer_pregunta(*random.choice(preguntas_matematica)):  
        return True  
    else:  
        # Segunda oportunidad  
        messagebox.showinfo("Intento Fallido", "Pregunta incorrecta. ¡Tienes una segunda oportunidad!")  
        return hacer_pregunta(*random.choice(preguntas_matematica))  

def reiniciar_juego():  
    global tablero  
    tablero = [["", "", ""], ["", "", ""], ["", "", ""]]  
    mostrar_tablero()  
    for fila in botones:  
        for boton in fila:  
            boton.config(text="")  

# Configuración de la ventana principal  
root = tk.Tk()  
root.title("Juego de Totito")  

# Crear botones para el tablero  
botones = []  
for i in range(3):  
    fila = []  
    for j in range(3):  
        boton = tk.Button(root, text="", font=('Arial', 24), width=5, height=2,  
                          command=lambda fila=i, col=j: boton_click(fila, col))  
        boton.grid(row=i, column=j)  
        fila.append(boton)  
    botones.append(fila)  

root.mainloop()