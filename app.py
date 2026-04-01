import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PESTAÑA Y PÁGINA
st.set_page_config(page_title="TECNO ADIVINANZAS MACHINE", page_icon="🤖")

# --- ESTILO CSS PERSONALIZADO (NEGRO + NARANJA #ffc300) ---
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
        font-size: 22px !important; /* Letra más grande */
        font-weight: 800 !important; /* Más negrita */
    }}

    /* 5. BOTONES MÁS PEQUEÑOS Y REDONDEADOS */
    div.stButton > button {{
        border-radius: 20px !important;
        font-weight: bold !important;
        padding: 5px 15px !important; /* Padding reducido para menor tamaño */
        font-size: 14px !important;
        transition: all 0.3s ease;
    }}

    /* Botón principal */
    div.stButton > button:first-child {{
        background-color: #ffc300 !important;
        color: #000000 !important;
        border: 2px solid #ffc300 !important;
    }}

    /* Estilo para mensajes de validación del robot */
    .mensaje-robot {{
        font-size: 18px;
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

# 3. FUNCIÓN PARA BUSCAR EL MODELO
@st.cache_resource
def configurar_modelo():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
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
col1, col2 = st.columns([2, 1]) # Proporción para que los botones se vean mejor

with col1:
    btn_crear = st.button("✏️ CREA TU ADIVINANZA")

with col2:
    st.button("🗑️ BORRAR", on_click=borrar_todo)

# 6. LÓGICA DE GENERACIÓN
if btn_crear:
    if objeto and funcion:
        if model:
            with st.spinner('🤖 ANALIZANDO...'):
                try:
                    consigna = (
                        f"ACTÚA COMO UN MAESTRO DE PRIMER GRADO. "
                        f"EL NIÑO DICE QUE UN/A '{objeto}' SIRVE PARA '{funcion}'. "
                        f"REGLA 1: SI LA FUNCIÓN NO TIENE SENTIDO CON EL OBJETO, RESPONDE: "
                        f"'¿ESTÁS SEGURO QUE ESA ES LA FUNCIÓN? PIENSA UN POCO MÁS ¿PARA QUÉ SE USA EL/LA {objeto}?' "
                        f"REGLA 2: SI NO SE ENTIENDE, RESPONDE: '¡UPS! NO ENTENDÍ, PUEDES ESCRIBIR DE NUEVO.' "
                        f"REGLA 3: SI TODO ESTÁ BIEN, CREA UNA ADIVINANZA CORTA DE 4 VERSOS (FUNCIÓN PRIMERO, FORMA DESPUÉS). "
                        f"TODO EN MAYÚSCULAS. RESPONDE SOLO EL TEXTO SOLICITADO."
                    )
                    
                    resultado = model.generate_content(consigna)
                    respuesta = resultado.text.upper()
                    
                    # Eliminamos la línea divisoria (---)
                    
                    if "¿QUÉ SOY?" in respuesta or "¿QUE SOY?" in respuesta:
                        st.markdown('<p class="adivinanza-subtitulo">📝 TU ADIVINANZA:</p>', unsafe_allow_html=True)
                        st.code(respuesta, language=None)
                    else:
                        # Mensaje del robot más amigable y legible
                        st.markdown(f'<p class="mensaje-robot">🤖 {respuesta}</p>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"ERROR: {e}")
        else:
            st.error("NO SE ENCONTRÓ MODELO.")
    else:
        st.warning("COMPLETA LOS DOS CUADROS.")
