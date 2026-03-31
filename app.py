import streamlit as st
import google.generativeai as genai

# 1. Configuración visual: Robot y Estrellas
st.set_page_config(page_title="TECNO-ADIVINANZAS MAKER", page_icon="🤖")

# 2. Conexión con la API KEY (Desde los Secrets de Streamlit)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Configura la API KEY en los Secrets de Streamlit.")

# 3. Selección del modelo estable
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Interfaz Limpia
st.title("🤖✨ TECNO ADIVINANZAS")
st.write("Escribe el nombre de un objeto y para qué sirve. ¡Haré magia digital!")

# Cuadros de texto sin sugerencias (placeholder vacío)
objeto = st.text_input("1. ¿Qué producto es?", placeholder="")
funcion = st.text_input("2. ¿Para qué sirve?", placeholder="")

# Botón de acción
if st.button("✨ ¡Crear mi Adivinanza!"):
    if objeto and funcion:
        try:
            # Instrucción optimizada para 1er y 2do grado
            consigna = (
                f"Actúa como un maestro de primaria. Crea una adivinanza de 4 versos "
                f"para niños de 6 años sobre un/a {objeto} que sirve para {funcion}. "
                f"Usa rimas simples. No digas el nombre del objeto. "
                f"Termina siempre con la pregunta: ¿Qué soy?"
            )
            
            # Generar respuesta de la IA
            resultado = model.generate_content(consigna)
            
            st.markdown("---")
            st.subheader("📝 Tu Adivinanza Robotizada:")
            st.write(resultado.text)
            
            st.divider()
            st.info("💡 ¡Sácale una foto o captura y súbela al Padlet!")
            
        except Exception as e:
            # Si el modelo flash falla, intentamos con el pro automáticamente
            try:
                model_alt = genai.GenerativeModel('gemini-1.0-pro')
                resultado = model_alt.generate_content(consigna)
                st.write(resultado.text)
            except:
                st.error(f"El robot tuvo un pequeño cortocircuito: {e}")
    else:
        st.warning("Por favor, completa los dos cuadritos de arriba.")
