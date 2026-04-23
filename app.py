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
# ║  CONFIGURAÇÃO DA PÁGINA E UX/UI GLOBAL (PADRÃO BSB AZUL PREMIUM)      ║
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
    .block-container { max-width: 520px !important; padding: 3rem 1rem !important; }
    .bsb-logo {
        font-size: 2.6rem; font-weight: 900;
        background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 50%, #2563eb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin: 0; letter-spacing: -0.04em;
        filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.2));
    }
    .bsb-slogan { text-align: center; color: #94a3b8 !important; font-size: 1rem; margin-bottom: 2rem; }

    /* CARROSSEL 3D */
    .carousel-wrapper { position: relative; width: 100%; height: 180px; margin-bottom: 30px; perspective: 1200px; overflow: hidden; }
    .carousel-track { position: relative; width: 100%; height: 100%; transform-style: preserve-3d; }
    .carousel-card {
        position: absolute; top: 0; left: 50%; width: 280px; height: 160px; margin-left: -140px;
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
        border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 20px; padding: 20px;
        animation: carousel-slide 25s infinite ease-in-out; opacity: 0;
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

    /* TITULOS E INPUTS */
    h3 {
        display: inline-block; background: rgba(56, 189, 248, 0.1); color: #38bdf8 !important;
        padding: 8px 16px !important; border-radius: 8px; font-size: 0.8rem !important;
        text-transform: uppercase; border-left: 4px solid #38bdf8; margin: 1.5rem 0 1rem 0 !important;
    }
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background: rgba(11, 30, 46, 0.6) !important; border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important; color: #e2e8f0 !important;
    }
    label { color: #94a3b8 !important; font-size: 0.72rem !important; font-weight: 700 !important; text-transform: uppercase; }

    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: #ffffff !important; font-weight: 800; border-radius: 10px; width: 100%; height: 50px;
    }
</style>
""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  LÓGICA E ESTADO                                                      ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'cadastro_realizado' not in st.session_state: st.session_state.cadastro_realizado = False
if 'dados_finais' not in st.session_state: st.session_state.dados_finais = {}
if 'razao_api' not in st.session_state: st.session_state.razao_api = ""

def buscar_cnpj():
    cnpj = re.sub(r'\D', '', st.session_state.in_cnpj)
    if len(cnpj) == 14:
        try:
            res = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}", timeout=5)
            if res.status_code == 200:
                st.session_state.razao_api = res.json().get("razao_social", "")
                st.toast("✅ Dados da Receita Federal Importados!")
        except: pass
    st.session_state.etapa = 2

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "FICHA CADASTRAL ESTRUTURADA - BSB", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    for k, v in dados.items():
        pdf.multi_cell(0, 8, f"{k.upper()}: {v}")
    return pdf.output(dest='S').encode('latin-1')

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  INTERFACE                                                            ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.markdown('<h1 class="bsb-logo">BSB Contabilidade</h1>', unsafe_allow_html=True)

if not st.session_state.cadastro_realizado:
    st.markdown('<p class="bsb-slogan">Onboarding Digital e Triagem de Conformidade Bancária</p>', unsafe_allow_html=True)
    
    # CARROSSEL DNA ORIGINAL
    st.markdown("""
    <div class="carousel-wrapper">
        <div class="carousel-track">
            <div class="carousel-card"><div style="font-size:2rem;">🛡️</div><b style="color:#38bdf8">SOCIETÁRIO</b><br><small>Estruturação de QSA para proteção patrimonial.</small></div>
            <div class="carousel-card"><div style="font-size:2rem;">📈</div><b style="color:#38bdf8">CRÉDITO</b><br><small>Análise de faturamento e solvência para captação.</small></div>
            <div class="carousel-card"><div style="font-size:2rem;">⚖️</div><b style="color:#38bdf8">COMPLIANCE</b><br><small>Verificação KYC e conformidade com a LGPD.</small></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3>1. Perfil do Cadastro</h3>", unsafe_allow_html=True)
    perfil = st.radio("", ["🏢 Empresa (PJ)", "👤 Indivíduo (PF)"], horizontal=True, label_visibility="collapsed")

    if "PJ" in perfil:
        col_c, col_b = st.columns([3, 1])
        with col_c: st.text_input("CNPJ Principal *", key="in_cnpj")
        with col_b: st.button("🔍 Validar", on_click=buscar_cnpj, use_container_width=True)

        if st.session_state.etapa == 2:
            st.markdown("<h3>2. Dados da Empresa</h3>", unsafe_allow_html=True)
            st.text_input("Razão Social *", value=st.session_state.razao_api)
            st.selectbox("Faturamento Mensal", ["Até R$ 50k", "R$ 50k a R$ 200k", "Acima de R$ 200k"], key="in_fat")

            # ════════════ ESTRUTURA SOCIETÁRIA DINÂMICA ════════════
            st.markdown("<h3>3. Quadro de Sócios e Administradores</h3>", unsafe_allow_html=True)
            num_socios = st.number_input("Número de sócios na empresa", min_value=1, max_value=10, step=1)
            
            lista_socios = []
            for i in range(int(num_socios)):
                st.markdown(f"**Dados do Sócio {i+1}**")
                s_col1, s_col2 = st.columns([2, 1])
                with s_col1: s_nome = st.text_input(f"Nome Completo Sócio {i+1}", key=f"s_nome_{i}")
                with s_col2: s_cpf = st.text_input(f"CPF Sócio {i+1}", key=f"s_cpf_{i}")
                if s_nome and s_cpf:
                    lista_socios.append(f"{s_nome} (CPF: {s_cpf})")

            if st.button("Finalizar e Gerar Documento", type="primary"):
                st.session_state.dados_finais = {
                    "Tipo": "PJ", "CNPJ": st.session_state.in_cnpj, 
                    "Razão": st.session_state.razao_api, 
                    "Sócios": " | ".join(lista_socios),
                    "Faturamento": st.session_state.in_fat
                }
                st.session_state.cadastro_realizado = True
                st.rerun()

    else:
        st.markdown("<h3>1. Dados Pessoais</h3>", unsafe_allow_html=True)
        st.text_input("Nome Completo *", key="pf_nome")
        st.text_input("CPF *", key="pf_cpf")
        st.selectbox("Patrimônio Estimado", ["Até R$ 500k", "R$ 500k a R$ 2M", "Acima de R$ 2M"], key="pf_pat")
        
        st.markdown("<h3>2. Verificação KYC</h3>", unsafe_allow_html=True)
        st.camera_input("Capture o documento de identidade")

        if st.button("Finalizar Cadastro de Alta Renda", type="primary"):
            st.session_state.dados_finais = {
                "Tipo": "PF", "Nome": st.session_state.pf_nome, 
                "CPF": st.session_state.pf_cpf, "Patrimônio": st.session_state.pf_pat
            }
            st.session_state.cadastro_realizado = True
            st.rerun()

else:
    st.balloons()
    st.markdown('<h2 style="text-align:center;">✅ Cadastro Concluído</h2>', unsafe_allow_html=True)
    pdf_output = gerar_pdf(st.session_state.dados_finais)
    st.download_button("📥 BAIXAR MINHA FICHA CADASTRAL (PDF)", data=pdf_output, file_name="Ficha_BSB.pdf", mime="application/pdf")
    if st.button("Novo Cadastro"): st.session_state.clear(); st.rerun()
