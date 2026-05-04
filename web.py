import streamlit as st
import random

# Configuración de página para móvil
st.set_page_config(page_title="Simulador San Fermín", page_icon="🐂", layout="centered")

# CSS para los colores de los botones
def aplicar_estilos_botones(colores):
    estilo = f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-of-type(4) button {{ background-color: {colores[0]} !important; color: white !important; }}
        div[data-testid="stVerticalBlock"] > div:nth-of-type(5) button {{ background-color: {colores[1]} !important; color: white !important; }}
        div[data-testid="stVerticalBlock"] > div:nth-of-type(6) button {{ background-color: {colores[2]} !important; color: white !important; }}
        </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)

@st.cache_data
def cargar_preguntas():
    lista = []
    try:
        with open("preguntas.txt", "r", encoding="utf-8") as f:
            for l in f:
                d = l.strip().split("|")
                if len(d) == 5:
                    # Guardamos la respuesta limpia de espacios
                    lista.append({
                        "p": d[0], 
                        "o": [d[1], d[2], d[3]], 
                        "c": d[4].strip().lower() 
                    })
    except: pass
    return lista

banco = cargar_preguntas()

# Estado de la sesión
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': 'menu', 'sesion': [], 'indice': 0, 
        'aciertos': 0, 'respondida': False, 'eleccion': None, 'mensaje': ("", "")
    })

# --- CALLBACKS ---
def empezar_test(cantidad):
    limite = max(1, min(len(banco), cantidad))
    st.session_state.update({
        'sesion': random.sample(banco, limite),
        'indice': 0, 'aciertos': 0, 'respondida': False, 'estado': 'jugando'
    })

def procesar_respuesta(letra, correcta):
    st.session_state.respondida = True
    st.session_state.eleccion = letra
    if letra == correcta:
        st.session_state.aciertos += 1
        st.session_state.mensaje = ("✅ ¡Acertaste!", "success")
    else:
        st.session_state.mensaje = (f"❌ Fallaste. La correcta era la {correcta.upper()}", "error")

def pasar_siguiente():
    st.session_state.update({'respondida': False, 'eleccion': None})
    st.session_state.indice += 1
    if st.session_state.indice >= len(st.session_state.sesion):
        st.session_state.estado = 'resultado'

# --- PANTALLAS ---
if st.session_state.estado == 'menu':
    st.title("🐂 Simulador Naranjitos")
    st.write(f"Preguntas disponibles: {len(banco)}")
    cantidad = st.number_input("¿Cuántas preguntas?", 1, len(banco), 30)
    st.button("Empezar Test", use_container_width=True, type="primary", on_click=empezar_test, args=(cantidad,))

elif st.session_state.estado == 'jugando':
    p_actual = st.session_state.sesion[st.session_state.indice]
    correcta = p_actual['c']
    
    st.caption(f"Pregunta {st.session_state.indice + 1} de {len(st.session_state.sesion)} | Aciertos: {st.session_state.aciertos}")
    st.markdown(f"### {p_actual['p']}")
    
    colores = ["#333", "#333", "#333"]
    if st.session_state.respondida:
        idx_map = {'a': 0, 'b': 1, 'c': 2}
        colores[idx_map[correcta]] = "#2ecc71" # Verde la correcta
        if st.session_state.eleccion != correcta:
            colores[idx_map[st.session_state.eleccion]] = "#e74c3c" # Rojo la elegida mal
            
    aplicar_estilos_botones(colores)

    st.button(p_actual["o"][0], use_container_width=True, on_click=procesar_respuesta, args=('a', correcta), disabled=st.session_state.respondida)
    st.button(p_actual["o"][1], use_container_width=True, on_click=procesar_respuesta, args=('b', correcta), disabled=st.session_state.respondida)
    st.button(p_actual["o"][2], use_container_width=True, on_click=procesar_respuesta, args=('c', correcta), disabled=st.session_state.respondida)

    if st.session_state.respondida:
        msg, tipo = st.session_state.mensaje
        
        # Forma correcta y segura de mostrar mensajes en Streamlit
        if tipo == "success":
            st.success(msg)
        else:
            st.error(msg)
            
        st.button("Siguiente Pregunta ➡️", use_container_width=True, type="primary", on_click=pasar_siguiente)

elif st.session_state.estado == 'resultado':
    st.title("🎉 Resultados")
    total = len(st.session_state.sesion)
    nota = (st.session_state.aciertos / total) * 10
    st.metric("Nota Final", f"{nota:.1f} / 10", f"{st.session_state.aciertos} aciertos")
    st.button("Volver al Inicio", use_container_width=True, on_click=lambda: st.session_state.update({'estado': 'menu'}))