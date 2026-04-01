import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PESTAÑA Y PÁGINA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- SÚPER ESTILO CSS PERSONALIZADO (NEGRO + NARANJA #ffc300) ---
st.markdown(f"""
    <style>
    /* 1. Fuerza color NEGRO en toda la app y textos base */
    .stApp, div[data-testid="stMarkdownContainer"] p, .stWidgetLabel, .stTextInput input, p {{
        color: #000000 !important;
        font-family: 'Source Sans Pro', sans-serif;
    }}
    
    /* 2. Estilo para el Título */
    .titulo-machine {{
        font-size: 28px !important;
        font-weight: bold;
        text-align: center;
        color: #000000 !important;
        margin-bottom: 25px;
        white-space: nowrap;
    }}

    /* 3. Estilo para el Subtítulo de la adivinanza */
    .adivinanza-subtitulo {{
        color: #000000 !important;
        font-size: 22px;
        font-weight: bold;
        margin-top: 15px;
    }}

    /* 4. RECUADRO DE ADIVINANZA (Texto más grande y negrita) */
    div[data-testid="stCodeBlock"] {{
        border: 4px solid #ffc300;
        border-radius: 20px;
        background-color: #f9f9f9;
        padding: 10px;
    }}
    div[data-testid="stCodeBlock"] code {{
        color: #000000 !important;
        font-size: 24px !important; 
        font-weight: 800 !important; 
    }}

    /* 5. BOTONES PEQUEÑOS Y REDONDEADOS */
    div.stButton > button {{
        border-radius: 20px !important;
        font-weight: bold !important;
        padding: 5px 15px !important; 
        font-size: 14px !important;
        transition: all 0.3s ease;
    }}

    /* Botón principal (Naranja) */
    div.stButton > button:first-child {{
        background-color: #ffc300 !important;
        color: #000000 !important;
        border: 2px solid #ffc300 !important;
    }}

    /* Botón borrar (Blanco/Gris) */
    div.stButton > button[data-testid="baseButton-secondary"] {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #cccccc !important;
    }}

    /* Estilo para mensajes de validación del robot */
    .mensaje-robot {{
        font-size: 20px;
        font-weight: bold;
        color: #000000;
        padding: 10px;
    }}

    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN CON LA LLAVE (SECRETS)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ CONFIGURA LA API KEY EN LOS SECRETS.")

# 3. DETECTOR AUTOMÁTICO DE MODELO
@st.cache_resource
def configurar_modelo():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
        return None
    except:
        return None

model = configurar_modelo()

# 4. FUNCIÓN PARA BORRAR TODO
def borrar_todo():
    st.session_state["objeto"] = ""
    st.session_state["funcion"] = ""

# 5. INTERFAZ DE USUARIO (UI)
st.markdown('<p class="titulo-machine">🤖 TECNO ADIVINANZAS MACHINE ✨</p>', unsafe_allow_html=True)
st.write("ESCRIBE EL OBJETO Y SU FUNCIÓN. ¡LA MÁQUINA CREARÁ TU ADIVINANZA!")

# CUADROS DE TEXTO
objeto = st.text_input("1. ¿QUÉ PRODUCTO ES?", key="objeto", autocomplete="off")
funcion = st.text_input("2. ¿PARA QUÉ SIRVE?", key="funcion", autocomplete="off")

# FILA DE BOTONES AJUSTADA
col1, col2 = st.columns([2, 1])

with col1:
    btn_crear = st.button("✏️ CREA TU ADIVINANZA")

with col2:
    st.button("🗑️ BORRAR", on_click=borrar_todo)

# 6. LÓGICA DE GENERACIÓN CON FILTRO TECNOLÓGICO
if btn_crear:
    if objeto and funcion:
        if model:
            with st.spinner('🤖 ANALIZANDO...'):
                try:
                    # PROMPT ESPECIALIZADO EN PRODUCTOS TECNOLÓGICOS (OBJETOS, SERVICIOS Y PROCESOS)
                    consigna = (
                        f"ACTÚA COMO UN MAESTRO DE TECNOLOGÍA. EL ALUMNO ESCRIBIÓ: '{objeto}' Y DICE QUE SIRVE PARA '{funcion}'. "
                        f"DEFINICIÓN: UN PRODUCTO TECNOLÓGICO ES TODO LO CREADO O TRANSFORMADO POR
