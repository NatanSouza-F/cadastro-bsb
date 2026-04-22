import streamlit as st
import time
from datetime import datetime

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURAÇÃO DA PÁGINA E UX/UI GLOBAL                                ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.set_page_config(page_title="BSB Contabilidade | Onboarding", page_icon="🏢", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #f8fafc; }

    /* Estilizando para parecer um app moderno */
    .main-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 2.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }
    h1 { color: #0f172a; text-align: center; font-weight: 800; font-size: 2.2rem; padding-bottom: 0; }
    .subtitle { color: #64748b; text-align: center; font-size: 1rem; margin-bottom: 2rem; }
    h3 { color: #0284c7 !important; font-size: 1.1rem !important; font-weight: 600 !important; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-top: 1rem; margin-bottom: 1rem; }
    
    /* Botões */
    div[data-testid="stButton"] button {
        background-color: #0284c7; color: white; font-weight: 600; border: none; border-radius: 6px; padding: 0.75rem 2rem; width: 100%; transition: all 0.2s ease; margin-top: 15px;
    }
    div[data-testid="stButton"] button:hover { background-color: #0369a1; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3); color: white; }
</style>
""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  GERENCIAMENTO DE ESTADO E CALLBACKS (A BLINDAGEM)                    ║
# ╚═══════════════════════════════════════════════════════════════════════╝
# Inicializa as variáveis se não existirem
if 'cadastro_realizado' not in st.session_state:
    st.session_state.cadastro_realizado = False
if 'dados_cliente' not in st.session_state:
    st.session_state.dados_cliente = {}
if 'erro_validacao' not in st.session_state:
    st.session_state.erro_validacao = False

# Callback: Roda ANTES da interface ser redesenhada
def processar_envio():
    # Puxa os dados direto das keys dos inputs
    cnpj = st.session_state.in_cnpj
    razao = st.session_state.in_razao
    regime = st.session_state.in_regime
    faturamento = st.session_state.in_fat
    erp = st.session_state.in_erp

    if not cnpj or not razao or regime == "Selecione..." or faturamento == "Selecione...":
        st.session_state.erro_validacao = True
    else:
        st.session_state.erro_validacao = False
        time.sleep(1.5) # Simula o processamento
        st.session_state.dados_cliente = {
            "cnpj": cnpj,
            "razao": razao,
            "faturamento": faturamento,
            "erp": erp,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        st.session_state.cadastro_realizado = True

# Callback: Reseta a tela
def resetar_tela():
    st.session_state.cadastro_realizado = False
    st.session_state.dados_cliente = {}
    st.session_state.erro_validacao = False

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  INTERFACE VISUAL                                                     ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.markdown("<h1>BSB Contabilidade</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Digital Onboarding - BPO Financeiro</div>", unsafe_allow_html=True)

# Envolvemos tudo numa div com classe CSS para ficar bonito
st.markdown('<div class="main-card">', unsafe_allow_html=True)

if not st.session_state.cadastro_realizado:
    st.markdown("<h3>1. Dados da Empresa</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.text_input("CNPJ *", placeholder="00.000.000/0000-00", key="in_cnpj")
    with col2:
        st.text_input("Razão Social *", placeholder="Sua Empresa LTDA", key="in_razao")
        
    col3, col4 = st.columns(2)
    with col3:
        st.text_input("WhatsApp do Gestor", placeholder="(00
