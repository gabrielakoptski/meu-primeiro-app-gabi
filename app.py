import streamlit as st
from gabi_ia_completa import GabiIA
import datetime

# Configuração da página
st.set_page_config(
    page_title="Gabi - Apoio à Recuperação",
    page_icon="🕊️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS personalizado para tema acolhedor
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stTextInput > div > div > input {
        background-color: white;
        border-radius: 20px;
        border: 2px solid #4CAF50;
    }
    .stButton > button {
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .crisis-alert {
        background-color: #FFEBEE;
        border: 3px solid #F44336;
        padding: 1rem;
        border-radius: 10px;
        color: #C62828;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Inicializa a Gabi
@st.cache_resource
def get_gabi():
    return GabiIA()

gabi = get_gabi()

# Sidebar com informações
with st.sidebar:
    st.title("🕊️ Gabi")
    st.markdown("*Apoio à Recuperação*")
    st.markdown("---")
    st.markdown("**Inspirada em:**")
    st.markdown("Gabriella Bogo")
    st.markdown("[@umaadictagabi](https://instagram.com/umaadictagabi)")
    st.markdown("---")
    st.markdown("🆘 **Emergência:**")
    st.markdown("📞 **188** - CVV")
    st.markdown("📞 **192** - SAMU")
    st.markdown("---")
    st.markdown("⚠️ *Esta IA é ferramenta de apoio.*")
    st.markdown("*Não substitui tratamento profissional.*")

# Área principal
st.title("🕊️ Gabi - Sua Companheira de Recuperação")
st.markdown("*Inspirada na história de Gabriella Bogo - 3 anos limpa*")
st.markdown("---")

# Inicializa histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Mensagem inicial da Gabi
    initial_response = gabi.get_response("Olá", "Usuário")
    st.session_state.messages.append({
        "role": "assistant", 
        "content": initial_response['response'],
        "alert_level": "NORMAL"
    })

# Input do usuário
user_input = st.chat_input("Como posso te ajudar hoje?")

if user_input:
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Obtém resposta da Gabi
    with st.spinner("Gabi está digitando..."):
        response = gabi.get_response(user_input)
    
    # Adiciona resposta da Gabi
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response['response'],
        "alert_level": response.get('alert_level', 'NORMAL'),
        "type": response.get('type', 'general')
    })
    
    # Se for crise, mostra alerta especial
    if response.get('alert_level') == 'HIGH':
        st.error("🚨 ATENÇÃO: Sinais de crise detectados. Direcionamento emergencial ativado.")

# Exibe histórico de conversa
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🕊️"):
            # Se for crise, destaca visualmente
            if message.get('alert_level') == 'HIGH':
                st.markdown(f'<div class="crisis-alert">{message["content"]}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(message["content"])

# Botões de ação rápida
st.markdown("---")
st.markdown("**⚡ Ações Rápidas:**")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🌊 Craving"):
        st.session_state.messages.append({
            "role": "user", 
            "content": "Estou com vontade de usar"
        })
        response = gabi.get_response("Estou com vontade de usar")
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response['response'],
            "type": "craving"
        })
        st.rerun()

with col2:
    if st.button("🧘 Ansiedade"):
        st.session_state.messages.append({
            "role": "user", 
            "content": "Estou ansioso"
        })
        response = gabi.get_response("Estou ansioso")
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response['response'],
            "type": "ansiedade"
        })
        st.rerun()

with col3:
    if st.button("😔 Culpa"):
        st.session_state.messages.append({
            "role": "user", 
            "content": "Me sinto culpado"
        })
        response = gabi.get_response("Me sinto culpado")
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response['response'],
            "type": "culpa"
        })
        st.rerun()

with col4:
    if st.button("📓 Diário"):
        st.session_state.messages.append({
            "role": "user", 
            "content": "Quero fazer meu check-in"
        })
        response = gabi.get_response("Quero fazer meu check-in")
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response['response'],
            "type": "diary"
        })
        st.rerun()

# Cartão de emergência (expansível)
with st.expander("🆘 Cartão de Emergência (clique para ver)"):
# 
    st.markdown("**Salve este número no seu celular:** 📞 **188** (CVV)")

# Recursos adicionais
with st.expander("📚 Recursos de Recuperação"):
    st.markdown(gabi.get_resources_guide())
