import streamlit as st
import time
import requests
import re
from datetime import datetime

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURAÇÃO DA PÁGINA E UX/UI GLOBAL                                ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.set_page_config(page_title="BSB Contabilidade | Onboarding Corporativo", page_icon="🏢", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp {
        background: radial-gradient(ellipse at top, rgba(56, 189, 248, 0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom, rgba(37, 99, 235, 0.05) 0%, transparent 50%),
                    #0b1e2e;
    }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 600px !important; padding-top: 2rem !important; }
    
    .bsb-logo {
        font-size: 2.6rem; font-weight: 900;
        background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 50%, #2563eb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 0; letter-spacing: -0.04em;
    }
    .bsb-slogan {
        text-align: center; color: #94a3b8 !important; font-size: 1rem;
        font-weight: 500; margin-bottom: 2rem;
    }

    h3 {
        display: inline-block; background: rgba(56, 189, 248, 0.1); color: #38bdf8 !important;
        padding: 8px 20px; border-radius: 8px; font-size: 0.8rem !important; font-weight: 800 !important;
        letter-spacing: 0.1em; text-transform: uppercase; border-left: 4px solid #38bdf8;
        margin-top: 2rem !important; margin-bottom: 1rem !important;
    }

    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, div[data-baseweb="number-input"] > div {
        background: rgba(11, 30, 46, 0.6) !important; border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important; color: #e2e8f0 !important;
    }
    
    label { color: #94a3b8 !important; font-size: 0.7rem !important; font-weight: 700 !important; text-transform: uppercase; }

    .lgpd-badge { display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 30px; color: #64748b; font-size: 0.7rem; }
</style>
""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  LÓGICA DE APIs E ESTADO                                              ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'cadastro_realizado' not in st.session_state: st.session_state.cadastro_realizado = False
if 'razao_social_api' not in st.session_state: st.session_state.razao_social_api = ""
if 'endereco_api' not in st.session_state: st.session_state.endereco_api = {"logradouro": "", "bairro": "", "localidade": "", "uf": ""}

def buscar_cnpj():
    cnpj = re.sub(r'\D', '', st.session_state.in_cnpj)
    if len(cnpj) == 14:
        try:
            res = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}", timeout=5)
            if res.status_code == 200:
                d = res.json()
                st.session_state.razao_social_api = d.get("razao_social", "")
                st.toast("✅ Dados da Receita Federal importados!")
        except: pass
    st.session_state.etapa = 2

def buscar_cep(key_cep):
    cep = re.sub(r'\D', '', st.session_state[key_cep])
    if len(cep) == 8:
        try:
            res = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
            if res.status_code == 200:
                st.session_state.endereco_api = res.json()
                st.toast("📍 Localização identificada!")
        except: pass

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CABECALHO                                                            ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.markdown('<h1 class="bsb-logo">BSB Contabilidade</h1>', unsafe_allow_html=True)
st.markdown('<p class="bsb-slogan">KYC & Onboarding: Ficha Cadastral de Alta Precisão</p>', unsafe_allow_html=True)

if not st.session_state.cadastro_realizado:
    st.markdown("<h3>1. Perfil do Solicitante</h3>", unsafe_allow_html=True)
    perfil = st.radio("", ["🏢 Pessoa Jurídica (Corporate)", "👤 Pessoa Física (Private)"], horizontal=True, label_visibility="collapsed")

    # ================= FLUXO CORPORATE (PJ) =================
    if "Jurídica" in perfil:
        col_c, col_b = st.columns([3, 1])
        with col_c: st.text_input("CNPJ Principal *", key="in_cnpj", placeholder="00.000.000/0000-00")
        with col_b: st.button("🔍 Consultar", on_click=buscar_cnpj, use_container_width=True)

        if st.session_state.etapa == 2:
            st.markdown("<h3>2. Dados da Instituição</h3>", unsafe_allow_html=True)
            st.text_input("Razão Social (Receita Federal) *", value=st.session_state.razao_social_api, key="in_razao")
            col_fan, col_cnae = st.columns(2)
            with col_fan: st.text_input("Nome Fantasia", key="in_fantasia")
            with col_cnae: st.text_input("CNAE Principal", placeholder="Ex: 6201-5/00", key="in_cnae")
            
            st.markdown("<h3>3. Localização e Infraestrutura</h3>", unsafe_allow_html=True)
            st.text_input("CEP Sede *", key="in_cep_pj", on_change=buscar_cep, args=("in_cep_pj",))
            st.selectbox("Tipo de Sede", ["Alugada", "Própria", "Sede Virtual / Coworking", "Residencial"], key="in_tipo_sede")
            
            st.markdown("<h3>4. Análise de Risco & Saúde Financeira</h3>", unsafe_allow_html=True)
            col_fat, col_div = st.columns(2)
            with col_fat: st.selectbox("Faturamento Médio Anual", ["Até R$ 250k", "R$ 250k a R$ 1.2M", "R$ 1.2M a R$ 4.8M", "Acima de R$ 4.8M"], key="in_fat_pj")
            with col_div: st.selectbox("Possui Dívidas Fiscais?", ["Não possui", "Sim (Até R$ 50k)", "Sim (Acima de R$ 50k)", "Em fase de execução"], key="in_divida")
            
            st.markdown("<h3>5. Quadro Societário (Assinante)</h3>", unsafe_allow_html=True)
            st.text_input("Nome do Sócio Responsável *", key="in_socio")
            st.text_input("CPF do Sócio *", key="in_socio_cpf")
            
            st.button("Finalizar Cadastro Corporativo", type="primary", use_container_width=True)

    # ================= FLUXO PRIVATE (PF) =================
    else:
        col_cpf, col_n = st.columns([1, 2])
        with col_cpf: st.text_input("CPF do Titular *", key="in_cpf")
        with col_n: st.text_input("Nome Completo *", key="in_nome_pf")
        
        if st.session_state.etapa == 1:
            st.button("Próxima Etapa", on_click=lambda: st.session_state.update({"etapa": 2}), use_container_width=True)

        if st.session_state.etapa == 2:
            st.markdown("<h3>2. Perfil Patrimonial & Rendimentos</h3>", unsafe_allow_html=True)
            col_renda, col_origem = st.columns(2)
            with col_renda: st.selectbox("Renda Mensal Comprovada", ["Até R$ 5k", "R$ 5k a R$ 15k", "R$ 15k a R$ 50k", "Acima de R$ 50k"], key="in_renda_pf")
            with col_origem: st.multiselect("Origem de Renda", ["CLT", "Pró-Labore", "Dividendos", "Aluguéis", "Renda Variável"], key="in_origem")
            
            col_bens, col_invest = st.columns(2)
            with col_bens: st.selectbox("Patrimônio Total Estimado", ["Até R$ 100k", "R$ 100k a R$ 500k", "R$ 500k a R$ 2M", "Acima de R$ 2M"], key="in_patrimonio")
            with col_invest: st.checkbox("📈 Investidor Bolsa/Cripto", key="in_investidor")

            st.markdown("<h3>3. Localização & Contato</h3>", unsafe_allow_html=True)
            st.text_input("CEP Residencial *", key="in_cep_pf", on_change=buscar_cep, args=("in_cep_pf",))
            col_w, col_e = st.columns(2)
            with col_w: st.text_input("WhatsApp", key="in_wpp_pf")
            with col_e: st.text_input("E-mail Principal", key="in_email_pf")

            st.markdown("<h3>4. Verificação de Identidade (KYC)</h3>", unsafe_allow_html=True)
            metodo = st.radio("Selecione o método de envio do documento:", ["📸 Tirar Foto Agora (Frente e Verso)", "👤 Anexar Arquivo Digital (PDF/IMG)"], horizontal=True)
            
            if "Foto" in metodo:
                st.camera_input("Frente do Documento (RG/CNH)")
                st.camera_input("Verso do Documento")
            else:
                st.file_uploader("Upload do Documento de Identificação", type=['pdf','png','jpg'])

            st.markdown("<h3>5. Compliance</h3>", unsafe_allow_html=True)
            st.selectbox("É uma Pessoa Politicamente Exposta (PEP)?", ["Não", "Sim"], help="Se você ou familiares próximos exercem cargos públicos relevantes.")
            
            st.button("Finalizar Cadastro de Alta Renda", type="primary", use_container_width=True)

    st.markdown('<div class="lgpd-badge">🔒 Criptografia SSL 256-bits | Em conformidade com a LGPD</div>', unsafe_allow_html=True)

else:
    st.balloons()
    st.success("✅ Ficha Cadastral enviada com sucesso para análise de comitê.")
    st.info("Nossa equipe de Onboarding entrará em contato em até 4 horas úteis.")
    st.button("Iniciar Novo Cadastro", on_click=lambda: st.session_state.clear())
