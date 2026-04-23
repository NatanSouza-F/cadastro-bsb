import streamlit as st
import requests
import re
from datetime import datetime
from io import BytesIO

# Importação para o PDF (Necessário instalar: pip install fpdf)
try:
    from fpdf import FPDF
except ImportError:
    st.error("Por favor, instale a biblioteca de PDF: pip install fpdf")

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURAÇÃO DE TELA E CSS PREMIUM                                   ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.set_page_config(page_title="BSB Onboarding Profissional", page_icon="🏢", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp {
        background: #0b1e2e;
        background-image: radial-gradient(circle at 20% 10%, rgba(37, 99, 235, 0.1) 0%, transparent 40%);
    }
    .bsb-logo {
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 5px;
    }
    .welcome-box {
        background: rgba(255,255,255,0.03);
        padding: 25px; border-radius: 15px; border: 1px solid rgba(56,189,248,0.2);
        margin-bottom: 30px; text-align: center;
    }
    h3 {
        color: #38bdf8 !important; font-size: 0.9rem !important;
        text-transform: uppercase; letter-spacing: 1px; border-left: 4px solid #38bdf8;
        padding-left: 15px; margin: 25px 0 15px 0 !important;
    }
    /* Estilo para Botão Primário */
    div[data-testid="stButton"] button[kind="primary"] {
        background: #2563eb; width: 100%; border-radius: 10px; height: 50px; font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  LOGICA DE NEGOCIO                                                    ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if 'fluxo' not in st.session_state: st.session_state.fluxo = "welcome"
if 'dados' not in st.session_state: st.session_state.dados = {}

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "FICHA CADASTRAL - BSB CONTABILIDADE", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    for k, v in dados.items():
        pdf.cell(200, 8, f"{k.upper()}: {v}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  TELA 1: BOAS-VINDAS (WELCOME)                                        ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if st.session_state.fluxo == "welcome":
    st.markdown('<h1 class="bsb-logo">BSB Contabilidade</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="welcome-box">
        <h2 style='color:white; font-size:1.4rem;'>Bem-vindo ao seu Onboarding Estratégico</h2>
        <p style='color:#94a3b8;'>Para oferecermos a melhor consultoria e soluções de crédito/fiscal, 
        precisamos conhecer profundamente o seu perfil ou o da sua empresa.</p>
        <p style='color:#38bdf8; font-weight:600;'>Este processo leva cerca de 5 minutos e é 100% seguro.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("INICIAR MEU CADASTRO", type="primary"):
        st.session_state.fluxo = "form"
        st.rerun()

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  TELA 2: FORMULÁRIO DE ALTA COMPLEXIDADE                              ║
# ╚═══════════════════════════════════════════════════════════════════════╝
elif st.session_state.fluxo == "form":
    st.markdown('<h1 class="bsb-logo" style="font-size:1.8rem;">Ficha Cadastral BSB</h1>', unsafe_allow_html=True)
    
    perfil = st.selectbox("Selecione o Perfil do Cadastro", ["Pessoa Jurídica (Empresa)", "Pessoa Física (Individual)"])
    
    if "Jurídica" in perfil:
        st.markdown("<h3>1. Identificação Corporativa</h3>", unsafe_allow_html=True)
        cnpj = st.text_input("CNPJ *")
        razao = st.text_input("Razão Social *")
        cnae = st.text_input("Atividade Principal (CNAE)")
        
        st.markdown("<h3>2. Análise de Saúde Financeira</h3>", unsafe_allow_html=True)
        fat = st.selectbox("Faturamento Médio Mensal", ["Até R$ 30k", "R$ 30k a R$ 100k", "R$ 100k a R$ 500k", "Acima de R$ 500k"])
        funcionarios = st.number_input("Número de Funcionários", min_value=0, step=1)
        st.selectbox("Possui Dívidas Fiscais ou Bancárias?", ["Não", "Sim - Sob controle", "Sim - Necessito Apoio/Parcelamento"])
        
        st.markdown("<h3>3. Localização e Contato</h3>", unsafe_allow_html=True)
        cep = st.text_input("CEP Sede")
        email = st.text_input("E-mail Financeiro")
        
        if st.button("FINALIZAR E GERAR FICHA", type="primary"):
            st.session_state.dados = {"Tipo": "PJ", "CNPJ": cnpj, "Razão": razao, "Faturamento": fat, "CEP": cep}
            st.session_state.fluxo = "final"
            st.rerun()

    else:
        st.markdown("<h3>1. Dados Pessoais</h3>", unsafe_allow_html=True)
        nome = st.text_input("Nome Completo *")
        cpf = st.text_input("CPF *")
        
        st.markdown("<h3>2. Perfil Patrimonial (Análise de Crédito)</h3>", unsafe_allow_html=True)
        renda = st.selectbox("Renda Mensal Estipada", ["Até R$ 5k", "R$ 5k a R$ 15k", "R$ 15k a R$ 30k", "Acima de R$ 30k"])
        bens = st.multiselect("Possui bens em seu nome?", ["Imóvel Próprio", "Veículo", "Investimentos (Bolsa/Cripto)", "Empresas em outros CNPJs"])
        st.selectbox("Deseja realizar Planejamento Sucessório ou Tributário?", ["Sim", "Não", "Tenho interesse em conhecer"])
        
        st.markdown("<h3>3. Documentação KYC</h3>", unsafe_allow_html=True)
        st.camera_input("Capture a frente do seu Documento (RG ou CNH)")
        
        if st.button("FINALIZAR E GERAR FICHA", type="primary"):
            st.session_state.dados = {"Tipo": "PF", "Nome": nome, "CPF": cpf, "Renda": renda}
            st.session_state.fluxo = "final"
            st.rerun()

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  TELA 3: FINALIZAÇÃO E DOWNLOAD                                       ║
# ╚═══════════════════════════════════════════════════════════════════════╝
else:
    st.balloons()
    st.markdown('<h1 class="bsb-logo">Pronto!</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; color:#94a3b8;'>
        Sua ficha cadastral foi processada com sucesso.<br>
        Abaixo você pode baixar o resumo das informações enviadas.
    </div><br>
    """, unsafe_allow_html=True)
    
    pdf_data = gerar_pdf(st.session_state.dados)
    st.download_button(
        label="📥 BAIXAR MINHA FICHA CADASTRAL (PDF)",
        data=pdf_data,
        file_name=f"Ficha_BSB_{datetime.now().strftime('%d_%m')}.pdf",
        mime="application/pdf"
    )
    
    if st.button("Iniciar Novo Cadastro"):
        st.session_state.fluxo = "welcome"
        st.rerun()
