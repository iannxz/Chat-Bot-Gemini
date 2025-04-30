import streamlit as st
from gemini_utils import GeminiChat
import time
from streamlit.components.v1 import html

# Configuração da página
st.set_page_config(
    page_title="Chatbot IA • Gemini",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS Customizado - Tema escuro
def load_css():
    st.markdown("""
    <style>
    /* Fundo escuro com gradiente */
    .stApp {
        background: linear-gradient(135deg, #1c1c1c 0%, #2c3e50 100%);
        color: #f5f5f5;
        font-family: 'Arial', sans-serif;
    }

    /* Cabeçalho */
    .css-1v3fvcr {
        color: #f5f5f5;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* Mensagens do chat */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 12px 16px !important;
        margin: 8px 0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    }

    /* Mensagem do usuário */
    [data-testid="stChatMessage-user"] {
        background-color: #4a8cff !important;
        color: white !important;
    }

    /* Mensagem do bot */
    [data-testid="stChatMessage-assistant"] {
        background-color: #2c2f33 !important;
        color: #f0f0f0 !important;
        border: 1px solid #3a3f47 !important;
    }

    /* Botão estilizado */
    .stButton>button {
        background: linear-gradient(to right, #4776E6, #8E54E9) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.3) !important;
    }

    /* Input do chat */
    .stChatInput {
        border-radius: 20px !important;
        padding: 12px !important;
        background-color: #1e1e1e !important;
        color: white !important;
    }

    .stTextInput>div>input {
        background-color: #1e1e1e !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Inicialização do chat
if 'chat' not in st.session_state:
    try:
        st.session_state.chat = GeminiChat()
        st.session_state.messages = []
        st.toast('Chat iniciado!', icon='🤖')
    except Exception as e:
        st.error(f"Falha ao iniciar: {str(e)}")
        st.stop()

# Sidebar
with st.sidebar:
    st.title("⚙️ Controle")
    st.markdown("---")
    
    if st.button("🔄 Novo Chat", use_container_width=True):
        st.session_state.chat.start_new_chat()
        st.session_state.messages = []
        st.rerun()
        st.toast('Novo chat criado!', icon='🔄')
    
    st.markdown("---")
    st.write(f"**Modelo:** {st.session_state.chat.model_name}")
    st.write(f"**Mensagens:** {len(st.session_state.messages)//2}")
    st.markdown("---")
    st.caption("Desenvolvido com Streamlit e Gemini API")

# Área principal
st.title("💬 Chatbot Inteligente")
st.caption("Converse com um assistente IA usando Gemini Pro")

# Efeito de digitação
def typing_effect(text):
    placeholder = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text + "▌")
        time.sleep(0.02)
    placeholder.markdown(displayed_text)

# Exibir histórico
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and i == len(st.session_state.messages)-1:
            typing_effect(message["content"])
        else:
            st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.spinner("Pensando..."):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        except Exception as e:
            st.error(f"Erro: {str(e)}")