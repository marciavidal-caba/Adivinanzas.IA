import streamlit as st
import google.generativeai as genai

# Configuramos la página para que se vea bien en tablets
st.set_page_config(page_title="La Máquina de Adivinanzas", page_icon="🧙‍♂️")

# CONECTAMOS CON TU API KEY (Usaremos un secreto por seguridad)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.title("🧙‍♂️ El Sabio de los Inventos")
st.write("Escribe el nombre de un objeto y para qué sirve. ¡Haré una adivinanza mágica!")

# Cuadros de texto grandes
objeto = st.text_input("1. ¿Qué producto es?", placeholder="Ejemplo: Botella")
funcion = st.text_input("2. ¿Para qué sirve?", placeholder="Ejemplo: Para guardar agua")

if st.button("✨ ¡Crear mi Adivinanza!"):
    if objeto and funcion:
        with st.spinner('El sabio está pensando...'):
            prompt = f"Eres un maestro de primer grado. Crea una adivinanza de 4 versos rimados para niños de 6 años sobre un/a {objeto} cuya función es {funcion}. No menciones el nombre del objeto en la adivinanza. Termina con la pregunta ¿Qué soy?"
            response = model.generate_content(prompt)
            
            st.markdown("---")
            st.subheader("📝 Tu Adivinanza:")
            st.write(response.text)
            
            # Recordatorio para el registro en Padlet
            st.info("💡 ¡Copia esta adivinanza y pégala en nuestro Padlet con una foto!")
    else:
        st.error("¡Ups! El sabio necesita que escribas en los dos cuadritos.")
