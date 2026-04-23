import streamlit as st
import time
import requests
import re
from datetime import datetime

# Importação para o PDF (Necessário instalar: pip install fpdf)
try:
    from fpdf import FPDF
except ImportError:
    st.error("Por favor, instale a biblioteca de PDF: pip install fpdf")

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURAÇÃO DA PÁGINA E UX/UI GLOBAL                                ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.set_page_config(page_title="BSB Contabilidade | Onboarding", page_icon="🏢", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp {
        background: radial-gradient(ellipse at top, rgba(56, 189, 248, 0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom, rgba(37, 99, 235, 0.05) 0%, transparent 50%),
                    #0b1e2e;
    }
    header[data-testid="stHeader"] { background: transparent; height: 0; }
    .block-container { max-width: 540px !important; padding: 3rem 1rem !important; }
    .bsb-logo {
        font-size: 2.6rem; font-weight: 900;
        background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 50%, #2563eb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin: 0; letter-spacing: -0.04em;
        filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.2));
    }
    .bsb-slogan { text-align: center; color: #94a3b8 !important; font-size: 1.05rem; margin-top: 12px; margin-bottom: 2rem; }

    /* CARROSSEL 3D */
    .carousel-wrapper { position: relative; width: 100%; height: 180px; margin-bottom: 40px; perspective: 1200px; overflow: hidden; }
    .carousel-track { position: relative; width: 100%; height: 100%; transform-style: preserve-3d; }
    .carousel-card {
        position: absolute; top: 0; left: 50%; width: 280px; height: 160px; margin-left: -140px;
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
        border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 20px; padding: 20px;
        box-shadow: 0 20px 40px rgba(56, 189, 248, 0.15);
        animation: carousel-slide 25s infinite ease-in-out; opacity: 0; display: flex; flex-direction: column; justify-content: center; text-align: center;
    }
    @keyframes carousel-slide {
        0% { opacity: 0; transform: translateX(100px) scale(0.9); }
        4% { opacity: 1; transform: translateX(0) scale(1); }
        16% { opacity: 1; transform: translateX(0) scale(1); }
        20% { opacity: 0; transform: translateX(-100px) scale(0.9); }
        100% { opacity: 0; transform: translateX(-100px) scale(0.9); }
    }
    .carousel-card:nth-child(1) { animation-delay: 0s; }
    .carousel-card:nth-child(2) { animation-delay: 5s; }
    .carousel-card:nth-child(3) { animation-delay: 10s; }

    /* INPUTS NASA */
    h3 {
        display: inline-block; background: rgba(56, 189, 248, 0.1); color: #38bdf8 !important;
        padding: 10px 20px 10px 24px !important; border-radius: 8px; font-size: 0.85rem !important; font-weight: 800 !important;
        letter-spacing: 0.15em; text-transform: uppercase; border-left: 4px solid #38bdf8;
        margin-top: 1.5rem !important; margin-bottom: 1.2rem !important;
    }
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background: rgba(11, 30, 46, 0.6) !important; backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.3) !important; border-radius: 10px !important; color: #e2e8f0 !important;
    }
    label { color: #94a3b8 !important; font-size: 0.72rem !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.08em; }

    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: #ffffff !important; font-weight: 800; border-radius: 12px; width: 100%; height: 50px; text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  MOTOR DE APIs E ESTADO                                               ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'cadastro_realizado' not in st.session_state: st.session_state.cadastro_realizado = False
if 'razao_api' not in st.session_state: st.session_state.razao_api = ""
if 'endereco_api' not in st.session_state: st.session_state.endereco_api = {"logradouro": "", "bairro": "", "localidade": "", "uf": ""}
if 'doc_method' not in st.session_state: st.session_state.doc_method = None

def buscar_cnpj():
    cnpj = re.sub(r'\D', '', st.session_state.in_cnpj)
    if len(cnpj) == 14:
        try:
            res = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}", timeout=5)
            if res.status_code == 200:
                st.session_state.razao_api = res.json().get("razao_social", "")
                st.toast("✅ Dados da Empresa Importados!")
        except: pass
    st.session_state.etapa = 2

def buscar_cep(key_cep):
    cep = re.sub(r'\D', '', st.session_state[key_cep])
    if len(cep) == 8:
        try:
            res = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5).json()
            if "erro" not in res:
                st.session_state.endereco_api = {
                    "rua": res.get("logradouro"),
                    "bairro": res.get("bairro"),
                    "cidade": res.get("localidade"),
                    "uf": res.get("uf")
                }
                st.toast("📍 Endereço Localizado!")
        except: pass

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "FICHA CADASTRAL BSB CONTABILIDADE", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    for k, v in dados.items():
        pdf.multi_cell(0, 8, f"{str(k).upper()}: {str(v)}")
    return pdf.output(dest='S').encode('latin-1')

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  INTERFACE PRINCIPAL                                                  ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.markdown('<h1 class="bsb-logo">BSB Contabilidade</h1>', unsafe_allow_html=True)

if not st.session_state.cadastro_realizado:
    st.markdown('<p class="bsb-slogan">Seja bem-vindo(a)! Para darmos continuidade ao seu processo, solicitamos o preenchimento a seguir:</p>', unsafe_allow_html=True)
    
    # CARROSSEL
    st.markdown("""
    <div class="carousel-wrapper">
        <div class="carousel-track">
            <div class="carousel-card"><div style="font-size:2rem;">🛡️</div><b style="color:#38bdf8">SOCIETÁRIO</b><br><small>Abertura e Alteração com precisão.</small></div>
            <div class="carousel-card"><div style="font-size:2rem;">📈</div><b style="color:#38bdf8">GESTÃO</b><br><small>Sua empresa no controle financeiro.</small></div>
            <div class="carousel-card"><div style="font-size:2rem;">⚖️</div><b style="color:#38bdf8">TRIBUTÁRIO</b><br><small>Redução legal de impostos.</small></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3>1. Perfil do Cadastro</h3>", unsafe_allow_html=True)
    perfil = st.radio("", ["🏢 Pessoa Jurídica (Empresa)", "👤 Pessoa Física (Individual)"], horizontal=True, label_visibility="collapsed")

    # --- FLUXO PJ ---
    if "Jurídica" in perfil:
        col_c, col_b = st.columns([3, 1])
        with col_c: st.text_input("CNPJ Principal *", key="in_cnpj")
        with col_b: st.button("🔍 Validar", on_click=buscar_cnpj, use_container_width=True)

        if st.session_state.etapa == 2:
            st.markdown("<h3>2. Dados da Empresa</h3>", unsafe_allow_html=True)
            st.text_input("Razão Social *", value=st.session_state.razao_api, key="in_razao")
            st.selectbox("Faturamento Médio Mensal", ["Até R$ 50k", "R$ 50k a R$ 200k", "Acima de R$ 200k"], key="in_fat")

            st.markdown("<h3>3. Localização da Sede</h3>", unsafe_allow_html=True)
            st.text_input("CEP Sede *", key="in_cep_pj", on_change=buscar_cep, args=("in_cep_pj",), placeholder="00000-000")
            
            col_rua, col_num = st.columns([3, 1])
            with col_rua: st.text_input("Logradouro", value=st.session_state.endereco_api["rua"], key="pj_rua")
            with col_num: st.text_input("Nº", key="pj_num")
            
            col_bair, col_cid, col_uf = st.columns([2, 2, 1])
            with col_bair: st.text_input("Bairro", value=st.session_state.endereco_api["bairro"], key="pj_bairro")
            with col_cid: st.text_input("Cidade", value=st.session_state.endereco_api["cidade"], key="pj_cidade")
            with col_uf: st.text_input("UF", value=st.session_state.endereco_api["uf"], key="pj_uf")

            st.markdown("<h3>4. Quadro de Sócios</h3>", unsafe_allow_html=True)
            num_socios = st.number_input("Número de sócios", min_value=1, max_value=10, step=1)
            lista_socios = []
            for i in range(int(num_socios)):
                st.markdown(f"**Sócio {i+1}**")
                s_c1, s_c2 = st.columns([2, 1])
                with s_c1: s_n = st.text_input(f"Nome Sócio {i+1}", key=f"sn_{i}")
                with s_c2: s_c = st.text_input(f"CPF Sócio {i+1}", key=f"sc_{i}")
                lista_socios.append(f"{s_n} ({s_c})")

            if st.button("Finalizar e Gerar Ficha PJ", type="primary"):
                st.session_state.final_data = {"Tipo": "PJ", "CNPJ": st.session_state.in_cnpj, "Razão": st.session_state.in_razao, "Sócios": lista_socios, "Endereço": f"{st.session_state.pj_rua}, {st.session_state.pj_num} - {st.session_state.pj_cidade}/{st.session_state.pj_uf}"}
                st.session_state.cadastro_realizado = True; st.rerun()

    # --- FLUXO PF ---
    else:
        col_cpf, col_n = st.columns([1, 2])
        with col_cpf: st.text_input("CPF *", key="in_cpf")
        with col_n: st.text_input("Nome Completo *", key="in_nome_pf")
        
        st.markdown("<h3>2. Endereço Residencial</h3>", unsafe_allow_html=True)
        st.text_input("CEP *", key="in_cep_pf", on_change=buscar_cep, args=("in_cep_pf",))
        
        col_rua2, col_num2 = st.columns([3, 1])
        with col_rua2: st.text_input("Logradouro", value=st.session_state.endereco_api["rua"], key="pf_rua")
        with col_num2: st.text_input("Nº", key="pf_num")

        st.markdown("<h3>3. Validação KYC</h3>", unsafe_allow_html=True)
        metodo = st.radio("Escolha como enviar seu documento:", ["Anexar Arquivo", "Tirar Foto"], horizontal=True)
        if metodo == "Anexar Arquivo": st.file_uploader("Upload RG/CNH", type=['pdf','png','jpg'])
        else: st.camera_input("Frente do Documento")

        if st.button("Finalizar Cadastro PF", type="primary"):
            st.session_state.final_data = {"Tipo": "PF", "Nome": st.session_state.in_nome_pf, "CPF": st.session_state.in_cpf, "Endereço": f"{st.session_state.pf_rua}, {st.session_state.pf_num}"}
            st.session_state.cadastro_realizado = True; st.rerun()

else:
    st.balloons()
    st.success("✅ Ficha Cadastral Processada com Sucesso!")
    pdf_output = gerar_pdf(st.session_state.final_data)
    st.download_button("📥 BAIXAR FICHA EM PDF", data=pdf_output, file_name="Ficha_BSB.pdf", mime="application/pdf")
    if st.button("Novo Cadastro"): st.session_state.clear(); st.rerun()
