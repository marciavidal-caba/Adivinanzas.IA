import streamlit as st
import google.generativeai as genai
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- ESTILO CSS COMPACTO Y SIN LÍNEAS ---
st.markdown(f"""
    <style>
    /* Eliminar espacios en blanco superiores */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }}
    
    /* Texto en Negro e Imprenta */
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

    /* Recuadro de Adivinanza (Grande y Negro) */
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

    /* Botones Compactos */
    div.stButton > button {{
        border-radius: 15px !important;
        font-weight: bold !important;
        padding: 2px 10px !important;
        height: 35px !important;
    }}
    
    /* Botón Crear (Naranja) */
    div.stButton > button:first-child {{
        background-color: #ffc300 !important;
        color: #000000 !important;
        border: 2px solid #ffc300 !important;
    }}

    /* Botón Borrar (Gris claro) */
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
        
        # === REEMPLAZA ESTO CON TU ID DE EXCEL ===
        ID_PLANILLA = "TU_ID_DE_GOOGLE_SHEET_AQUÍ" 
        sheet = client.open_by_key(ID_PLANILLA).sheet1
        
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        sheet.append_row([fecha, nombre.upper(), obj.upper(), func.upper(), adv.upper()])
    except Exception as e:
        print(f"Error al guardar: {e}")

# 3. CONFIGURACIÓN IA (API KEY)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ FALTA API KEY EN SECRETS.")

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

# 4. INTERFAZ (ORDEN COMPACTO)
st.markdown('<p class="titulo-machine">🤖 TECNO ADIVINANZAS MACHINE ✨</p>', unsafe_allow_html=True)

# Inputs seguidos sin separadores
nombre = st.text_input("¿CUÁL ES TU NOMBRE?", key="nombre", autocomplete="off")
objeto = st.text_input("1. ¿QUÉ PRODUCTO ES?", key="objeto", autocomplete="off")
funcion = st.text_input("2. ¿PARA QUÉ SIRVE?", key="funcion", autocomplete="off")

# Botones en una fila
col1, col2 = st.columns([2, 1])
with col1:
    btn_crear = st.button("✏️ CREA TU ADIVINANZA")
with col2:
    st.button("🗑️ BORRAR", on_click=borrar_todo)

# 5. LÓGICA DE CONTROL Y GUARDADO
if btn_crear:
    if nombre and objeto and funcion:
        if model:
            with st.spinner('🤖 ANALIZANDO...'):
                try:
                    consigna = (
                        f"ACTÚA COMO UN MAESTRO DE TECNOLOGÍA. ALUMNO: {nombre}. OBJETO: {objeto}. FUNCIÓN: {funcion}. "
                        f"SI LA FUNCIÓN ES NATURAL (COMO NADAR, CRECER SOLO, O ALGO QUE NO REQUIERE TRABAJO HUMANO), RESPONDE EXACTAMENTE: "
                        f"¿ESTÁS SEGURO DE QUE ES UN PRODUCTO TECNOLÓGICO? VUELVE A INTENTARLO. "
                        f"CASO CONTRARIO, CREA UNA ADIVINANZA MUY BREVE (4 VERSOS), MAYÚSCULAS, CON TILDES. "
                        f"PROHIBIDO SALUDAR. TERMINA CON: ¿QUÉ SOY?"
                    )
                    resultado = model.generate_content(consigna)
                    respuesta = resultado.text.upper().strip()
                    
                    if "¿QUÉ SOY?" in respuesta:
                        st.code(respuesta, language=None)
                        guardar_en_excel(nombre, objeto, funcion, respuesta)
                    else:
                        st.markdown(f'<p style="font-size:20px; font-weight:bold;">🤖 {respuesta}</p>', unsafe_allow_html=True)
                except Exception as e:
                    st.error("INTENTA DE NUEVO.")
        else: st.error("MOTOR NO ENCONTRADO.")
    else:
        st.warning("POR FAVOR, COMPLETA TODOS LOS CAMPOS.")
