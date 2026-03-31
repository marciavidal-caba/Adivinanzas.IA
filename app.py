import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PESTAÑA Y PÁGINA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- ESTILO CSS PARA EL TÍTULO EN UNA SOLA LÍNEA ---
st.markdown("""
    <style>
    .titulo-machine {
        font-size: 30px !important;
        font-weight: bold;
        text-align: center;
        white-space: nowrap;
        color: #1E88E5;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN CON LA LLAVE (SECRETS)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ CONFIGURA LA API KEY EN LOS SECRETS DE STREAMLIT.")

# 3. FUNCIÓN TÉCNICA PARA BUSCAR EL MODELO DISPONIBLE
@st.cache_resource
def configurar_modelo():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except:
        return None

model = configurar_modelo()

# 4. INTERFAZ DE USUARIO (UI)
st.markdown('<p class="titulo-machine">🤖✨ TECNO ADIVINANZAS MACHINE</p>', unsafe_allow_html=True)
st.write("ESCRIBE EL OBJETO Y SU FUNCIÓN. ¡LA MÁQUINA CREARÁ TU ADIVINANZA!")

# CUADROS DE TEXTO CON AUTOCOMPLETE DESACTIVADO (SIN HISTORIAL)
objeto = st.text_input("1. ¿QUÉ PRODUCTO ES?", placeholder="", autocomplete="off")
funcion = st.text_input("2. ¿PARA QUÉ SIRVE?", placeholder="", autocomplete="off")

# 5. LÓGICA DE GENERACIÓN
if st.button("✨ CREA TU ADIVINANZA TECNOLÓGICA"):
    if objeto and funcion:
        if model:
            with st.spinner('🤖 EL ROBOT ESTÁ PENSANDO...'):
                try:
                    # PROMPT ESTRUCTURADO: FUNCIÓN (V1-2) -> FORMA (V3-4)
                    consigna = (
                        f"ERES UN DOCENTE DE PRIMARIA. CREA UNA ADIVINANZA MUY CORTA SOBRE UN/A {objeto}. "
                        f"SIGUE ESTRICTAMENTE ESTA ESTRUCTURA DE 4 VERSOS: "
                        f"LOS PRIMEROS 2 VERSOS DEBEN EXPLICAR QUE SIRVE PARA {funcion}. "
                        f"LOS ÚLTIMOS 2 VERSOS DEBEN DESCRIBIR SU FORMA, COLOR O MATERIAL. "
                        f"REGLAS: NO SALUDES, NO DIGAS HOLA, SOLO ESCRIBE LOS 4 VERSOS Y '¿QUÉ SOY?'. "
                        f"TODO EL TEXTO DEBE ESTAR EN MAYÚSCULAS."
                    )
                    
                    resultado = model.generate_content(consigna)
                    
                    # PROCESAMIENTO DEL RESULTADO
                    st.markdown("---")
                    st.subheader("📝 TU ADIVINANZA:")
                    
                    # DOBLE FILTRO DE MAYÚSCULAS PARA SEGURIDAD
                    texto_final = resultado.text.upper()
                    st.write(texto_final)
                    
                    st.success("¡LISTO! YA PODÉS SACAR LA FOTO PARA EL PADLET. 📸")
                    
                except Exception as e:
                    st.error(f"HUBO UN ERROR TÉCNICO: {e}")
        else:
            st.error("NO SE ENCONTRÓ UN MODELO DE IA COMPATIBLE.")
    else:
        st.warning("POR FAVOR, COMPLETA LOS DOS CUADRITOS PARA CONTINUAR.")
