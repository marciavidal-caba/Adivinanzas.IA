import streamlit as st
import google.generativeai as genai

# Configuración de página
st.set_page_config(page_title="El Sabio de los Inventos", page_icon="🧙‍♂️")

# Conexión Segura con la API KEY
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la API KEY en los Secrets de Streamlit.")

# Usamos el modelo más estable
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🧙‍♂️ El Sabio de los Inventos")
st.write("Escribe el nombre de un objeto y para qué sirve.")

objeto = st.text_input("1. ¿Qué es?", placeholder="Ej: Paraguas")
funcion = st.text_input("2. ¿Para qué sirve?", placeholder="Ej: Para no mojarse")

if st.button("✨ ¡Crear Adivinanza!"):
    if objeto and funcion:
        try:
            prompt = f"Eres un maestro de niños de 6 años. Crea una adivinanza corta de 4 versos sobre un/a {objeto} que sirve para {funcion}. No digas el nombre del objeto. Termina con: ¿Qué soy?"
            response = model.generate_content(prompt)
            st.success("¡Aquí tienes!")
            st.subheader(response.text)
        except Exception as e:
            st.error(f"Hubo un problemita: {e}")
    else:
        st.warning("Completa los dos cuadritos, por favor.")
