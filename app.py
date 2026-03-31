import streamlit as st
import google.generativeai as genai

# 1. Configuración de la Máquina
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# 2. Conexión con la Llave (Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Configura la API KEY en los Secrets.")

# 3. FUNCIÓN DE EXPERTO: Buscar modelo automático
@st.cache_resource
def configurar_modelo():
    try:
        # Buscamos qué modelos tienes permitidos
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Retorna el primer modelo válido que encuentre (ej: gemini-1.5-flash)
                return genai.GenerativeModel(m.name)
    except Exception as e:
        st.error(f"Error al buscar modelos: {e}")
    return None

model = configurar_modelo()

# 4. Interfaz Visual Limpia
st.title("🤖✨ TECNO ADIVINANZAS MACHINE")
st.write("Escribe el objeto y su función. ¡Crearé una adivinanza!")

# Cuadros de texto sin sugerencias
objeto = st.text_input("1. ¿Qué producto es?", placeholder="")
funcion = st.text_input("2. ¿Para qué sirve?", placeholder="")

# Botón de encendido
if st.button("✨ ¡ENCENDER LA MÁQUINA!"):
    if objeto and funcion:
        if model:
            with st.spinner('🤖 Procesando datos...'):
                try:
                    consigna = (
                        f"Crea una adivinanza de 4 versos para niños de 6 años "
                        f"sobre un/a {objeto} que sirve para {funcion}. "
                        f"No digas el nombre del objeto. Termina con: ¿Qué soy?"
                    )
                    resultado = model.generate_content(consigna)
                    
                    st.markdown("---")
                    st.subheader("📝 Tu Adivinanza:")
                    st.write(resultado.text)
                    st.success("¡Operación exitosa! 🚀")
                except Exception as e:
                    st.error(f"La máquina se trabó: {e}")
        else:
            st.error("No se encontró un modelo compatible. Revisa tu API KEY.")
    else:
        st.warning("Completa los dos cuadritos, por favor.")
