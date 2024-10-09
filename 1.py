import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# Definir las preguntas para cada tema
preguntas = {
    "matematicas": [
        ("¿Cuánto es 2 + 2?", "4"),
        ("¿Cuánto es 5 * 6?", "30"),
        ("¿Cuánto es 12 / 4?", "3"),
        ("¿Cuál es la raíz cuadrada de 9?", "3"),
        ("¿Cuánto es 23 - 10?", "13"),
    ],
    "lenguaje": [
        ("¿Quién escribió 'Don Quijote de la Mancha'?", ["A. Cervantes", "B. Shakespeare", "C. Borges"], "A. Cervantes"),
        ("¿Qué es un adjetivo?", ["A. Palabra que describe un sustantivo", "B. Palabra que une oraciones", "C. Palabra que expresa acción"], "A. Palabra que describe un sustantivo"),
        ("¿Cuál es el sinónimo de 'feliz'?", ["A. Triste", "B. Contento", "C. Enojado"], "B. Contento"),
    ],
    "filosofia": [
        ("¿Quién es conocido como el padre de la filosofía?", ["A. Sócrates", "B. Platón", "C. Aristóteles"], "A. Sócrates"),
        ("¿Qué es el empirismo?", ["A. Conocimiento a través de la experiencia", "B. Conocimiento a través de la razón", "C. Conocimiento a través de la fe"], "A. Conocimiento a través de la experiencia"),
        ("¿Qué propone Descartes con 'Cogito, ergo sum'?", ["A. Pienso, luego existo", "B. Soy feliz, luego existo", "C. Vivo, luego pienso"], "A. Pienso, luego existo"),
    ],
}

class JuegoTotito:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego Educativo de Totito")

        self.tablero = [""] * 9
        self.turno = "X"
        self.tema_actual = None
        self.pregunta_actual = None
        self.intentos = 0
        self.opcion_seleccionada = tk.StringVar()
        self.casilla_seleccionada = None

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.radio_var = tk.StringVar(value="matematicas")
        for tema in preguntas.keys():
            radio_btn = tk.Radiobutton(self.frame, text=tema.capitalize(), variable=self.radio_var, value=tema, command=self.cambiar_tema)
            radio_btn.pack(side=tk.LEFT)

        self.botones_frame = tk.Frame(self.root)
        self.botones_frame.pack()

        self.botones = [tk.Button(self.botones_frame, text="", font=("Arial", 24), width=5, height=2, command=lambda i=i: self.seleccionar_casilla(i)) for i in range(9)]
        for i, btn in enumerate(self.botones):
            btn.grid(row=i // 3, column=i % 3)

        self.opciones_frame = tk.Frame(self.root)
        self.opciones_frame.pack()

    def cambiar_tema(self):
        self.tema_actual = self.radio_var.get()
        self.intentos = 0

    def seleccionar_casilla(self, index):
        if self.tablero[index] == "" and self.tema_actual:
            self.casilla_seleccionada = index
            self.siguiente_pregunta()

    def siguiente_pregunta(self):
        if self.intentos < 3:
            if self.tema_actual == "matematicas":
                self.mostrar_pregunta_matematicas()
            else:
                self.mostrar_pregunta_con_opciones()
        else:
            messagebox.showinfo("Fin de intentos", "Has fallado las tres preguntas. Cambiando de tema.")
            self.intentos = 0
            self.tema_actual = None
            self.casilla_seleccionada = None
            self.resetear_pregunta()

    def resetear_pregunta(self):
        self.tema_actual = self.radio_var.get()
        self.intentos = 0

    def mostrar_pregunta_matematicas(self):
        pregunta, respuesta_correcta = random.choice(preguntas["matematicas"])
        respuesta_usuario = simpledialog.askstring("Pregunta", pregunta)
        
        if respuesta_usuario is None:
            messagebox.showinfo("Cancelado", "Has cancelado la pregunta.")
            self.casilla_seleccionada = None
            return
        
        if respuesta_usuario.strip() == respuesta_correcta:
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
            self.hacer_movimiento(self.casilla_seleccionada)
        else:
            self.intentos += 1
            messagebox.showinfo("Incorrecto", f"Respuesta incorrecta. Tienes {3 - self.intentos} intentos restantes.")
            self.siguiente_pregunta()

    def mostrar_pregunta_con_opciones(self):
        for widget in self.opciones_frame.winfo_children():
            widget.destroy()

        pregunta, opciones, respuesta_correcta = random.choice(preguntas[self.tema_actual])
        self.opcion_seleccionada.set(None)

        label_pregunta = tk.Label(self.opciones_frame, text=pregunta)
        label_pregunta.pack()

        for opcion in opciones:
            radio_btn = tk.Radiobutton(self.opciones_frame, text=opcion, variable=self.opcion_seleccionada, value=opcion)
            radio_btn.pack()

        btn_responder = tk.Button(self.opciones_frame, text="Responder", command=lambda: self.verificar_respuesta_opciones(respuesta_correcta))
        btn_responder.pack()

    def verificar_respuesta_opciones(self, respuesta_correcta):
        respuesta_usuario = self.opcion_seleccionada.get()

        if respuesta_usuario == "":
            messagebox.showinfo("Error", "Debes seleccionar una opción.")
            return

        if respuesta_usuario == respuesta_correcta:
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
            self.limpiar_pregunta()
            self.hacer_movimiento(self.casilla_seleccionada)
        else:
            self.intentos += 1
            messagebox.showinfo("Incorrecto", f"Respuesta incorrecta. Tienes {3 - self.intentos} intentos restantes.")
            self.siguiente_pregunta()

    def limpiar_pregunta(self):
        for widget in self.opciones_frame.winfo_children():
            widget.destroy()

    def hacer_movimiento(self, index):
        self.tablero[index] = self.turno
        self.botones[index].config(text=self.turno)
        if self.verificar_ganador(self.turno):
            messagebox.showinfo("Ganador", f"¡{self.turno} ha ganado!")
            self.resetear_tablero()
        elif "" not in self.tablero:
            messagebox.showinfo("Empate", "¡Es un empate!")
            self.resetear_tablero()
        else:
            self.turno = "O" if self.turno == "X" else "X"
        self.casilla_seleccionada = None

    def verificar_ganador(self, jugador):
        combinaciones_ganadoras = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]
        return any(all(self.tablero[i] == jugador for i in combinacion) for combinacion in combinaciones_ganadoras)

    def resetear_tablero(self):
        self.tablero = [""] * 9
        for btn in self.botones:
            btn.config(text="")
        self.turno = "X"
        self.tema_actual = None
        self.intentos = 0
        self.casilla_seleccionada = None
        self.resetear_pregunta()

# Ejecutar el juego
if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoTotito(root)
    root.mainloop()
