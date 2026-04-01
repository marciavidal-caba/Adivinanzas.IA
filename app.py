import streamlit as st
import google.generativeai as genai
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- DISEÑO ESTÉTICO COMPACTO (NEGRO Y NARANJA) ---
st.markdown(f"""
    <style>
    /* Eliminar márgenes superiores */
    .block-container {{ padding-top: 1rem !important; padding-bottom: 0rem !important; }}
    
    /* Todo el texto en Negro */
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

    /* Recuadro de Adivinanza (Borde Naranja) */
    div[data-testid="stCodeBlock"] {{
        border: 4px solid #ffc300;
        border-radius: 15px;
        background-color: #f9f9f9;
        padding: 15px;
        margin-top: 5px !important;
    }}
    div[data-testid="stCodeBlock"] code {{
        color: #000000 !important;
        font-size: 24px !important; 
        font-weight: 800 !important;
        white-space: pre-wrap !important;
    }}

    /* Botones Personalizados */
    div.stButton > button {{
        border-radius: 15px !important;
        font-weight: bold !important;
        height: 40px !important;
    }}
    
    /* Botón CREAR (Naranja) */
    div.stButton > button:first-child {{
        background-color: #ffc300 !important;
        color: #000000 !important;
        border: 2px solid #ffc300 !important;
    }}

    /* Botón BORRAR (Gris) */
    div.stButton > button[data-testid="baseButton-secondary"] {{
        background-color: #eeeeee !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIÓN DE GUARDADO EN GOOGLE SHEETS
def guardar_en_excel(nombre, obj, func, adv):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scope)
        client = gspread.authorize(creds)
        
        # TU ID DE EXCEL INTEGRADO
        ID_PLANILLA = "1Sppk9CJ3s-jrUug9zVwDl5BWjVHS5kPBZEE2JmhcLfw" 
        sheet = client.open_by_key(ID_PLANILLA).sheet1
        
        # Registro de Fecha y Hora exacta
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sheet.append_row([ahora, nombre.upper(), obj.upper(), func.upper(), adv.upper()])
    except Exception as e:
        st.error(f"Error al conectar con el Excel: {e}")

# 3. CONFIGURACIÓN IA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def borrar_todo():
    st.session_state["nombre"] = ""
    st.session_state["objeto"] = ""
    st.session_state["funcion"] = ""

# 4. INTERFAZ DE USUARIO (SIN LÍNEAS DIVISORIAS)
st.markdown('<p class="titulo-machine">🤖 TECNO ADIVINANZAS MACHINE ✨</p>', unsafe_allow_html=True)

nombre = st.text_input("ESCRIBE TU NOMBRE", key="nombre", autocomplete="off")
objeto = st.text_input("PIENSA UN PRODUCTO TECNOLÓGICO Y ESCRIBELO", key="objeto", autocomplete="off")
funcion = st.text_input("¿CUÁL ES LA FUNCIÓN DEL PRODUCTO?", key="funcion", autocomplete="off")

col1, col2 = st.columns([2, 1])
with col1:
    btn_crear = st.button("✏️ CREA TU ADIVINANZA")
with col2:
    st.button("🗑️ BORRAR TODO", on_click=borrar_todo)

# 5. LÓGICA DE CONTROL (EL "CEREBRO" DE LA MÁQUINA)
if btn_crear:
    if nombre and objeto and funcion:
        with st.spinner('🤖 PROCESANDO...'):
            try:
                # PROMPT ULTRA-ESTRICTO (CONCEPTO TECNOLÓGICO)
                consigna = (
                    f"ERES UNA MÁQUINA DE ADIVINANZAS PARA NIÑOS DE 6 AÑOS. "
                    f"DATOS RECIBIDOS -> NOMBRE: {nombre}, OBJETO: {objeto}, FUNCIÓN: {funcion}. "
                    f"REGLA 1: SI LA FUNCIÓN ES NATURAL O NO CREADA POR EL HOMBRE (EJ: CRECER, VOLAR CON ALAS, LLOVER, NADAR COMO PEZ), RESPONDE EXACTAMENTE: ¿ESTÁS SEGURO DE QUE ES UN PRODUCTO TECNOLÓGICO? VUELVE A INTENTARLO. "
                    f"REGLA 2: SI EL OBJETO Y LA FUNCIÓN NO TIENEN NINGUNA RELACIÓN LÓGICA, RESPONDE: NO ENTIENDO LA RELACIÓN ENTRE {objeto} Y {funcion}. REVISA TUS RESPUESTAS. "
                    f"REGLA 3: SI ES CORRECTO, ESCRIBE **SÓLO** UNA ADIVINANZA DE 4 VERSOS BREVES EN MAYÚSCULAS CON TILDES. TERMINA CON ¿QUÉ SOY? "
                    f"PROHIBIDO: EXPLICAR, SALUDAR O DAR CUALQUIER TEXTO QUE NO SEA LA ADIVINANZA."
                )
                
                res = model.generate_content(consigna)
                respuesta_ia = res.text.upper().strip()
                
                # Verificamos si es una adivinanza o una advertencia
                if "¿QUÉ SOY?" in respuesta_ia:
                    st.code(respuesta_ia, language=None)
                    guardar_en_excel(nombre, objeto, funcion, respuesta_ia)
                else:
                    st.markdown(f'<p style="font-size:22px; font-weight:bold; color:#d9534f;">🤖 {respuesta_ia}</p>', unsafe_allow_html=True)
            except Exception as e:
                st.error("Hubo un error con la IA. Intenta de nuevo.")
    else:
        st.warning("POR FAVOR, COMPLETA TODOS LOS CAMPOS.")
