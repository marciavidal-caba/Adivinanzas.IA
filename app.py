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
    
    /* 2. Estilo para el Título (Grande, Negro, Centrado) */
    .titulo-machine {{
        font-size: 28px !important;
        font-weight: bold;
        text-align: center;
        color: #000000 !important;
        margin-bottom: 25px;
        white-space: nowrap;
    }}

    /* 3. Estilo para el Subtítulo de la adivinanza (Negro y Grande) */
    .adivinanza-subtitulo {{
        color: #000000 !important;
        font-size: 20px;
        font-weight: bold;
        margin-top: 15px;
    }}

    /* 4. Estilo MINIMALISTA INFANTIL para el recuadro de la adivinanza (st.code) */
    div[data-testid="stCodeBlock"] {{
        border: 4px solid #ffc300; /* Borde Naranja Amarillento */
        border-radius: 20px;      /* Bordes muy redondeados */
        background-color: #f9f9f9; /* Fondo gris muy clarito */
        padding: 15px;
    }}
    /* Asegura que el texto DENTRO de la adivinanza sea Negro y Grande */
    div[data-testid="stCodeBlock"] code {{
        color: #000000 !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }}

    /* 5. Estilo para el BOTÓN PRINCIPAL (Fondo Naranja, Texto Negro, Redondeado) */
    div.stButton > button:first-child {{
        background-color: #ffc300 !important; /* Fondo Naranja */
        color: #000000 !important;            /* Texto Negro */
        border-radius: 25px !important;      /* Muy redondeado */
        border: 2px solid #ffc300 !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease;
    }}
    /* Efecto al pasar el mouse por el botón */
    div.stButton > button:first-child:hover {{
        background-color: #e6b000 !important; /* Naranja un poco más oscuro */
        border-color: #e6b000 !important;
        transform: scale(1.03); /* Se agranda un poquito */
    }}

    /* 6. Estilo para el BOTÓN BORRAR (Gris, Texto Negro, Redondeado) */
    div.stButton > button[data-testid="baseButton-secondary"] {{
        border-radius: 25px !important;
        color: #000000 !important;
        border: 2px solid #cccccc !important;
        background-color: #ffffff !important;
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
st.markdown('<p class="titulo-machine">🤖TECNO ADIVINANZAS MACHINE✨</p>', unsafe_allow_html=True)
st.write("ESCRIBE EL OBJETO Y SU FUNCIÓN. ¡LA MÁQUINA CREARÁ TU ADIVINANZA!")

# CUADROS DE TEXTO SIN HISTORIAL
objeto = st.text_input("1. ¿QUÉ PRODUCTO ES?", key="objeto", autocomplete="off")
funcion = st.text_input("2. ¿PARA QUÉ SIRVE?", key="funcion", autocomplete="off")

# FILA DE BOTONES
col1, col2 = st.columns(2)

with col1:
    btn_crear = st.button("✏️CREA TU ADIVINANZA")

with col2:
    st.button("🗑️BORRAR TODO", on_click=borrar_todo)

# 6. LÓGICA DE GENERACIÓN CON VALIDACIÓN Y NUEVO DISEÑO
if btn_crear:
    if objeto and funcion:
        if model:
            with st.spinner('🤖 EL ROBOT ESTÁ ANALIZANDO...'):
                try:
                    consigna = (
                        f"ACTÚA COMO UN MAESTRO DE PRIMER GRADO (NIÑOS DE 6 AÑOS). "
                        f"EL NIÑO DICE QUE UN/A '{objeto}' SIRVE PARA '{funcion}'. "
                        f"REGLA 1: SI LA FUNCIÓN NO TIENE NINGÚN SENTIDO CON EL OBJETO, RESPONDE EXACTAMENTE: "
                        f"'¿ESTÁS SEGURO QUE ESA ES LA FUNCIÓN? PIENSA UN POCO MÁS ¿PARA QUÉ SE USA EL/LA {objeto}?' "
                        f"REGLA 2: SI LO QUE ESCRIBIÓ NO SE ENTIENDE, RESPONDE: "
                        f"'¡UPS! NO ENTENDÍ, PUEDES ESCRIBIR DE NUEVO.' "
                        f"REGLA 3: SI TODO ESTÁ CORRECTO, CREA UNA ADIVINANZA CORTA DE 4 VERSOS: "
                        f"V1 Y V2 SOBRE LA FUNCIÓN, V3 Y V4 SOBRE LA FORMA O COLOR. "
                        f"TODO EL TEXTO EN MAYÚSCULAS. NO SALUDES."
                    )
                    
                    resultado = model.generate_content(consigna)
                    respuesta = resultado.text.upper()
                    
                    st.markdown("---")
                    
                    # SI ES UNA ADIVINANZA (TIENE PREGUNTA)
                    if "¿QUÉ SOY?" in respuesta or "¿QUE SOY?" in respuesta:
                        st.markdown('<p class="adivinanza-subtitulo">📝 TU ADIVINANZA:</p>', unsafe_allow_html=True)
                        # MOSTRAR EN EL RECUADRO CON BORDES REDONDEADOS Y BOTÓN DE COPIADO
                        st.code(respuesta, language=None)
                    else:
                        # SI ES UN MENSAJE DE VALIDACIÓN (TEXTO NEGRO)
                        st.markdown(f"{respuesta}")
                    
                except Exception as e:
                    st.error(f"HUBO UN ERROR TÉCNICO: {e}")
        else:
            st.error("NO SE ENCONTRÓ MODELO DE IA.")
    else:
        st.warning("POR FAVOR, COMPLETA LOS DOS CUADRITOS.")
