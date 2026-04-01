import streamlit as st
import google.generativeai as genai
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PESTAÑA Y PÁGINA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- ESTILO CSS PERSONALIZADO (NEGRO + NARANJA #ffc300) ---
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
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN CON GOOGLE SHEETS
def guardar_en_excel(nombre, obj, func, adv):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        # RECUERDA CAMBIAR ESTE ID POR EL DE TU PLANILLA
        sheet = client.open_by_key("TU_ID_DE_GOOGLE_SHEET_AQUI").sheet1
        
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        # Ahora agregamos el Nombre en la segunda columna
        sheet.append_row([fecha, nombre.upper(), obj.upper(), func.upper(), adv.upper()])
    except Exception as e:
        print(f"Error guardando en Excel: {e}")

# 3. CONEXIÓN API GEMINI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ FALTA API KEY.")

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
    st.session_state["nombre"] = ""
    st.session_state["objeto"] = ""
    st.session_state["funcion"] = ""

# 4. INTERFAZ DE USUARIO
st.markdown('<p class="titulo-machine">🤖 TECNO ADIVINANZAS MACHINE ✨</p>', unsafe_allow_html=True)

# NUEVO CAMPO: NOMBRE DEL ALUMNO
nombre = st.text_input("¿CUÁL ES TU NOMBRE?", key="nombre", autocomplete="off")

st.write("---") # Una línea divisoria sutil

objeto = st.text_input("1. ¿QUÉ PRODUCTO ES?", key="objeto", autocomplete="off")
funcion = st.text_input("2. ¿PARA QUÉ SIRVE?", key="funcion", autocomplete="off")

col1, col2 = st.columns([2, 1])
with col1:
    btn_crear = st.button("✏️ CREA TU ADIVINANZA")
with col2:
    st.button("🗑️ BORRAR TODO", on_click=borrar_todo)

# 5. LÓGICA DE GENERACIÓN Y GUARDADO
if btn_crear:
    if nombre and objeto and funcion:
        if model:
            with st.spinner('🤖 ANALIZANDO...'):
                try:
                    consigna = (
                        f"ACTÚA COMO UN MAESTRO DE TECNOLOGÍA. EL ALUMNO {nombre} ESCRIBIÓ: '{objeto}' Y '{funcion}'. "
                        f"REGLA 1: SI LA FUNCIÓN ES NATURAL (COMO NADAR, CRECER SOLO, O ALGO QUE NO REQUIERE TRABAJO HUMANO), RESPONDE: "
                        f"¿ESTÁS SEGURO DE QUE ES UN PRODUCTO TECNOLÓGICO? VUELVE A INTENTARLO. "
                        f"REGLA 2: SI ES UN PRODUCTO DEL CAMPO O ALIMENTO PROCESADO, ACÉPTALO. "
                        f"REGLA 3: CREA UNA ADIVINANZA CORTA DE 4 VERSOS EN MAYÚSCULAS CON TILDES. "
                        f"REGLA 4: NO SALUDES. TERMINA CON: ¿QUÉ SOY?"
                    )
                    
                    resultado = model.generate_content(consigna)
                    respuesta = resultado.text.upper().strip()
                    
                    if "¿QUÉ SOY?" in respuesta:
                        st.markdown('<p class="adivinanza-subtitulo">📝 TU ADIVINANZA:</p>', unsafe_allow_html=True)
                        st.code(respuesta, language=None)
                        # GUARDAR EN EXCEL
                        guardar_en_excel(nombre, objeto, funcion, respuesta)
                    else:
                        st.markdown(f'<p style="font-size:20px; font-weight:bold; color:black;">🤖 {respuesta}</p>', unsafe_allow_html=True)
                except Exception as e:
                    st.error("INTENTA DE NUEVO EN UN MOMENTO.")
        else: st.error("MOTOR NO ENCONTRADO.")
    else:
        st.warning("POR FAVOR, COMPLETA TU NOMBRE Y LOS DOS CUADRITOS.")
