import streamlit as st
import random

# 1. CONFIGURACIÓN Y ESTILOS
st.set_page_config(page_title="Simulador Naranjitos", page_icon="🐂", layout="centered")

def aplicar_estilos_botones(colores):
    # Usamos selectores para los botones dentro del contenedor de opciones
    estilo = f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-of-type(1) button {{ background-color: {colores[0]} !important; color: white !important; border: none !important; }}
        div[data-testid="stVerticalBlock"] > div:nth-of-type(2) button {{ background-color: {colores[1]} !important; color: white !important; border: none !important; }}
        div[data-testid="stVerticalBlock"] > div:nth-of-type(3) button {{ background-color: {colores[2]} !important; color: white !important; border: none !important; }}
        </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)

# 2. CARGA DE DATOS (Sin caché para actualización inmediata)
def cargar_preguntas():
    lista = []
    try:
        with open("preguntas.txt", "r", encoding="utf-8") as f:
            for l in f:
                d = l.strip().split("|")
                if len(d) == 5:
                    lista.append({
                        "p": d[0], 
                        "o": [d[1], d[2], d[3]], 
                        "c": d[4].strip().lower()
                    })
    except Exception:
        pass
    return lista

banco = cargar_preguntas()

# 3. GESTIÓN DEL ESTADO
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': 'menu',
        'sesion': [],
        'indice': 0,
        'respuestas_usuario': {}  # Guarda {indice: letra_elegida}
    })

# 4. FUNCIONES DE LÓGICA
def empezar_test(cantidad):
    limite = max(1, min(len(banco), cantidad))
    st.session_state.update({
        'sesion': random.sample(banco, limite),
        'indice': 0,
        'respuestas_usuario': {},
        'estado': 'jugando'
    })

def registrar_respuesta(letra):
    st.session_state.respuestas_usuario[st.session_state.indice] = letra

def mover(paso):
    st.session_state.indice += paso

def finalizar():
    st.session_state.estado = 'resultado'

# 5. INTERFAZ DE USUARIO
if st.session_state.estado == 'menu':
    st.title("🐂 Simulador Naranjitos")
    st.write(f"Preguntas cargadas: {len(banco)}")
    
    cantidad = st.number_input("¿Cuántas preguntas quieres hacer?", 
                               min_value=1, 
                               max_value=len(banco), 
                               value=min(100, len(banco)))
    
    st.button("Empezar Test", use_container_width=True, type="primary", on_click=empezar_test, args=(cantidad,))

elif st.session_state.estado == 'jugando':
    idx = st.session_state.indice
    p_actual = st.session_state.sesion[idx]
    correcta = p_actual['c']
    total_preg = len(st.session_state.sesion)
    
    # Progreso
    st.caption(f"Pregunta {idx + 1} de {total_preg}")
    st.progress((idx + 1) / total_preg)
    st.markdown(f"### {p_actual['p']}")
    
    # Lógica de Colores
    colores = ["#333", "#333", "#333"]
    ya_respondida = idx in st.session_state.respuestas_usuario
    
    if ya_respondida:
        elegida = st.session_state.respuestas_usuario[idx]
        idx_map = {'a': 0, 'b': 1, 'c': 2}
        colores[idx_map[correcta]] = "#2ecc71"  # Verde la correcta
        if elegida
