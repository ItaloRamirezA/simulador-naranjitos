import streamlit as st
import random

st.set_page_config(page_title="Simulador Naranjitos", page_icon="🐂", layout="centered")

def aplicar_estilos_botones(colores):
    estilo = f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-of-type(4) button {{ background-color: {colores[0]} !important; color: white !important; }}
        div[data-testid="stVerticalBlock"] > div:nth-of-type(5) button {{ background-color: {colores[1]} !important; color: white !important; }}
        div[data-testid="stVerticalBlock"] > div:nth-of-type(6) button {{ background-color: {colores[2]} !important; color: white !important; }}
        </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)

def cargar_preguntas():
    lista = []
    try:
        with open("preguntas.txt", "r", encoding="utf-8") as f:
            for l in f:
                d = l.strip().split("|")
                if len(d) == 5:
                    lista.append({"p": d[0], "o": [d[1], d[2], d[3]], "c": d[4].strip().lower()})
    except: pass
    return lista

banco = cargar_preguntas()

# --- ESTADO DE SESIÓN ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': 'menu',
        'sesion': [],
        'indice': 0,
        'respuestas_usuario': {} # Guardamos {indice: letra_elegida}
    })

# --- FUNCIONES DE NAVEGACIÓN ---
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

# --- PANTALLAS ---
if st.session_state.estado == 'menu':
    st.title("🐂 Simulador Naranjitos")
    cantidad = st.number_input("¿Cuántas preguntas?", 1, len(banco), min(100, len(banco)))
    st.button("Empezar Test", use_container_width=True, type="primary", on_click=empezar_test, args=(cantidad,))

elif st.session_state.estado == 'jugando':
    idx = st.session_state.indice
    p_actual = st.session_state.sesion[idx]
    correcta = p_actual['c']
    total_preg = len(st.session_state.sesion)
    
    # Cabecera
    st.caption(f"Pregunta {idx + 1} de {total_preg}")
    st.progress((idx + 1) / total_preg)
    st.markdown(f"### {p_actual['p']}")
    
    # Lógica de colores (si ya fue respondida)
    colores = ["#333", "#333", "#333"]
    ya_respondida = idx in st.session_state.respuestas_usuario
    
    if ya_respondida:
        elegida = st.session_state.respuestas_usuario[idx]
        idx_map = {'a': 0, 'b': 1, 'c': 2}
        colores[idx_map[correcta]] = "#2ecc71" # Verde la correcta
        if elegida != correcta:
            colores[idx_map[elegida]] = "#e74c3c" # Rojo la elegida mal
            
    aplicar_estilos_botones(colores)

    # Botones de opciones
    st.button(p_actual["o"][0], use_container_width=True, on_click=registrar_respuesta, args=('a',), disabled=ya_respondida)
    st.button(p_actual["o"][1], use_container_width=True, on_click=registrar_respuesta, args=('b',), disabled=ya_respondida)
    st.button(p_actual["o"][2], use_container_width=True, on_click=registrar_respuesta, args=('c',), disabled=ya_respondida)

    if ya_respondida:
        if st.session_state.respuestas_usuario[idx] == correcta:
            st.success("✅ ¡Correcto!")
        else:
            st.error(f"❌ Incorrecto. La buena era la {correcta.upper()}")

    st.write("---")
    
    # Barra de Navegación inferior
    col_pre, col_next = st.columns(2)
    
    with col_pre:
        if idx > 0:
            st.button("⬅️ Anterior", use_container_width=True, on_click=mover, args=(-1,))
    
    with col_next:
        if idx < total_preg - 1:
            texto_sig = "Siguiente ➡️" if ya_respondida else "Saltar ➡️"
            st.button(texto_sig, use_container_width=True, on_click=mover, args=(1,))
        else:
            st.button("Finalizar Test 🏁", use_container_width=True, type="primary", on_click=finalizar)

elif st.session_state.estado == 'resultado':
    st.title("🎉 Resultados Finales")
    
    sesion = st.session_state.sesion
    respuestas = st.session_state.respuestas_usuario
    total = len(sesion)
    
    # Cálculo de puntos
    aciertos = 0
    fallos = 0
    no_respondidas = 0
    
    for i, p in enumerate(sesion):
        if i in respuestas:
            if respuestas[i] == p['c']:
                aciertos += 1
            else:
                fallos += 1
        else:
            no_respondidas += 1
            
    puntos_netos = aciertos - (fallos / 3)
    nota = (max(0, puntos_netos) / total) * 10
    
    st.metric("Nota Final", f"{nota:.2f} / 10")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Aciertos ✅", aciertos)
    c2.metric("Fallos ❌", fallos)
    c3.metric("En blanco ⚪", no_respondidas)
    
    st.info(f"Nota calculada sobre {total} preguntas. Los fallos restan 0.33, las blancas no restan.")
    
    if st.button("Reintentar mismo test", use_container_width=True):
        st.session_state.update({'indice': 0, 'respuestas_usuario': {}, 'estado': 'jugando'})
        st.rerun()
        
    if st.button("Volver al Menú Principal", use_container_width=True, type="primary"):
        st.session_state.estado = 'menu'
        st.rerun()
