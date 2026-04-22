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

    /* Fundo Dark Mode Radial com tons de azul */
    .stApp {
        background: radial-gradient(ellipse at top, rgba(56, 189, 248, 0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom, rgba(37, 99, 235, 0.05) 0%, transparent 50%),
                    #0b1e2e;
    }

    header[data-testid="stHeader"] { background: transparent; height: 0; }

    .block-container {
        max-width: 540px !important; 
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
        font-size: 1.05rem;
        font-weight: 500;
        line-height: 1.5;
        margin-top: 12px;
        margin-bottom: 2rem; 
        padding: 0 10px;
    }

    /* ═══════════════════════════════════════════════════════════════
       CARROSSEL 3D ANIMADO (Invisível/Suave)
       ═══════════════════════════════════════════════════════════════ */
    .carousel-wrapper {
        position: relative;
        width: 100%;
        height: 180px;
        margin: 10px 0 40px 0; 
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
        top: 0; left: 50%;
        width: 280px; height: 160px;
        margin-left: -140px;
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        padding: 20px 24px;
        box-shadow: 0 20px 40px rgba(56, 189, 248, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        display: flex; flex-direction: column; justify-content: space-between;
        opacity: 0; cursor: pointer;
        animation: carousel-slide 25s infinite ease-in-out; 
    }
    .carousel-card::before {
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #38bdf8, transparent);
        opacity: 0.8;
    }
    .carousel-wrapper:hover .carousel-card, .carousel-wrapper:active .carousel-card {
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
    .carousel-label { font-size: 0.72rem; font-weight: 700; color: #38bdf8 !important; letter-spacing: 0.12em; margin-bottom: -10px; }
    .carousel-description { font-size: 0.8rem; color: #f1f5f9 !important; font-weight: 400; margin: 4px 0; line-height: 1.3; }

    /* ═══════════════════════════════════════════════════════════════
       UI NASA: FORMULÁRIO, INPUTS E TIPOGRAFIA
       ═══════════════════════════════════════════════════════════════ */
    h3 {
        display: inline-block;
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8 !important;
        padding: 10px 20px 10px 24px !important; 
        border-radius: 8px; font-size: 0.85rem !important; font-weight: 800 !important;
        letter-spacing: 0.15em; text-transform: uppercase;
        border-left: 4px solid #38bdf8;
        margin-top: 1rem !important; margin-bottom: 1.5rem !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.05);
    }
    div[data-testid="column"] { padding: 0 8px; }

    /* Inputs Glassmorphism Alto Contraste */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-baseweb="number-input"] > div {
        background: rgba(11, 30, 46, 0.6) !important; 
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.3) !important; 
        border-radius: 10px !important; 
        transition: all 0.3s ease;
    }
    div[data-baseweb="select"] > div:hover, div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:hover, div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="number-input"] > div:hover, div[data-baseweb="number-input"] > div:focus-within {
        background: rgba(11, 30, 46, 0.9) !important;
        border-color: rgba(56, 189, 248, 0.8) !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.15);
    }
    
    /* Acessibilidade: Cor do texto digitado mais clara para leitura fácil */
    input, select, div[data-baseweb="select"] span { 
        color: #e2e8f0 !important; 
        font-size: 0.9rem !important; 
        font-weight: 500 !important;
    }
    
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: #94a3b8 !important; font-size: 0.72rem !important; font-weight: 700 !important;
        text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px !important; padding-left: 2px;
    }

    /* Botão Secundário (API Buscar) */
    button[kind="secondary"] {
        background: rgba(56, 189, 248, 0.1) !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        color: #38bdf8 !important;
        border-radius: 10px !important;
        margin-top: 28px !important;
        height: 42px !important;
        transition: all 0.2s ease !important;
    }
    button[kind="secondary"]:hover {
        background: rgba(56, 189, 248, 0.2) !important;
        transform: translateY(-1px);
    }

    /* Botão CTA Principal */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: #ffffff !important; font-weight: 800; font-size: 1rem;
        border: none; border-radius: 12px; padding: 0.9rem 2rem; width: 100%;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-top: 20px; text-transform: uppercase; letter-spacing: 0.1em;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 10px 30px rgba(14, 165, 233, 0.5);
        background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
    }

    /* Trust Badge LGPD */
    .lgpd-badge {
        display: flex; align-items: center; justify-content: center; gap: 8px;
        margin-top: 15px; color: #64748b; font-size: 0.75rem; font-weight: 500;
    }
    .lgpd-badge svg { fill: #64748b; width: 14px; height: 14px; }

    div[data-testid="stExpander"] {
        background: #1a2e42; border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; margin-top: 40px;
    }
    div[data-testid="stExpander"] summary p { color: #38bdf8 !important; font-weight: 700; letter-spacing: 0.05em; }
</style>
""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  MOTOR DE INTEGRAÇÃO API E ESTADO (LÓGICA CLEAN)                      ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if 'etapa' not in st.session_state:
    st.session_state.etapa = 1
if 'cadastro_realizado' not in st.session_state:
    st.session_state.cadastro_realizado = False
if 'dados_cliente' not in st.session_state:
    st.session_state.dados_cliente = {}
if 'razao_social_api' not in st.session_state:
    st.session_state.razao_social_api = ""
if 'erro_validacao' not in st.session_state:
    st.session_state.erro_validacao = False

def buscar_cnpj_api():
    cnpj_raw = st.session_state.in_cnpj
    cnpj_limpo = re.sub(r'\D', '', cnpj_raw)
    
    if len(cnpj_limpo) == 14:
        try:
            # Integração real e gratuita com BrasilAPI para gerar o "Efeito Uau"
            response = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}", timeout=5)
            if response.status_code == 200:
                dados = response.json()
                st.session_state.razao_social_api = dados.get("razao_social", "")
                st.toast("✅ Empresa localizada com sucesso na Receita Federal!")
            else:
                st.session_state.razao_social_api = ""
        except:
            st.session_state.razao_social_api = ""
    
    st.session_state.etapa = 2 # Libera a segunda etapa

def processar_envio():
    razao = st.session_state.in_razao
    regime = st.session_state.in_regime
    faturamento = st.session_state.in_fat
    erp = st.session_state.in_erp

    if not razao or regime == "Selecione..." or faturamento == "Selecione...":
        st.session_state.erro_validacao = True
    else:
        st.session_state.erro_validacao = False
        st.session_state.dados_cliente = {
            "cnpj": st.session_state.in_cnpj,
            "razao": razao,
            "faturamento": faturamento,
            "erp": erp,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        st.session_state.cadastro_realizado = True

def resetar_tela():
    st.session_state.etapa = 1
    st.session_state.cadastro_realizado = False
    st.session_state.dados_cliente = {}
    st.session_state.razao_social_api = ""
    st.session_state.erro_validacao = False

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CABEÇALHO DA TELA E SAUDAÇÃO                                         ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.markdown('<h1 class="bsb-logo">BSB Contabilidade</h1>', unsafe_allow_html=True)
st.markdown("""
<p class="bsb-slogan">
    Seja bem-vindo(a)! Para darmos continuidade ao seu processo, solicitamos o preenchimento das informações a seguir:
</p>
""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CARROSSEL DE SERVIÇOS 3D                                             ║
# ╚═══════════════════════════════════════════════════════════════════════╝
carousel_html = """
<div class="carousel-wrapper">
    <div class="carousel-track">
        <div class="carousel-card"><div class="carousel-icon">🏢</div><div class="carousel-label">SOCIETÁRIO</div><div class="carousel-description">Todo negócio precisa estar juridicamente em dia para garantir segurança e conformidade.</div></div>
        <div class="carousel-card"><div class="carousel-icon">💰</div><div class="carousel-label">RECUPERAÇÃO DE CRÉDITOS</div><div class="carousel-description">Você sabia que sua empresa pode ter valores pagos indevidamente a serem recuperados?</div></div>
        <div class="carousel-card"><div class="carousel-icon">🧾</div><div class="carousel-label">DEPARTAMENTO FISCAL</div><div class="carousel-description">O cenário tributário brasileiro é desafiador, mas ajudamos na correta apuração e entrega.</div></div>
        <div class="carousel-card"><div class="carousel-icon">👥</div><div class="carousel-label">DEPARTAMENTO PESSOAL</div><div class="carousel-description">Gerenciar pessoas exige atenção constante à legislação trabalhista e previdenciária.</div></div>
        <div class="carousel-card"><div class="carousel-icon">📊</div><div class="carousel-label">CONTABILIDADE</div><div class="carousel-description">Na BSB Contabilidade, tratamos a contabilidade como uma ferramenta de gestão.</div></div>
    </div>
    <div style="text-align: center; color: #64748b; font-size: 0.65rem; margin-top: 155px; opacity: 0.7;">
        👉 Pressione ou passe o mouse no card para pausar a leitura
    </div>
</div>
"""
if not st.session_state.cadastro_realizado:
    st.markdown(carousel_html, unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  INTERFACE DO FORMULÁRIO (PROGRESSIVE DISCLOSURE)                     ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if not st.session_state.cadastro_realizado:
    
    # ETAPA 1: Identificação (CNPJ)
    st.markdown("<h3>1. Identificação</h3>", unsafe_allow_html=True)
    
    col_cnpj, col_btn = st.columns([3, 1], gap="small")
    with col_cnpj:
        st.text_input("CNPJ da Empresa *", placeholder="00.000.000/0000-00", key="in_cnpj")
    with col_btn:
        st.button("🔍 Buscar", on_click=buscar_cnpj_api, use_container_width=True)

    # ETAPA 2: Abre apenas se o usuário avançar
    if st.session_state.etapa == 2:
        st.markdown("<h3>2. Dados Operacionais</h3>", unsafe_allow_html=True)
        
        st.text_input("Razão Social *", value=st.session_state.razao_social_api, placeholder="Sua Empresa LTDA", key="in_razao")
            
        col3, col4 = st.columns([1, 1], gap="medium")
        with col3:
            st.text_input("WhatsApp do Gestor", placeholder="(00) 00000-0000", key="in_wpp")
        with col4:
            st.text_input("E-mail Financeiro", placeholder="financeiro@empresa.com", key="in_email")

        col5, col6 = st.columns([1, 1], gap="medium")
        with col5:
            st.selectbox("Regime Tributário", ["Selecione...", "Simples Nacional", "Lucro Presumido", "Lucro Real"], key="in_regime")
            st.selectbox("Sistema de Gestão (ERP)", ["Nenhum / Excel", "Conta Azul", "Omie", "Nibo", "Bling", "Outro"], key="in_erp")
        with col6:
            st.selectbox("Faturamento Médio Mensal", ["Selecione...", "Até R$ 20.000", "R$ 20.001 a R$ 100.000", "R$ 100.001 a R$ 500.000", "Acima de R$ 500.000"], key="in_fat")
            st.number_input("Volume NFs emitidas/mês", min_value=0, step=10, key="in_notas")

        if st.session_state.erro_validacao:
            st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.4); color: #ef4444; padding: 12px; border-radius: 8px; text-align: center; font-weight: 600; margin-top: 10px;">
                ⚠️ Por favor, preencha todos os campos obrigatórios (*).
            </div>
            """, unsafe_allow_html=True)

        st.button("Finalizar Cadastro Seguro", on_click=processar_envio, type="primary")
        
        # Selo Trust & Compliance (LGPD)
        st.markdown("""
        <div class="lgpd-badge">
            <svg viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>
            Ambiente criptografado e 100% aderente à LGPD.
        </div>
        """, unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  TELA DE SUCESSO                                                      ║
# ╚═══════════════════════════════════════════════════════════════════════╝
else:
    with st.spinner("Criptografando e processando dados..."):
        time.sleep(1.5)
    st.success(f"✅ Cadastro finalizado com sucesso! Nossa equipe analisará seus dados e entrará em contato.")
    st.info("A BSB Contabilidade agradece a confiança. Um consultor enviará os próximos passos no seu WhatsApp.")
    st.balloons()
    
    st.button("⬅️ Novo Cadastro (Modo Demo)", on_click=resetar_tela)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  EASTER EGG: MOTOR DE RISCO DO BACK-OFFICE (LÓGICA AVANÇADA)          ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if st.session_state.cadastro_realizado:
    with st.expander("🔒 VISÃO INTERNA BSB (Mostrar na Reunião)"):
        st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Processamento SQL simulado pós-captação:</p>", unsafe_allow_html=True)
        dados = st.session_state.dados_cliente
        
        # Motor de Score Logico (Categorização de Risco: Baixo a Crítico)
        risco = "BAIXO"
        cor_risco = "#10b981" 
        recomendacao = "Fluxo padrão liberado. Setup simplificado."
        
        if dados['erp'] == "Nenhum / Excel" and dados['faturamento'] in ["R$ 100.001 a R$ 500.000", "Acima de R$ 500.000"]:
            risco = "CRÍTICO"
            cor_risco = "#ef4444"
            recomendacao = "Atenção: Alto volume sem ERP. Exige capping manual. Acionar matriz de risco."
        elif dados['erp'] == "Nenhum / Excel":
            risco = "MÉDIO"
            cor_risco = "#f59e0b"
            recomendacao = "Normalização necessária. Implantar Conta Azul pré-onboarding."

        st.markdown(f"""
        <div style="background: #0b1e2e; padding: 15px; border-radius: 10px; border: 1px solid #334155;">
            <p style="margin: 0; color: #f1f5f9;"><strong>Lead Capturado:</strong> {dados['razao']} ({dados['cnpj']})</p>
            <p style="margin: 0; color: #f1f5f9;"><strong>Faturamento:</strong> {dados['faturamento']}</p>
            <p style="margin: 0; color: #f1f5f9;"><strong>Fonte de Dados:</strong> {dados['erp']}</p>
            <hr style="border-color: #334155;">
            <h4 style="color: #38bdf8; margin-bottom: 5px;">🤖 Motor de Score Analítico</h4>
            <p style="margin: 0; color: #f1f5f9;">Classificação de Risco Operacional: <strong style='color: {cor_risco}; font-size: 1.1rem;'>{risco}</strong></p>
            <p style="margin: 0; color: #94a3b8; font-size: 0.85rem;">Diretriz do Sistema: {recomendacao}</p>
        </div>
        """, unsafe_allow_html=True)
