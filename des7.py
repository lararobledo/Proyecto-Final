import streamlit as st
import os
from groq import Groq

st.set_page_config(
    page_title="Mi chat de IA",
    page_icon="👻",
    layout="centered",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
        html, body, .block-container {
            background-color: #C0D6DF;
            color: #0A0A0A;
        }
        .stButton>button {
            background-color: #F6D7A7;
            color: #0A0A0A;
            font-weight: bold;
            border-radius: 8px;
        }
        .stTextInput>div>div>input {
            background-color: #F6D7A7;
            color: #0A0A0A;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Este es mi chat de IA")
st.subheader("Mi primera aplicación con Streamlit")

nombre = st.text_input("¿Cómo te llamás?", key="nombre_usuario")
if st.button("Saludar"):
    st.write(f"Hola {nombre}, ¡espero que estés bien! 😊")

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def crear_usuario_groq():
    clave_secreta = st.secrets["API_KEY"]
    return Groq(api_key=clave_secreta)

def configurar_pagina():
    st.sidebar.title("Configuración de la IA")
    elegirModelo = st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, key="modelo_selector")
    return elegirModelo

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state["mensajes"] = []

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
    )

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    modelo = configurar_pagina()
    cliente = crear_usuario_groq()
    inicializar_estado()
    area_chat()

    mensajeDeEntrada = st.chat_input('Escribí tu mensaje')

    if mensajeDeEntrada:
        actualizar_historial("user", mensajeDeEntrada, "🐵")
        chat_completo = configurar_modelo(cliente, modelo, mensajeDeEntrada)

        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun()

if __name__ == "__main__":
    main()
