import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# Definir las preguntas para cada tema
preguntas = {
    "matematicas": [
        ("¿Cuánto es 2 + 2?", "4"),
        ("¿Cuánto es 5 * 6?", "30"),
        ("¿Cuánto es 12 / 4?", "3"),
        ("¿cual es la raiz cuadrada de 54?"),
        ("¿cuanto es 23 - 10"),
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
        self.opcion_seleccionada = tk.StringVar()  # Variable para almacenar la opción seleccionada

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.radio_var = tk.StringVar(value="matematicas")
        for tema in preguntas.keys():
            radio_btn = tk.Radiobutton(self.frame, text=tema.capitalize(), variable=self.radio_var, value=tema, command=self.cambiar_tema)
            radio_btn.pack(side=tk.LEFT)

        self.botones_frame = tk.Frame(self.root)
        self.botones_frame.pack()

        self.botones = [tk.Button(self.botones_frame, text="", font=("Arial", 24), width=5, height=2, command=lambda i=i: self.hacer_movimiento(i)) for i in range(9)]
        for i, btn in enumerate(self.botones):
            btn.grid(row=i // 3, column=i % 3)

        # Frame para mostrar las preguntas con opciones
        self.opciones_frame = tk.Frame(self.root)
        self.opciones_frame.pack()

    def cambiar_tema(self):
        self.tema_actual = self.radio_var.get()
        self.intentos = 0

    def siguiente_pregunta(self):
        if self.intentos < 3:
            if self.tema_actual == "matematicas":
                self.mostrar_pregunta_matematicas()
            else:
                self.mostrar_pregunta_con_opciones()
        else:
            messagebox.showinfo("Fin de intentos", "Has fallado las tres preguntas. Cambiando de tema.")
            self.intentos = 0  # Resetear los intentos
            self.tema_actual = None  # Forzar al usuario a cambiar de tema
            # Reseteamos las preguntas para que el usuario elija un nuevo tema
            self.resetear_pregunta()

    def resetear_pregunta(self):
        self.tema_actual = self.radio_var.get()  # Volvemos a pedir el tema actual
        self.intentos = 0

    def mostrar_pregunta_matematicas(self):
        pregunta, respuesta_correcta = random.choice(preguntas["matematicas"])
        respuesta_usuario = simpledialog.askstring("Pregunta", pregunta)
        
        if respuesta_usuario is None:  # Si el usuario cancela
            messagebox.showinfo("Cancelado", "Has cancelado la pregunta.")
            return  # Salimos de la función sin penalizar
        
        if respuesta_usuario.strip() == respuesta_correcta:
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
            self.intentos = 0
        else:
            self.intentos += 1
            messagebox.showinfo("Incorrecto", f"Respuesta incorrecta. Tienes {3 - self.intentos} intentos restantes.")
            self.siguiente_pregunta()

    def mostrar_pregunta_con_opciones(self):
        # Limpiamos el frame de opciones
        for widget in self.opciones_frame.winfo_children():
            widget.destroy()

        # Seleccionar una pregunta del tema
        pregunta, opciones, respuesta_correcta = random.choice(preguntas[self.tema_actual])
        self.opcion_seleccionada.set(None)  # Limpiar selección previa

        # Mostrar la pregunta
        label_pregunta = tk.Label(self.opciones_frame, text=pregunta)
        label_pregunta.pack()

        # Crear los radio buttons para las opciones
        for opcion in opciones:
            radio_btn = tk.Radiobutton(self.opciones_frame, text=opcion, variable=self.opcion_seleccionada, value=opcion)
            radio_btn.pack()

        # Botón para enviar la respuesta
        btn_responder = tk.Button(self.opciones_frame, text="Responder", command=lambda: self.verificar_respuesta_opciones(respuesta_correcta))
        btn_responder.pack()

    def verificar_respuesta_opciones(self, respuesta_correcta):
        respuesta_usuario = self.opcion_seleccionada.get()

        if respuesta_usuario == "":
            messagebox.showinfo("Error", "Debes seleccionar una opción.")
            return

        if respuesta_usuario == respuesta_correcta:
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
            self.limpiar_pregunta()  # Limpiar la pregunta después de una respuesta correcta
            self.intentos = 0
        else:
            self.intentos += 1
            messagebox.showinfo("Incorrecto", f"Respuesta incorrecta. Tienes {3 - self.intentos} intentos restantes.")
            self.siguiente_pregunta()

    def limpiar_pregunta(self):
        # Limpiar las preguntas y opciones del frame
        for widget in self.opciones_frame.winfo_children():
            widget.destroy()

    def hacer_movimiento(self, index):
        if self.tablero[index] == "" and self.tema_actual:
            self.tablero[index] = self.turno
            self.botones[index].config(text=self.turno)
            if self.verificar_ganador(self.turno):
                messagebox.showinfo("Ganador", f"¡{self.turno} ha ganado!")
                self.resetear_tablero()
            elif "" not in self.tablero:
                messagebox.showinfo("Empate", "¡Es un empate!")
                self.resetear_tablero()
            else:
                # Hacer la pregunta automáticamente tras el movimiento
                self.siguiente_pregunta()
                self.turno = "O" if self.turno == "X" else "X"

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
        self.resetear_pregunta()

# Ejecutar el juego
if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoTotito(root)
    root.mainloop()

