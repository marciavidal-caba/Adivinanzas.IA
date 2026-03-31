import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA MÁQUINA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# 2. CONEXIÓN CON LA LLAVE (SECRETS)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ CONFIGURA LA API KEY EN LOS SECRETS.")

# 3. FUNCIÓN PARA BUSCAR MODELO AUTOMÁTICO
@st.cache_resource
def configurar_modelo():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except:
        return None

model = configurar_modelo()

# 4. INTERFAZ EN MAYÚSCULAS
st.title("🤖✨ TECNO ADIVINANZAS MACHINE")
st.write("ESCRIBE EL OBJETO Y SU FUNCIÓN. ¡LA MÁQUINA CREARÁ UNA ADIVINANZA!")

# CUADROS DE TEXTO SIN SUGERENCIAS
objeto = st.text_input("1. ¿QUÉ PRODUCTO ES?", placeholder="")
funcion = st.text_input("2. ¿PARA QUÉ SIRVE?", placeholder="")

# BOTÓN DE ENCENDIDO
if st.button("✨ ¡ENCENDER LA MÁQUINA!"):
    if objeto and funcion:
        if model:
            with st.spinner('🤖 PROCESANDO DATOS...'):
                try:
                    # INSTRUCCIÓN ULTRA-ESTRICTA: SIN SALUDOS NI EXPLICACIONES
                    consigna = (
                        f"CREA UNA ADIVINANZA DE 4 VERSOS PARA NIÑOS DE 6 AÑOS "
                        f"SOBRE UN/A {objeto} QUE SIRVE PARA {funcion}. "
                        f"REGLAS ESTRICTAS: "
                        f"1. NO SALUDES. "
                        f"2. NO DIGAS 'HOLA'. "
                        f"3. NO DES EXPLICACIONES. "
                        f"4. ESCRIBE SOLO LOS 4 VERSOS Y LA PREGUNTA FINAL. "
                        f"5. TODO EN MAYÚSCULAS."
                    )
                    
                    resultado = model.generate_content(consigna)
                    
                    st.markdown("---")
                    st.subheader("📝 TU ADIVINANZA:")
                    
                    # DOBLE FILTRO DE MAYÚSCULAS
                    texto_final = resultado.text.upper()
                    st.write(texto_final)
                    
                except Exception as e:
                    st.error(f"LA MÁQUINA SE TRABÓ: {e}")
        else:
            st.error("NO SE ENCONTRÓ UN MODELO COMPATIBLE.")
    else:
        st.warning("COMPLETA LOS DOS CUADRITOS, POR FAVOR.")
