import streamlit as st
import random

# 1. CONFIGURACIÓN Y ESTILOS
st.set_page_config(page_title="Simulador Naranjitos", page_icon="🐂", layout="centered")

def aplicar_estilos_botones(colores):
    estilo = f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-of-type(1) button {{ background-color: {colores[0]} !important; color: white !important; border: none !important; }}
        div[data-testid="stVerticalBlock"] > div:nth-of-type(2) button {{ background-color: {colores[1]} !important; color: white !important; border: none !important; }}
        div[data-testid="stVerticalBlock"] > div:nth-of-type(3) button {{ background-color: {colores[2]} !important; color: white !important; border: none !important; }}
        </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)

# 2. CARGA DE DATOS
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
        'respuestas_usuario': {}
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
    
    st.caption(f"Pregunta {idx + 1} de {total_preg}")
    st.progress((idx + 1) / total_preg)
    st.markdown(f"### {p_actual['p']}")
    
    colores = ["#333", "#333", "#333"]
    ya_respondida = idx in st.session_state.respuestas_usuario
    
    if ya_respondida:
        elegida = st.session_state.respuestas_usuario[idx]
        idx_map = {'a': 0, 'b': 1, 'c': 2}
        colores[idx_map[correcta]] = "#2ecc71"
        if elegida != correcta:
            colores[idx_map[elegida]] = "#e74c3c"
            
    aplicar_estilos_botones(colores)

    with st.container():
        st.button(p_actual["o"][0], key=f"a_{idx}", use_container_width=True, on_click=registrar_respuesta, args=('a',), disabled=ya_respondida)
        st.button(p_actual["o"][1], key=f"b_{idx}", use_container_width=True, on_click=registrar_respuesta, args=('b',), disabled=ya_respondida)
        st.button(p_actual["o"][2], key=f"c_{idx}", use_container_width=True, on_click=registrar_respuesta, args=('c',), disabled=ya_respondida)

    if ya_respondida:
        if st.session_state.respuestas_usuario[idx] == correcta:
            st.success("✅ ¡Correcto!")
        else:
            st.error(f"❌ Incorrecto. La respuesta era: {correcta.upper()}")

    st.write("---")
    
    col_izq, col_der = st.columns(2)
    with col_izq:
        if idx > 0:
            st.button("⬅️ Anterior", use_container_width=True, on_click=mover, args=(-1,))
    with col_der:
        if idx < total_preg - 1:
            texto_boton = "Siguiente ➡️" if ya_respondida else "Saltar ➡️"
            st.button(texto_boton, use_container_width=True, on_click=mover, args=(1,))
        else:
            st.button("Finalizar y Ver Nota 🏁", use_container_width=True, type="primary", on_click=finalizar)

elif st.session_state.estado == 'resultado':
    st.title("🎉 Resultados del Simulador")
    sesion = st.session_state.sesion
    respuestas = st.session_state.respuestas_usuario
    total = len(sesion)
    
    aciertos = sum(1 for i, p in enumerate(sesion) if i in respuestas and respuestas[i] == p['c'])
    fallos = sum(1 for i, p in enumerate(sesion) if i in respuestas and respuestas[i] != p['c'])
    blancas = total - (aciertos + fallos)
            
    puntos_netos = aciertos - (fallos / 3)
    nota_final = (max(0, puntos_netos) / total) * 10
    
    st.metric("Nota Final", f"{nota_final:.2f} / 10")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Aciertos", aciertos)
    c2.metric("Fallos", fallos)
    c3.metric("Blancas", blancas)
    
    st.info(f"Sistema: Acierto +1 | Fallo -0.33 | Blanca 0")
    
    if st.button("Repetir mismo examen", use_container_width=True):
        st.session_state.update({'indice': 0, 'respuestas_usuario': {}, 'estado': 'jugando'})
        st.rerun()
        
    if st.button("Ir al Menú", use_container_width=True, type="primary"):
        st.session_state.estado = 'menu'
        st.rerun()
