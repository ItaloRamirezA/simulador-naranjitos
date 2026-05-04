import customtkinter as ctk
import random

# Configuración visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppSimulador(ctk.CTk):
    def __init__(self, preguntas):
        super().__init__()
        self.title("Simulador Naranjitos - San Fermín")
        self.geometry("600x650")
        self.banco = preguntas
        self.mostrar_menu_inicio()

    def limpiar_pantalla(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_menu_inicio(self):
        self.limpiar_pantalla()
        
        ctk.CTkLabel(self, text="SIMULADOR OFICIAL", font=("Arial", 28, "bold")).pack(pady=(50, 10))
        ctk.CTkLabel(self, text="Auxiliares Protección Civil", font=("Arial", 16)).pack(pady=(0, 40))

        ctk.CTkLabel(self, text="¿Cuántas preguntas quieres hacer?", font=("Arial", 14)).pack(pady=5)
        
        self.entry_cantidad = ctk.CTkEntry(self, width=120, placeholder_text="Ej: 30")
        self.entry_cantidad.insert(0, "30")
        self.entry_cantidad.pack(pady=10)

        btn_personalizado = ctk.CTkButton(self, text="Empezar Test Personalizado", 
                                         command=self.preparar_test_personalizado, 
                                         width=300, height=50)
        btn_personalizado.pack(pady=10)

        btn_rapido = ctk.CTkButton(self, text="Modo Rápido (30 preguntas)", 
                                   command=lambda: self.inicializar_test(30), 
                                   fg_color="#1f538d", hover_color="#2666ad",
                                   width=300, height=50)
        btn_rapido.pack(pady=10)

        ctk.CTkLabel(self, text=f"Total disponible: {len(self.banco)} preguntas", font=("Arial", 11), text_color="gray").pack(pady=20)

    def preparar_test_personalizado(self):
        try:
            val = self.entry_cantidad.get().strip()
            cantidad = int(val) if val else 30
            self.inicializar_test(cantidad)
        except ValueError:
            self.inicializar_test(30)

    def inicializar_test(self, cantidad):
        self.limpiar_pantalla()
        
        # Ajuste dinámico de cantidad
        limite = max(1, min(len(self.banco), cantidad))
        
        self.indice = 0
        self.aciertos = 0
        self.sesion = random.sample(self.banco, limite)
        
        self.label_puntos = ctk.CTkLabel(self, text=f"Pregunta 1/{len(self.sesion)}")
        self.label_puntos.pack(pady=10)

        self.label_pregunta = ctk.CTkLabel(self, text="", font=("Arial", 18, "bold"), wraplength=500)
        self.label_pregunta.pack(pady=30)

        self.btn_a = ctk.CTkButton(self, text="", command=lambda: self.validar("a"), width=450, height=55, fg_color="#333")
        self.btn_a.pack(pady=8)
        self.btn_b = ctk.CTkButton(self, text="", command=lambda: self.validar("b"), width=450, height=55, fg_color="#333")
        self.btn_b.pack(pady=8)
        self.btn_c = ctk.CTkButton(self, text="", command=lambda: self.validar("c"), width=450, height=55, fg_color="#333")
        self.btn_c.pack(pady=8)

        self.label_res = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.label_res.pack(pady=15)

        self.btn_next = ctk.CTkButton(self, text="Siguiente", command=self.cargar_sig, state="disabled")
        self.btn_next.pack(pady=10)

        self.actualizar_pregunta()

    def actualizar_pregunta(self):
        self.btn_next.configure(state="disabled", fg_color="gray")
        self.label_res.configure(text="")
        for b in [self.btn_a, self.btn_b, self.btn_c]:
            b.configure(fg_color="#333", state="normal")

        p = self.sesion[self.indice]
        self.label_pregunta.configure(text=p["p"])
        self.btn_a.configure(text=p["o"][0])
        self.btn_b.configure(text=p["o"][1])
        self.btn_c.configure(text=p["o"][2])
        self.label_puntos.configure(text=f"Pregunta {self.indice + 1}/{len(self.sesion)}")

    def validar(self, r):
        # Limpieza extrema de la respuesta para evitar fallos por formato
        correcta = str(self.sesion[self.indice]["c"]).lower().strip()
        r_usuario = str(r).lower().strip()
        
        for b in [self.btn_a, self.btn_b, self.btn_c]: b.configure(state="disabled")

        if r_usuario == correcta:
            self.aciertos += 1
            self.get_btn(r_usuario).configure(fg_color="#2ecc71")
            self.label_res.configure(text="✅ ¡Correcto!", text_color="#2ecc71")
        else:
            self.get_btn(r_usuario).configure(fg_color="#e74c3c")
            self.get_btn(correcta).configure(fg_color="#2ecc71")
            self.label_res.configure(text=f"❌ Error. Era la {correcta.upper()}", text_color="#e74c3c")
        
        self.btn_next.configure(state="normal", fg_color="#1f538d")

    def get_btn(self, letra):
        return {"a": self.btn_a, "b": self.btn_b, "c": self.btn_c}.get(letra, self.btn_a)

    def cargar_sig(self):
        self.indice += 1
        if self.indice < len(self.sesion):
            self.actualizar_pregunta()
        else:
            self.mostrar_pantalla_final()

    def mostrar_pantalla_final(self):
        self.limpiar_pantalla()
        total_preguntas = len(self.sesion)
        
        # Evitar error de división si la lista estuviera vacía
        nota = (self.aciertos / total_preguntas) * 10 if total_preguntas > 0 else 0
        
        ctk.CTkLabel(self, text="Test Finalizado", font=("Arial", 26, "bold")).pack(pady=40)
        ctk.CTkLabel(self, text=f"Puntuación: {self.aciertos}/{total_preguntas}", font=("Arial", 20)).pack(pady=10)
        ctk.CTkLabel(self, text=f"Nota Final: {nota:.1f}/10", font=("Arial", 22), text_color="#3498db").pack(pady=10)

        ctk.CTkButton(self, text="Volver al Menú Inicio", command=self.mostrar_menu_inicio, width=300, height=60, fg_color="#27ae60", hover_color="#2ecc71").pack(pady=30)
        ctk.CTkButton(self, text="Salir del Programa", command=self.quit, width=300, height=60, fg_color="#c0392b", hover_color="#e74c3c").pack(pady=10)

def cargar():
    lista = []
    try:
        with open("preguntas.txt", "r", encoding="utf-8") as f:
            for l in f:
                d = l.strip().split("|")
                if len(d) == 5:
                    # Limpiamos la respuesta correcta desde la carga
                    lista.append({
                        "p": d[0], 
                        "o": [d[1], d[2], d[3]], 
                        "c": d[4].strip().lower()
                    })
    except Exception as e:
        print(f"Error al cargar archivo: {e}")
    return lista

if __name__ == "__main__":
    datos = cargar()
    if datos:
        app = AppSimulador(datos)
        app.mainloop()
    else:
        print("Error: No se encontró preguntas.txt o está vacío.")