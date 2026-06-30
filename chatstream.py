import streamlit as st
import google.generativeai as genai
import os


# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="AI Premium Chat | Mentor de Código", page_icon="✨", layout="centered")

# --- RECURSOS Y CONFIGURACIÓN ---
USER_AVATAR_FILE = "user_avatar.png"
ASSISTANT_AVATAR_FILE = "assistant_avatar.png"
MODEL_NAME = 'gemini-3.1-flash-lite'

USER_AVATAR = USER_AVATAR_FILE if os.path.exists(USER_AVATAR_FILE) else "👤"
ASSISTANT_AVATAR = ASSISTANT_AVATAR_FILE if os.path.exists(ASSISTANT_AVATAR_FILE) else "🤖"

# Prompt de sistema para definir la personalidad del bot
SYSTEM_PROMPT = """
Eres un mentor de programación profesional. Proporciona ejemplos de código claros, 
concisos y bien documentados. Prefiere Python, JavaScript y shell scripts. 
Mantén un tono elegante, sofisticado y servicial.
"""

# --- CONFIGURACIÓN SEGURA DEL MODELO ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_PROMPT)
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

st.markdown(f"""
    <style>
    /* Fondo y Base */
    .stApp {{
        background-color: #0e1117;
        color: #ffffff;
    }}
    
    /* Estilo de los Mensajes de Chat */
    [data-testid="stChatMessage"] {{
        background-color: transparent !important;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }}

    /* Burbuja del Usuario (Gradiente Púrpura a Azul) */
    [data-testid="stChatMessageUser"] > div:nth-child(2) {{
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%) !important;
        border-radius: 20px 20px 5px 20px !important;
        padding: 15px !important;
        border: none !important;
        color: white !important;
    }}

    /* Burbuja del Asistente (Glassmorphism) */
    [data-testid="stChatMessageAssistant"] > div:nth-child(2) {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px 20px 20px 5px !important;
        padding: 15px !important;
    }}

    /* Animación suave al aparecer */
    [data-testid="stChatMessage"] {{
        animation: fadeIn 0.6s ease;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- INTERFAZ DE USUARIO ---
with st.sidebar:
    st.title("✨ AI Premium")
    st.caption(f"Modelo: {MODEL_NAME}")
    st.markdown("Mentor de Programación Profesional.")
    st.markdown("---")
    if st.button("Limpiar Chat", icon="🔄"):
        st.session_state.messages = []
        st.rerun()

st.title("AI Premium Chat")
st.caption("✨ Mentor de Código Responsivo | Identidad Visual Optimizada")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con avatares integrados
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else ASSISTANT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- MANEJO DE ENTRADA ---
if prompt := st.chat_input("Pregunta a tu mentor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Hubo un error al conectar con la IA. Revisa tu conexión o clave API.")
