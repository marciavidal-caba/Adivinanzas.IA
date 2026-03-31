import streamlit as st
import google.generativeai as genai

# 1. Título e Icono en la pestaña
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# 2. Conexión con la llave (Asegúrate que en Secrets diga GOOGLE_API_KEY)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ No hay llave configurada.")

# 3. EL CAMBIO CLAVE: Usamos 'gemini-pro' (Es el más estable del mundo)
model = genai.GenerativeModel('gemini-pro')

# 4. Interfaz Visual
st.title("🤖✨ TECNO ADIVINANZAS MACHINE")
st.write("¡Hola! Soy tu máquina de inventos. Escribe y crearé magia.")

# Cuadros de texto limpios
objeto = st.text_input("1. ¿Qué producto tecnológico es?", placeholder="")
funcion = st.text_input("2. ¿Para qué sirve?", placeholder="")

# Botón de encendido
if st.button("✨ ¡ENCENDER LA MÁQUINA!"):
    if objeto and funcion:
        # Usamos un mensaje de espera animado
        with st.spinner('🤖 Procesando datos...'):
            try:
                # Instrucción para la IA
                consigna = (
                    f"Eres un robot que crea adivinanzas para niños de 6 años. "
                    f"Crea una adivinanza de 4 versos sobre un/a {objeto} que sirve para {funcion}. "
                    f"No digas el nombre del objeto. Termina con: ¿Qué soy?"
                )
                
                # Generar respuesta
                resultado = model.generate_content(consigna)
                
                st.markdown("---")
                st.subheader("📝 Tu Adivinanza:")
                st.write(resultado.text)
                st.success("¡Logrado! ✨")
                
            except Exception as e:
                # Si esto falla, te dirá el error exacto para que yo lo arregle
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Escribe en los dos cuadritos, por favor.")
