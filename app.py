import streamlit as st
import google.generativeai as genai

# 1. Configuración de la pestaña y el icono
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# 2. Conexión con la API KEY (Configurada en Secrets de Streamlit)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Configura la API KEY en los Secrets de Streamlit.")

# 3. Configuración del Modelo (Usamos el nombre más compatible del 2026)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Interfaz Visual: Título y Estrellas
st.title("🤖✨ TECNO ADIVINANZAS MACHINE")
st.write("Escribe el objeto y para qué sirve. ¡La máquina creará una adivinanza!")

# Cuadros de texto limpios para niños (sin sugerencias)
objeto = st.text_input("1. ¿Qué producto es?", placeholder="")
funcion = st.text_input("2. ¿Para qué sirve?", placeholder="")

# Botón de acción
if st.button("✨ ¡ENCENDER LA MÁQUINA!"):
    if objeto and funcion:
        try:
            # Instrucción interna para la IA
            consigna = (
                f"Eres un experto en educación infantil. Crea una adivinanza "
                f"para niños de 6 años sobre un/a {objeto} que sirve para {funcion}. "
                f"Usa 4 versos con rimas muy simples. No digas el nombre del objeto. "
                f"Termina con la pregunta: ¿Qué soy?"
            )
            
            # Generar la respuesta
            resultado = model.generate_content(consigna)
            
            st.markdown("---")
            st.subheader("📝 Tu Adivinanza:")
            st.write(resultado.text)
            
            st.divider()
            st.info("💡 ¡Sácale una foto y súbela al muro de Padlet!")
            
        except Exception as e:
            # Si hay error de modelo, intentamos una ruta alternativa
            st.error(f"La máquina está procesando datos. Intenta tocar el botón otra vez.")
    else:
        st.warning("La máquina necesita que completes los dos espacios.")
