import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PESTAÑA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- ESTILO PARA EL TÍTULO EN UNA LÍNEA ---
st.markdown("""
    <style>
    .titulo-machine {
        font-size: 32px !important;
        font-weight: bold;
        text-align: center;
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True)

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

# 4. INTERFAZ VISUAL
st.markdown('<p class="titulo-machine">🤖✨ TECNO ADIVINANZAS MACHINE</p>', unsafe_allow_html=True)
st.write("ESCRIBE EL OBJETO Y SU FUNCIÓN. ¡LA MÁQUINA CREARÁ TU ADIVINANZA!")

# CUADROS DE TEXTO
objeto = st.text_input("1. ¿QUÉ PRODUCTO ES?", placeholder="")
funcion = st.text_input("2. ¿PARA QUÉ SIRVE?", placeholder="")

# --- CAMBIO DE NOMBRE EN EL BOTÓN ---
if st.button("✨ CREA TU ADIVINANZA TECNOLÓGICA"):
    if objeto and funcion:
        if model:
            with st.spinner('🤖 PROCESANDO DATOS...'):
                try:
                    # INSTRUCCIÓN ESTRUCTURADA: FUNCIÓN -> FORMA -> BREVEDAD
                    consigna = (
                        f"ERES UN MAESTRO DE PRIMER GRADO. CREA UNA ADIVINANZA CORTA SOBRE UN/A {objeto}. "
                        f"SIGUE ESTA ESTRUCTURA DE 4 VERSOS BREVES: "
                        f"VERSOS 1 Y 2: DESCRIBE QUE SIRVE PARA {funcion}. "
                        f"VERSOS 3 Y 4: DESCRIBE SU FORMA, COLOR O MATERIAL. "
                        f"REGLAS: NO SALUDES, NO DES PISTAS EXTRAS, SOLO LOS 4 VERSOS Y '¿QUÉ SOY?'. "
                        f"TODO EN MAYÚSCULAS."
                    )
                    
                    resultado = model.generate_content(consigna)
                    
                    st.markdown("---")
                    st.subheader("📝 TU ADIVINANZA:")
                    st.write(resultado.text.upper())
                    
                except Exception as e:
                    st.error(f"LA MÁQUINA SE TRABÓ: {e}")
        else:
            st.error("NO SE ENCONTRÓ UN MODELO COMPATIBLE.")
    else:
        st.warning("COMPLETA LOS DOS CUADRITOS, POR FAVOR.")
