import streamlit as st
import google.generativeai as genai
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- ESTILO CSS COMPACTO ---
st.markdown(f"""
    <style>
    .block-container {{ padding-top: 1rem !important; padding-bottom: 0rem !important; }}
    .stApp, div[data-testid="stMarkdownContainer"] p, .stWidgetLabel, .stTextInput input, p {{
        color: #000000 !important;
        font-family: 'Source Sans Pro', sans-serif;
        margin-bottom: 5px !important;
    }}
    .titulo-machine {{
        font-size: 26px !important;
        font-weight: bold;
        text-align: center;
        color: #000000 !important;
        margin-bottom: 10px !important;
    }}
    div[data-testid="stCodeBlock"] {{
        border: 4px solid #ffc300;
        border-radius: 15px;
        background-color: #f9f9f9;
        padding: 10px;
        margin-top: 5px !important;
    }}
    div[data-testid="stCodeBlock"] code {{
        color: #000000 !important;
        font-size: 22px !important; 
        font-weight: 800 !important;
        white-space: pre-wrap !important;
    }}
    div.stButton > button {{
        border-radius: 15px !important;
        font-weight: bold !important;
        padding: 2px 10px !important;
        height: 35px !important;
    }}
    div.stButton > button:first-child {{
        background-color: #ffc300 !important;
        color: #000000 !important;
        border: 2px solid #ffc300 !important;
    }}
    div.stButton > button[data-testid="baseButton-secondary"] {{
        background-color: #eeeeee !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN CON GOOGLE SHEETS
def guardar_en_excel(nombre, obj, func, adv):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scope)
        client = gspread.authorize(creds)
        
        # === TU ID DE EXCEL AQUÍ ===
        ID_PLANILLA = "TU_ID_DE_GOOGLE_SHEET_AQUÍ" 
        sheet = client.open_by_key(ID_PLANILLA).sheet1
        
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sheet.append_row([fecha_hora, nombre.upper(), obj.upper(), func.upper(), adv.upper()])
    except Exception as e:
        print(f"Error al guardar: {e}")

# 3. CONFIGURACIÓN IA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def borrar_todo():
    st.session_state["nombre"] = ""
    st.session_state["objeto"] = ""
    st.session_state["funcion"] = ""

# 4. INTERFAZ
st.markdown('<p class="titulo-machine">🤖 TECNO ADIVINANZAS MACHINE ✨</p>', unsafe_allow_html=True)

nombre = st.text_input("¿CUÁL ES TU NOMBRE?", key="nombre", autocomplete="off")
objeto = st.text_input("¿QUÉ PRODUCTO ES?", key="objeto", autocomplete="off")
funcion = st.text_input("¿PARA QUÉ SIRVE?", key="funcion", autocomplete="off")

col1, col2 = st.columns([2, 1])
with col1:
    btn_crear = st.button("✏️ CREA TU ADIVINANZA")
with col2:
    st.button("🗑️ BORRAR", on_click=borrar_todo)

# 5. LÓGICA DE CONTROL (LA MÁQUINA DE ADIVINANZAS)
if btn_crear:
    if nombre and objeto and funcion:
        with st.spinner('🤖 CREANDO...'):
            try:
                # CONSIGNA REFORZADA PARA EVITAR CHARLAS
                consigna = (
                    f"CONTEXTO: ALUMNO DE 6 AÑOS. OBJETO: {objeto}. FUNCIÓN: {funcion}. "
                    f"TAREA: EVALUAR SI ES PRODUCTO TECNOLÓGICO O NATURAL. "
