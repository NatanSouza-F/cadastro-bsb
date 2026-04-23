import streamlit as st
import time
import requests
import re
from datetime import datetime

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURAÇÃO DA PÁGINA E UX/UI GLOBAL (PADRÃO BSB AZUL PREMIUM)      ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.set_page_config(page_title="BSB Contabilidade | Onboarding", page_icon="🏢", layout="centered")

# CSS NASA: Glassmorphism, Micro-interações, Acessibilidade e LGPD
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    .stApp {
        background: radial-gradient(ellipse at top, rgba(56, 189, 248, 0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom, rgba(37, 99, 235, 0.05) 0%, transparent 50%),
                    #0b1e2e;
    }
    header[data-testid="stHeader"] { background: transparent; height: 0; }
    .block-container { max-width: 580px !important; padding: 2rem 1rem !important; }
    
    .bsb-logo {
        font-size: 2.6rem; font-weight: 900;
        background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 50%, #2563eb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin: 0; letter-spacing: -0.04em;
        filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.2));
    }
    .bsb-slogan {
        text-align: center; color: #94a3b8 !important; font-size: 1.05rem;
        font-weight: 500; line-height: 1.5; margin-top: 12px; margin-bottom: 2rem;
    }

    h3 {
        display: inline-block; background: rgba(56, 189, 248, 0.1); color: #38bdf8 !important;
        padding: 10px 20px 10px 24px !important; border-radius: 8px; font-size: 0.85rem !important; font-weight: 800 !important;
        letter-spacing: 0.15em; text-transform: uppercase; border-left: 4px solid #38bdf8;
        margin-top: 1.5rem !important; margin-bottom: 1.2rem !important; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.05);
    }

    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-baseweb="number-input"] > div {
        background: rgba(11, 30, 46, 0.6) !important; backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.3) !important; border-radius: 10px !important; transition: all 0.3s ease;
    }
    
    input, select { color: #e2e8f0 !important; font-size: 0.9rem !important; }
    label { color: #94a3b8 !important; font-size: 0.72rem !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.08em; }

    div.stButton > button[kind="secondary"] {
        background: rgba(11, 30, 46, 0.8) !important; border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 16px !important; color: #f1f5f9 !important; width: 100% !important; height: 70px !important;
        font-weight: 700 !important; transition: all 0.3s ease !important;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: #ffffff !important; font-weight: 800; border: none; border-radius: 12px; padding: 0.8rem 2rem; width: 100%;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3); text-transform: uppercase; letter-spacing: 0.1em;
    }

    .lgpd-badge { display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 20px; color: #64748b; font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  LÓGICA DE NEGÓCIO E ESTADO                                           ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'cadastro_realizado' not in st.session_state: st.session_state.cadastro_realizado = False
if 'dados_cliente' not in st.session_state: st.session_state.dados_cliente = {}
if 'razao_social_api' not in st.session_state: st.session_state.razao_social_api = ""
if 'doc_method' not in st.session_state: st.session_state.doc_method = None
if 'endereco_api' not in st.session_state: st.session_state.endereco_api = {"logradouro": "", "bairro": "", "localidade": "", "uf": ""}

def buscar_cnpj():
    cnpj = re.sub(r'\D', '', st.session_state.in_cnpj)
    if len(cnpj) == 14:
        try:
            res = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}", timeout=5)
            if res.status_code == 200:
                d = res.json()
                st.session_state.razao_social_api = d.get("razao_social", "")
                st.toast("✅ Empresa validada!")
        except: pass
    st.session_state.etapa = 2

def buscar_cep(key_cep):
    cep = re.sub(r'\D', '', st.session_state[key_cep])
    if len(cep) == 8:
        try:
            res = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
            if res.status_code == 200:
                st.session_state.endereco_api = res.json()
                st.toast("📍 Endereço localizado!")
        except: pass

def finalizar(perfil):
    st.session_state.dados_cliente = {
        "perfil": perfil, 
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"), 
        "endereco": st.session_state.endereco_api
    }
    st.session_state.cadastro_realizado = True

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  INTERFACE VISUAL                                                     ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.markdown('<h1 class="bsb-logo">BSB Contabilidade</h1>', unsafe_allow_html=True)
st.markdown('<p class="bsb-slogan">Seja bem-vindo(a)! Para darmos continuidade ao seu processo, solicitamos o preenchimento das informações a seguir:</p>', unsafe_allow_html=True)

if not st.session_state.cadastro_realizado:
    st.markdown("<h3>1. Perfil de Atendimento</h3>", unsafe_allow_html=True)
    perfil = st.radio("", ["🏢 Pessoa Jurídica (Empresa)", "👤 Pessoa Física (Individual)"], horizontal=True, label_visibility="collapsed")

    if "Jurídica" in perfil:
        col_c, col_b = st.columns([3, 1])
        with col_c: st.text_input("CNPJ da Empresa *", key="in_cnpj", placeholder="00.000.000/0000-00")
        with col_b: st.button("🔍 Validar", on_click=buscar_cnpj, use_container_width=True)

        if st.session_state.etapa == 2:
            st.markdown("<h3>2. Dados da Empresa</h3>", unsafe_allow_html=True)
            st.text_input("Razão Social *", value=st.session_state.razao_social_api, key="in_razao")
            col_w, col_e = st.columns(2)
            with col_w: st.text_input("WhatsApp do Gestor *", key="in_wpp")
            with col_e: st.text_input("E-mail Comercial *", key="in_email")
            
            st.markdown("<h3>3. Localização</h3>", unsafe_allow_html=True)
            st.text_input("CEP Sede *", key="in_cep_pj", on_change=buscar_cep, args=("in_cep_pj",), placeholder="00000-000")
            if st.session_state.endereco_api.get("logradouro"):
                st.info(f"📍 {st.session_state.endereco_api['logradouro']}, {st.session_state.endereco_api['bairro']} - {st.session_state.endereco_api['localidade']}/{st.session_state.endereco_api['uf']}")

            st.markdown("<h3>4. Operacional</h3>", unsafe_allow_html=True)
            st.selectbox("Faturamento Médio Mensal *", ["Até R$ 20k", "R$ 20k a R$ 100k", "Acima de R$ 100k"], key="in_fat")
            st.button("Finalizar Cadastro de Empresa", type="primary", on_click=finalizar, args=("PJ",))
    else:
        col_cpf, col_n = st.columns([1, 2])
        with col_cpf: st.text_input("CPF *", key="in_cpf")
        with col_n: st.text_input("Nome Completo *", key="in_nome_pf")
        
        st.markdown("<h3>2. Endereço e Contato</h3>", unsafe_allow_html=True)
        st.text_input("CEP Residencial *", key="in_cep_pf", on_change=buscar_cep, args=("in_cep_pf",))
        col_w2, col_e2 = st.columns(2)
        with col_w2: st.text_input("WhatsApp *", key="in_wpp_pf")
        with col_e2: st.text_input("E-mail *", key="in_email_pf")

        st.markdown("<h3>3. Identificação (KYC)</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.button("👤 Anexar Documento", on_click=lambda: st.session_state.update({"doc_method": "Anexar"}), type="secondary", use_container_width=True)
        with c2: st.button("📸 Tirar Foto Agora", on_click=lambda: st.session_state.update({"doc_method": "Foto"}), type="secondary", use_container_width=True)

        if st.session_state.doc_method == "Anexar": st.file_uploader("Upload RG/CNH", type=['pdf','png','jpg'])
        if st.session_state.doc_method == "Foto": st.camera_input("Capturar Documento")

        st.button("Finalizar Cadastro Pessoa Física", type="primary", on_click=finalizar, args=("PF",))

    st.markdown('<div class="lgpd-badge">🔒 Ambiente seguro de acordo com a LGPD</div>', unsafe_allow_html=True)

else:
    st.balloons()
    st.success("✅ Cadastro Finalizado! Recebemos suas informações.")
    with st.expander("🔒 ÁREA DO CONSULTOR (Visão de Dados)"):
        st.json(st.session_state.dados_cliente)
