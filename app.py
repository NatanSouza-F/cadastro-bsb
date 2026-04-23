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

# CSS NASA: Glassmorphism, Micro-interações, Acessibilidade e Carrossel 3D
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }

    /* Fundo Dark Mode Radial com tons de azul */
    .stApp {
        background: radial-gradient(ellipse at top, rgba(56, 189, 248, 0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom, rgba(37, 99, 235, 0.05) 0%, transparent 50%),
                    #0b1e2e;
    }

    header[data-testid="stHeader"] { background: transparent; height: 0; }

    .block-container {
        max-width: 520px !important; 
        padding: 3rem 1rem 1rem 1rem !important;
    }

    h1, h2, h3, h4, p, span, div, label { color: #f1f5f9; }

    /* Logo BSB com gradiente Azul Premium */
    .bsb-logo {
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 50%, #2563eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 0;
        letter-spacing: -0.04em;
        filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.2));
    }
    
    .bsb-slogan {
        text-align: center;
        color: #94a3b8 !important;
        font-size: 1rem;
        font-weight: 500;
        margin-top: 8px;
        margin-bottom: 2rem;
    }

    /* ═══════════════════════════════════════════════════════════════
       CARROSSEL 3D ANIMADO ( DNA DO PRIMEIRO PROTÓTIPO )
       ═══════════════════════════════════════════════════════════════ */
    .carousel-wrapper {
        position: relative;
        width: 100%;
        height: 180px;
        margin: 10px 0 30px 0;
        perspective: 1200px;
        overflow: hidden;
    }
    
    .carousel-track {
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
    }

    .carousel-card {
        position: absolute;
        top: 0;
        left: 50%;
        width: 280px;
        height: 160px;
        margin-left: -140px;
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        padding: 20px 24px;
        box-shadow: 0 20px 40px rgba(56, 189, 248, 0.15), 0 0 0 1px rgba(56, 189, 248, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        opacity: 0;
        cursor: pointer;
        animation: carousel-slide 25s infinite ease-in-out; 
    }

    .carousel-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #38bdf8, transparent);
        opacity: 0.8;
    }
    
    .carousel-wrapper:hover .carousel-card {
        animation-play-state: paused !important;
    }
    
    .carousel-card:nth-child(1) { animation-delay: 0s; }
    .carousel-card:nth-child(2) { animation-delay: 5s; }
    .carousel-card:nth-child(3) { animation-delay: 10s; }
    .carousel-card:nth-child(4) { animation-delay: 15s; }
    .carousel-card:nth-child(5) { animation-delay: 20s; }

    @keyframes carousel-slide {
        0% { opacity: 0; transform: translateX(100px) scale(0.9); }
        4% { opacity: 1; transform: translateX(0) scale(1); }
        16% { opacity: 1; transform: translateX(0) scale(1); }
        20% { opacity: 0; transform: translateX(-100px) scale(0.9); }
        100% { opacity: 0; transform: translateX(-100px) scale(0.9); }
    }

    .carousel-icon { font-size: 1.8rem; line-height: 1; margin-bottom: 2px;}
    .carousel-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #38bdf8 !important;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: -10px;
    }
    .carousel-description {
        font-size: 0.8rem;
        color: #f1f5f9 !important;
        font-weight: 400;
        margin: 4px 0;
        text-shadow: none;
        line-height: 1.3;
    }

    /* UI NASA: FORMULÁRIO, INPUTS E TIPOGRAFIA */
    
    /* Títulos de Sessão (Badges) */
    h3 {
        display: inline-block;
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8 !important;
        padding: 8px 16px !important;
        border-radius: 8px;
        font-size: 0.8rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        border-left: 4px solid #38bdf8;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.05);
    }

    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, div[data-baseweb="number-input"] > div {
        background: rgba(11, 30, 46, 0.6) !important; 
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.2) !important; 
        border-radius: 10px !important; 
        color: #e2e8f0 !important;
        transition: all 0.3s ease;
    }
    
    div[data-baseweb="input"] > div:hover, div[data-baseweb="input"] > div:focus-within {
        background: rgba(11, 30, 46, 0.9) !important;
        border-color: rgba(56, 189, 248, 0.8) !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.15);
    }
    
    input, select { color: #e2e8f0 !important; font-size: 0.9rem !important;}
    
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: #94a3b8 !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Botão Primary */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: #ffffff !important;
        font-weight: 800;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2rem;
        width: 100%;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-top: 20px;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 8px 30px rgba(14, 165, 233, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  LÓGICA E ESTADO                                                      ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'cadastro_realizado' not in st.session_state: st.session_state.cadastro_realizado = False
if 'dados' not in st.session_state: st.session_state.dados = {}
if 'razao_social_api' not in st.session_state: st.session_state.razao_social_api = ""
if 'nome_fantasia_api' not in st.session_state: st.session_state.nome_fantasia_api = ""

def buscar_cnpj():
    cnpj = re.sub(r'\D', '', st.session_state.in_cnpj)
    if len(cnpj) == 14:
        try:
            response = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}", timeout=5)
            if response.status_code == 200:
                dados = response.json()
                st.session_state.razao_social_api = dados.get("razao_social", "")
                st.session_state.nome_fantasia_api = dados.get("nome_fantasia", "")
                st.toast("✅ Empresa validada na Receita!")
        except: pass
    st.session_state.etapa = 2

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
# ║  BOAS-VINDAS E CARROSSEL 3D                                           ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.markdown('<h1 class="bsb-logo">BSB Contabilidade</h1>', unsafe_allow_html=True)

if not st.session_state.cadastro_realizado:
    st.markdown('<p class="bsb-slogan">Seja bem-vindo(a)! Para darmos continuidade ao seu processo, solicitamos o preenchimento das informações a seguir:</p>', unsafe_allow_html=True)
    
    # Carrossel 3D Animado ( DNA do primeiro protótipo )
    carousel_html = """
    <div class="carousel-wrapper">
        <div class="carousel-track">
            <div class="carousel-card">
                <div class="carousel-icon">🏢</div>
                <div class="carousel-label">SOCIETÁRIO</div>
                <div class="carousel-description">Todo negócio precisa estar juridicamente em dia para garantir segurança e conformidade.</div>
            </div>
            <div class="carousel-card">
                <div class="carousel-icon">💰</div>
                <div class="carousel-label">RECUPERAÇÃO DE CRÉDITOS</div>
                <div class="carousel-description">Você sabia que sua empresa pode ter valores pagos indevidamente a serem recuperados?</div>
            </div>
            <div class="carousel-card">
                <div class="carousel-icon">🧾</div>
                <div class="carousel-label">DEPARTAMENTO FISCAL</div>
                <div class="carousel-description">O cenário tributário brasileiro é desafiador, mas ajudamos na correta apuração e entrega.</div>
            </div>
            <div class="carousel-card">
                <div class="carousel-icon">👥</div>
                <div class="carousel-label">DEPARTAMENTO PESSOAL</div>
                <div class="carousel-description">Gerenciar pessoas exige atenção constante à legislação trabalhista e previdenciária.</div>
            </div>
            <div class="carousel-card">
                <div class="carousel-icon">📊</div>
                <div class="carousel-label">CONTABILIDADE</div>
                <div class="carousel-description">Na BSB Contabilidade, tratamos a contabilidade como uma ferramenta de gestão.</div>
            </div>
        </div>
        <div style="text-align: center; color: #64748b; font-size: 0.65rem; margin-top: 155px; opacity: 0.7;">
            👉 Pressione ou passe o mouse no card para pausar a leitura
        </div>
    </div>
    """
    st.markdown(carousel_html, unsafe_allow_html=True)

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  INTERFACE DO FORMULÁRIO ( NÍVEL BANCÁRIO DETALHADO )                 ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    st.markdown("<h3>1. Qual é o seu perfil?</h3>", unsafe_allow_html=True)
    perfil = st.radio("Selecione:", ["🏢 Empresa (CNPJ)", "👤 Pessoa Física (CPF)"], horizontal=True, label_visibility="collapsed")

    if "Empresa" in perfil:
        col_c, col_b = st.columns([3, 1])
        with col_c: st.text_input("CNPJ Principal *", key="in_cnpj", placeholder="00.000.000/0000-00")
        with col_b: st.button("🔍 Validar", on_click=buscar_cnpj, use_container_width=True)

        if st.session_state.etapa == 2:
            st.markdown("<h3>2. Dados Institucionais e Contato</h3>", unsafe_allow_html=True)
            st.text_input("Razão Social (Receita Federal) *", value=st.session_state.razao_social_api, key="in_razao")
            col_fan, col_cnae = st.columns(2)
            with col_fan: st.text_input("Nome Fantasia", value=st.session_state.nome_fantasia_api, key="in_fantasia")
            with col_cnae: st.text_input("Atividade Principal (CNAE)", placeholder="Ex: 6201-5/00", key="in_cnae")
            
            st.markdown("<h3>3. Localização da Sede</h3>", unsafe_allow_html=True)
            st.text_input("CEP Sede *", key="in_cep_pj", placeholder="00000-000")
            
            st.markdown("<h3>4. Análise Financeira & Risco</h3>", unsafe_allow_html=True)
            col_fat, col_div = st.columns(2)
            with col_fat: st.selectbox("Faturamento Médio Mensal *", ["Até R$ 30k", "R$ 30k a R$ 100k", "R$ 100k a R$ 500k", "Acima de R$ 500k"], key="in_fat")
            with col_div: st.selectbox("Possui Dívidas Fiscais?", ["Não", "Sim - Parceladas", "Sim - Em aberto", "Em execução fiscal"], key="in_divida")
            
            st.markdown("<h3>5. Representante Legal (Para Contrato)</h3>", unsafe_allow_html=True)
            st.text_input("Nome Completo do Sócio Assinante *", key="in_socio_nome")
            st.text_input("CPF do Sócio *", placeholder="000.000.000-00", key="in_socio_cpf")
            
            if st.button("Finalizar Cadastro Corporativo", type="primary"):
                st.session_state.dados = {"Tipo": "PJ", "CNPJ": st.session_state.in_cnpj, "Razão": st.session_state.in_razao, "Sócio": st.session_state.in_socio_nome, "Risco": st.session_state.in_divida, "Faturamento": st.session_state.in_fat}
                st.session_state.cadastro_realizado = True
                st.rerun()

    else:
        col_cpf, col_n = st.columns([1, 2])
        with col_cpf: st.text_input("CPF *", placeholder="000.000.000-00", key="in_cpf")
        with col_n: st.text_input("Nome Completo *", placeholder="Digite seu nome", key="in_nome_pf")
        st.button("Avançar", on_click=lambda: st.session_state.update({"etapa": 2}), use_container_width=True)

        if st.session_state.etapa == 2:
            st.markdown("<h3>2. Perfil Patrimonial & Rendimentos</h3>", unsafe_allow_html=True)
            col_renda, col_bens = st.columns(2)
            with col_renda: st.selectbox("Renda Mensal Comprovada", ["Até R$ 5k", "R$ 5k a R$ 15k", "R$ 15k a R$ 50k", "Acima de R$ 50k"], key="in_renda_pf")
            with col_bens: st.multiselect("Possui bens em seu nome?", ["Imóvel Próprio", "Veículo", "Investimentos (Bolsa/Cripto)", "Participação em outras empresas"], key="in_bens")
            
            st.text_input("CEP de Residência *", placeholder="00000-000", key="in_cep_pf")

            st.markdown("<h3>3. Validação de Segurança (KYC)</h3>", unsafe_allow_html=True)
            st.camera_input("Capture a frente do seu Documento (RG/CNH)")
            st.camera_input("Capture o verso do seu Documento")

            if st.button("Finalizar Cadastro de Alta Renda", type="primary"):
                st.session_state.dados = {"Tipo": "PF", "Nome": st.session_state.in_nome_pf, "CPF": st.session_state.in_cpf, "Renda": st.session_state.in_renda_pf, "Bens": st.session_state.in_bens}
                st.session_state.cadastro_realizado = True
                st.rerun()

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  TELA DE SUCESSO E DOWNLOAD DO PDF                                  ║
# ╚═══════════════════════════════════════════════════════════════════════╝
else:
    st.balloons()
    st.markdown('<h1 class="bsb-logo">Pronto!</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; color:#94a3b8; padding: 20px;'>
        Sua ficha cadastral de alta complexidade foi processada.<br>
        Faça o download do PDF abaixo e aguarde o contato do nosso comitê de onboarding.
    </div><br>
    """, unsafe_allow_html=True)
    
    # Gera o PDF com os dados capturados
    pdf_data = gerar_pdf(st.session_state.dados)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 BAIXAR FICHA CADASTRAL (PDF)",
            data=pdf_data,
            file_name=f"Ficha_BSB_Banking_{datetime.now().strftime('%d_%m')}.pdf",
            mime="application/pdf"
        )
        st.button("Iniciar Novo Cadastro", on_click=lambda: st.session_state.clear())
