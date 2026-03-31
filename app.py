import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PESTAÑA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- ESTILO PARA QUE EL TÍTULO QUEDE EN UNA SOLA LÍNEA ---
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

# 4. INTERFAZ CON TÍTULO AJUSTADO
# USAMOS HTML PARA QUE EL ESTILO QUE CREAMOS ARRIBA SE APLIQUE
st.markdown('<p class="titulo-machine">🤖✨ TECNO ADIVINANZAS MACHINE</p>', unsafe_allow_html=True)
st.write("ESCRIBE EL OBJETO Y SU FUNCIÓN. ¡LA MÁQUINA CREARÁ UNA ADIVINANZA!")

# CUADROS DE TEXTO
objeto = st.text_input("1. ¿QUÉ PRODUCTO ES?", placeholder="")
funcion = st.text_input("2. ¿PARA QUÉ SIRVE?", placeholder="")

# BOTÓN DE ENCENDIDO
if st.button("✨ ¡ENCENDER LA MÁQUINA!"):
    if objeto and funcion:
        if model:
            with st.spinner('🤖 PROCESANDO DATOS...'):
                try:
                    consigna = (
                        f"CREA UNA ADIVINANZA DE 4 VERSOS PARA NIÑOS DE 6 AÑOS "
                        f"SOBRE UN/A {objeto} QUE SIRVE PARA {funcion}. "
                        f"REGLAS ESTRICTAS: NO SALUDES, NO DES EXPLICACIONES. "
                        f"ESCRIBE SOLO LOS 4 VERSOS Y LA PREGUNTA FINAL EN MAYÚSCULAS."
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
