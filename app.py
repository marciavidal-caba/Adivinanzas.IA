import streamlit as st
import google.generativeai as genai

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
        padding: 10px;
    }}
    div[data-testid="stCodeBlock"] code {{
        color: #000000 !important;
        font-size: 24px !important; 
        font-weight: 800 !important; 
    }}
    div.stButton > button {{
        border-radius: 20px !important;
        font-weight: bold !important;
        padding: 5px 15px !important; 
        font-size: 14px !important;
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
        padding: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN CON LA LLAVE
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

def borrar_todo():
    st.session_state["objeto"] = ""
    st.session_state["funcion"] = ""

# 4. INTERFAZ DE USUARIO
st.markdown('<p class="titulo-machine">🤖 TECNO ADIVINANZAS MACHINE ✨</p>', unsafe_allow_html=True)
st.write("ESCRIBE EL OBJETO Y SU FUNCIÓN. ¡LA MÁQUINA CREARÁ TU ADIVINANZA!")

objeto = st.text_input("1. ¿QUÉ PRODUCTO ES?", key="objeto", autocomplete="off")
funcion = st.text_input("2. ¿PARA QUÉ SIRVE?", key="funcion", autocomplete="off")

col1, col2 = st.columns([2, 1])
with col1:
    btn_crear = st.button("✏️ CREA TU ADIVINANZA")
with col2:
    st.button("🗑️ BORRAR", on_click=borrar_todo)

# 5. LÓGICA CON FILTRO TECNOLÓGICO (ESTRUCTURA CORREGIDA)
if btn_crear:
    if objeto and funcion:
        if model:
            with st.spinner('🤖 ANALIZANDO...'):
                try:
                    # Unimos la consigna en una sola línea para evitar errores de sintaxis
                    consigna = (
                        f"ACTÚA COMO UN MAESTRO DE TECNOLOGÍA. EL NIÑO ESCRIBIÓ: '{objeto}' Y '{funcion}'. "
                        f"REGLA 1: SI EL OBJETO ES NATURAL (PIEDRA, NUBE, ARCOIRIS), RESPONDE: '¿ESTÁS SEGURO QUE ES UN PRODUCTO TECNOLÓGICO? VUELVE A INTENTARLO.' "
                        f"REGLA 2: SI ES UN PRODUCTO DEL CAMPO (MANZANA, LECHE), MENCIONA SU FUNCIÓN Y QUE FUE CULTIVADO O COMPRADO. "
                        f"REGLA 3: SI ES UN SERVICIO (LAVADO, CORTE), ENFÓCATE EN LA TÉCNICA. "
                        f"REGLA 4: SI ESTÁ BIEN, CREA UNA ADIVINANZA DE 4 VERSOS: V1-V2 FUNCIÓN, V3-V4 FORMA O PROCESO. "
                        f"TODO EN MAYÚSCULAS Y TERMINA CON '¿QUÉ SOY?'."
                    )
                    
                    resultado = model.generate_content(consigna)
                    respuesta = resultado.text.upper().strip()
                    
                    if "¿QUÉ SOY?" in respuesta or "¿QUE SOY?" in respuesta:
                        st.markdown('<p class="adivinanza-subtitulo">📝 TU ADIVINANZA:</p>', unsafe_allow_html=True)
                        st.code(respuesta, language=None)
                    else:
                        st.markdown(f'<p class="mensaje-robot">🤖 {respuesta}</p>', unsafe_allow_html=True)
                except Exception as e:
                    if "429" in str(e):
                        st.error("🤖 CUPO AGOTADO. REINTENTA MAÑANA.")
                    else:
                        st.error(f"ERROR: {e}")
        else:
            st.error("NO SE ENCONTRÓ MOTOR DE IA.")
    else:
        st.warning("POR FAVOR, COMPLETA LOS DOS CUADRITOS.")
