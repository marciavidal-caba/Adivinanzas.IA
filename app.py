import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PESTAÑA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- ESTILO CSS (FUERZA NEGRO E IMPRENTA) ---
st.markdown(f"""
    <style>
    .stApp, div[data-testid="stMarkdownContainer"] p, .stWidgetLabel, .stTextInput input, p {{
        color: #000000 !important;
        font-family: 'Source Sans Pro', sans-serif;
    }}
    .titulo-machine {{
        font-size: 28px !important;
        font-weight: bold;
        text-align: center;
        color: #000000 !important;
        margin-bottom: 25px;
    }}
    .adivinanza-subtitulo {{
        color: #000000 !important;
        font-size: 22px;
        font-weight: bold;
        margin-top: 15px;
    }}
    div[data-testid="stCodeBlock"] {{
        border: 4px solid #ffc300;
        border-radius: 20px;
        background-color: #f9f9f9;
        padding: 15px;
    }}
    div[data-testid="stCodeBlock"] code {{
        color: #000000 !important;
        font-size: 24px !important; 
        font-weight: 800 !important;
        white-space: pre-wrap !important;
    }}
    div.stButton > button {{
        border-radius: 20px !important;
        font-weight: bold !important;
        padding: 5px 15px !important; 
    }}
    div.stButton > button:first-child {{
        background-color: #ffc300 !important;
        color: #000000 !important;
        border: 2px solid #ffc300 !important;
    }}
    div.stButton > button[data-testid="baseButton-secondary"] {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #cccccc !important;
    }}
    .mensaje-robot {{
        font-size: 20px;
        font-weight: bold;
        color: #000000;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ FALTA API KEY.")

# 3. MOTOR IA
@st.cache_resource
def configurar_modelo():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
        return None
    except: return None

model = configurar_modelo()

def borrar_todo():
    st.session_state["objeto"] = ""
    st.session_state["funcion"] = ""

# 4. INTERFAZ
st.markdown('<p class="titulo-machine">🤖 TECNO ADIVINANZAS MACHINE ✨</p>', unsafe_allow_html=True)
st.write("ESCRIBE EL OBJETO Y SU FUNCIÓN. ¡LA MÁQUINA CREARÁ TU ADIVINANZA!")

objeto = st.text_input("1. ¿QUÉ PRODUCTO ES?", key="objeto", autocomplete="off")
funcion = st.text_input("2. ¿PARA QUÉ SIRVE?", key="funcion", autocomplete="off")

col1, col2 = st.columns([2, 1])
with col1:
    btn_crear = st.button("✏️ CREA TU ADIVINANZA")
with col2:
    st.button("🗑️ BORRAR", on_click=borrar_todo)

# 5. LÓGICA DE CONTROL ESTRICTO
if btn_crear:
    if objeto and funcion:
        if model:
            with st.spinner('🤖 ANALIZANDO...'):
                try:
                    # INSTRUCCIONES ULTRA-ESTRICTAS PARA EVITAR DIÁLOGO
                    consigna = (
                        f"TAREA: ESCRIBIR UNA ADIVINANZA TECNOLÓGICA. "
                        f"OBJETO: {objeto}. FUNCIÓN: {funcion}. "
                        f"REGLA DE ORO: NO SALUDES, NO EXPLIQUES NADA, NO DES COMENTARIOS. "
                        f"REGLA DE PRODUCTO: SI '{objeto}' NO ES UN PRODUCTO TECNOLÓGICO (ES ALGO NATURAL), "
                        f"RESPONDE SOLO: ¿ESTÁS SEGURO QUE ES UN PRODUCTO TECNOLÓGICO? VUELVE A INTENTARLO. "
                        f"REGLA DE FORMATO: 4 VERSOS CORTOS. V1 Y V2 FUNCIÓN. V3 Y V4 FORMA O PROCESO. "
                        f"AL FINAL ESCRIBE '¿QUÉ SOY?'. "
                        f"TODO EN MAYÚSCULAS."
                    )
                    
                    resultado = model.generate_content(consigna)
                    respuesta = resultado.text.upper().strip()
                    
                    # FILTRO DE SEGURIDAD PARA QUE NO SE "ESCAPE" NADA
                    if "¿QUÉ SOY?" in respuesta or "¿QUE SOY?" in respuesta:
                        st.markdown('<p class="adivinanza-subtitulo">📝 TU ADIVINANZA:</p>', unsafe_allow_html=True)
                        st.code(respuesta, language=None)
                    else:
                        st.markdown(f'<p class="mensaje-robot">🤖 {respuesta}</p>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error("INTENTA DE NUEVO EN UN MOMENTO.")
        else: st.error("MOTOR NO ENCONTRADO.")
    else: st.warning("COMPLETA LOS DOS CUADRITOS.")
