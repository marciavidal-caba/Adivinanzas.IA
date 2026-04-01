import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PESTAÑA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .titulo-machine {
        font-size: 26px !important;
        font-weight: bold;
        text-align: center;
        white-space: nowrap;
        color: #000000;
        margin-bottom: 20px;
    }
    .adivinanza-texto {
        color: #000000;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN CON LA LLAVE
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ CONFIGURA LA API KEY EN LOS SECRETS.")

# 3. FUNCIÓN PARA BUSCAR MODELO
@st.cache_resource
def configurar_modelo():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except:
        return None

model = configurar_modelo()

# --- FUNCIÓN PARA BORRAR TODO ---
def borrar_todo():
    st.session_state["objeto"] = ""
    st.session_state["funcion"] = ""

# 4. INTERFAZ DE USUARIO (UI)
st.markdown('<p class="titulo-machine">🤖✨ TECNO ADIVINANZAS MACHINE</p>', unsafe_allow_html=True)
st.write("ESCRIBE EL OBJETO Y SU FUNCIÓN. ¡LA MÁQUINA CREARÁ TU ADIVINANZA!")

# CUADROS DE TEXTO CON "KEY" PARA PODER BORRARLOS
objeto = st.text_input("1. ¿QUÉ PRODUCTO ES?", key="objeto", autocomplete="off")
funcion = st.text_input("2. ¿PARA QUÉ SIRVE?", key="funcion", autocomplete="off")

# FILA DE BOTONES
col1, col2 = st.columns(2)

with col1:
    btn_crear = st.button("✨ CREA TU ADIVINANZA")

with col2:
    # BOTÓN PARA BORRAR
    st.button("🗑️ BORRAR TODO", on_click=borrar_todo)

# 5. LÓGICA DE GENERACIÓN CON VALIDACIÓN
if btn_crear:
    if objeto and funcion:
        if model:
            with st.spinner('🤖 EL ROBOT ESTÁ ANALIZANDO...'):
                try:
                    # PROMPT CON LÓGICA DE VALIDACIÓN
                    consigna = (
                        f"ACTÚA COMO UN MAESTRO QUE AYUDA A NIÑOS DE 6 AÑOS. "
                        f"EL NIÑO DICE QUE UN/A '{objeto}' SIRVE PARA '{funcion}'. "
                        f"REGLA 1: SI LA FUNCIÓN NO TIENE SENTIDO CON EL OBJETO, RESPONDE EXACTAMENTE: "
                        f"'¿ESTÁS SEGURO QUE ESA ES LA FUNCIÓN? PIENSA UN POCO MÁS ¿PARA QUÉ SE USA EL/LA {objeto}?' "
                        f"REGLA 2: SI LO QUE ESCRIBIÓ NO SE ENTIENDE O SON LETRAS AL AZAR, RESPONDE: "
                        f"'¡UPS! NO ENTENDÍ, PUEDES ESCRIBIR DE NUEVO.' "
                        f"REGLA 3: SI TODO TIENE SENTIDO, CREA UNA ADIVINANZA DE 4 VERSOS: "
                        f"V1 Y V2 SOBRE LA FUNCIÓN, V3 Y V4 SOBRE LA FORMA O COLOR. "
                        f"TODO EN MAYÚSCULAS. SIN SALUDOS."
                    )
                    
                    resultado = model.generate_content(consigna)
                    respuesta = resultado.text.upper()
                    
                    st.markdown("---")
                    
                    # SI ES UNA ADIVINANZA (TIENE PREGUNTA), USAMOS EL CUADRO DE COPIADO
                    if "¿QUÉ SOY?" in respuesta or "¿QUE SOY?" in respuesta:
                        st.markdown('<p class="adivinanza-texto">📝 TU ADIVINANZA:</p>', unsafe_allow_html=True)
                        st.code(respuesta, language=None)
                    else:
                        # SI ES UN MENSAJE DE ERROR DE LA IA, LO MOSTRAMOS SIMPLE
                        st.warning(respuesta)
                    
                except Exception as e:
                    st.error(f"HUBO UN ERROR: {e}")
    else:
        st.warning("POR FAVOR, COMPLETA LOS DOS CUADRITOS.")
