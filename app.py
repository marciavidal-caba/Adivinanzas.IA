import streamlit as st
import google.generativeai as genai
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- DISEÑO ESTÉTICO ---
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
        padding: 15px;
    }}
    div[data-testid="stCodeBlock"] code {{
        color: #000000 !important;
        font-size: 24px !important; 
        font-weight: 800 !important;
    }}
    div.stButton > button {{
        border-radius: 15px !important;
        font-weight: bold !important;
        height: 40px !important;
    }}
    div.stButton > button:first-child {{
        background-color: #ffc300 !important;
        color: #000000 !important;
        border: 2px solid #ffc300 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIÓN DE GUARDADO
def guardar_en_excel(nombre, obj, func, adv):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scope)
        client = gspread.authorize(creds)
        ID_PLANILLA = "1Sppk9CJ3s-jrUug9zVwDl5BWjVHS5kPBZEE2JmhcLfw" 
        sheet = client.open_by_key(ID_PLANILLA).sheet1
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sheet.append_row([ahora, nombre.upper(), obj.upper(), func.upper(), adv.upper()])
    except Exception as e:
        st.error(f"Error de Excel: {e}")

# 3. CONFIGURACIÓN IA CON AUTO-DETECCIÓN
model = None
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    try:
        # Buscamos qué modelos están disponibles en tu cuenta
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name or 'pro' in m.name:
                    model = genai.GenerativeModel(m.name)
                    break
    except Exception as e:
        st.error(f"Error al listar modelos: {e}")
else:
    st.error("FALTA API KEY EN SECRETS")

def borrar_todo():
    st.session_state["nombre"] = ""
    st.session_state["objeto"] = ""
    st.session_state["funcion"] = ""

# 4. INTERFAZ
st.markdown('<p class="titulo-machine">🤖 TECNO ADIVINANZAS MACHINE ✨</p>', unsafe_allow_html=True)

nombre = st.text_input("ESCRIBE TU NOMBRE", key="nombre", autocomplete="off")
objeto = st.text_input("PIENSA UN PRODUCTO TECNOLÓGICO Y ESCRIBELO", key="objeto", autocomplete="off")
funcion = st.text_input("¿CUÁL ES LA FUNCIÓN DEL PRODUCTO?", key="funcion", autocomplete="off")

col1, col2 = st.columns([2, 1])
with col1:
    btn_crear = st.button("✏️ CREA TU ADIVINANZA")
with col2:
    st.button("🗑️ BORRAR TODO", on_click=borrar_todo)

# 5. LÓGICA
if btn_crear:
    if nombre and objeto and funcion:
        if model:
            with st.spinner('🤖 CREANDO TU ADIVINANZA..'):
                try:
                    consigna = (
                        f"ERES UNA MÁQUINA DE ADIVINANZAS. ALUMNO: {nombre}. OBJETO: {objeto}. FUNCIÓN: {funcion}. "
                        f"SI LA FUNCIÓN ES NATURAL (CRECER, NADAR, VOLAR), RESPONDE: ¿ESTÁS SEGURO DE QUE ES UN PRODUCTO TECNOLÓGICO? VUELVE A INTENTARLO. "
                        f"SI ES CORRECTO, ESCRIBE SOLO UNA ADIVINANZA DE 4 VERSOS EN MAYÚSCULAS CON TILDES. TERMINA CON ¿QUÉ SOY? "
                        f"NO SALUDES NI EXPLIQUES NADA."
                    )
                    res = model.generate_content(consigna)
                    respuesta_ia = res.text.upper().strip()
                    
                    if "¿QUÉ SOY?" in respuesta_ia:
                        st.code(respuesta_ia, language=None)
                        guardar_en_excel(nombre, objeto, funcion, respuesta_ia)
                    else:
                        st.markdown(f'<p style="font-size:20px; font-weight:bold;">🤖 {respuesta_ia}</p>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error técnico al generar: {e}")
        else:
            st.error("No se encontró ningún modelo compatible. Revisa tu API KEY.")
    else:
        st.warning("POR FAVOR, COMPLETA TODOS LOS CAMPOS.")
