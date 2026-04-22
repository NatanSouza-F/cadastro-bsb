import streamlit as st
import time
from datetime import datetime

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURAÇÃO DA PÁGINA E UX/UI GLOBAL (PADRÃO BSB AZUL PREMIUM)      ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.set_page_config(page_title="BSB Contabilidade | Onboarding", page_icon="🏢", layout="centered")

# CSS customizado para a paleta Azul BSB com animações padrão PULSE
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
        max-width: 480px !important;
        padding: 3rem 1rem 1rem 1rem !important;
    }

    h1, h2, h3, h4, p, span, div, label { color: #f1f5f9; }

    /* Logo BSB com gradiente Azul Premium */
    .bsb-logo {
        font-size: 2.4rem;
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
       CARROSSEL 3D ANIMADO — Estilo premium adapted for BSB services
       ═══════════════════════════════════════════════════════════════ */
    .carousel-wrapper {
        position: relative;
        width: 100%;
        height: 180px;
        margin: 16px 0 24px 0;
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
        animation: carousel-rotate 20s infinite ease-in-out;
    }
    .carousel-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #38bdf8, transparent);
        opacity: 0.8;
    }
    .carousel-card:nth-child(1) { animation-delay: 0s; }
    .carousel-card:nth-child(2) { animation-delay: 5s; }
    .carousel-card:nth-child(3) { animation-delay: 10s; }
    .carousel-card:nth-child(4) { animation-delay: 15s; }

    @keyframes carousel-rotate {
        0%, 100% { opacity: 0; transform: translateX(0) rotateY(90deg) scale(0.8); }
        5% { opacity: 1; transform: translateX(0) rotateY(0deg) scale(1); }
        20% { opacity: 1; transform: translateX(0) rotateY(0deg) scale(1); }
        25% { opacity: 0; transform: translateX(-100%) rotateY(-90deg) scale(0.8); }
    }

    .carousel-icon { font-size: 1.8rem; line-height: 1; }
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
    }

    /* Card Principal do Formulário com Glow Azul */
    .main-card {
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(56, 189, 248, 0.05);
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
    }
    
    /* Borda superior azul luminosa no card */
    .main-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, #38bdf8, transparent);
        opacity: 0.8;
    }

    /* Títulos das sessões */
    h3 {
        color: #38bdf8 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-bottom: 1px solid rgba(56, 189, 248, 0.15);
        padding-bottom: 8px;
        margin-top: 1rem;
        margin-bottom: 1rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* Estilização dos Inputs Dark */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: #0b1e2e !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }
    div[data-baseweb="select"] > div:hover, div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:hover, div[data-baseweb="input"] > div:focus-within {
        border-color: rgba(56, 189, 248, 0.6) !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.1);
    }
    
    input, select, div[data-baseweb="select"] span { color: #f1f5f9 !important; }
    
    /* Cor dos labels dos inputs */
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
    }

    /* Botão estilo CTA Azul */
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: #ffffff !important;
        font-weight: 800;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        width: 100%;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.25);
        transition: all 0.3s ease;
        margin-top: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4);
        background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
    }

    /* Ajuste para Expander (Visão Interna) */
    div[data-testid="stExpander"] {
        background: #1a2e42;
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
    }
    div[data-testid="stExpander"] summary p {
        color: #38bdf8 !important;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  GERENCIAMENTO DE ESTADO E CALLBACKS (A BLINDAGEM)                    ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if 'cadastro_realizado' not in st.session_state:
    st.session_state.cadastro_realizado = False
if 'dados_cliente' not in st.session_state:
    st.session_state.dados_cliente = {}
if 'erro_validacao' not in st.session_state:
    st.session_state.erro_validacao = False

def processar_envio():
    cnpj = st.session_state.in_cnpj
    razao = st.session_state.in_razao
    regime = st.session_state.in_regime
    faturamento = st.session_state.in_fat
    erp = st.session_state.in_erp

    if not cnpj or not razao or regime == "Selecione..." or faturamento == "Selecione...":
        st.session_state.erro_validacao = True
    else:
        st.session_state.erro_validacao = False
        time.sleep(1.5)
        st.session_state.dados_cliente = {
            "cnpj": cnpj,
            "razao": razao,
            "faturamento": faturamento,
            "erp": erp,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        st.session_state.cadastro_realizado = True

def resetar_tela():
    st.session_state.cadastro_realizado = False
    st.session_state.dados_cliente = {}
    st.session_state.erro_validacao = False

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CABEÇALHO DA TELA E SAUDAÇÃO                                         ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.markdown('<h1 class="bsb-logo">BSB Contabilidade</h1>', unsafe_allow_html=True)
st.markdown('<p class="bsb-slogan">Bem-vindo! Para darmos continuidade, precisamos realizar o seu cadastro financeiro.</p>', unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CARROSSEL DE SERVIÇOS 3D — High Standard                            ║
# ╚═══════════════════════════════════════════════════════════════════════╝
# Data de serviços BSB (fictícia mas baseada em site contábil)
SERVICES = [
    {
        "icon": "📊",
        "label": "ASSESSORIA CONTÁBIL",
        "description": "Organização da documentação contábil, emissão de balanços, balancetes e demonstrações financeiras."
    },
    {
        "icon": "📝",
        "label": "GESTÃO TRIBUTÁRIA",
        "description": "Planejamento tributário, apuração de impostos e entrega de obrigações acessórias."
    },
    {
        "icon": "👥",
        "label": "DEPARTAMENTO PESSOAL",
        "description": "Gestão da folha de pagamento, férias, décimo terceiro, admissões e demissões."
    },
    {
        "icon": "🚀",
        "label": "ABERTURA DE EMPRESA",
        "description": "Formalização completa de empresas, obtenção de CNPJ e alvarás."
    }
]

# Criando o HTML do carrossel dinamicamente com base nos dados
carousel_html = """
<div class="carousel-wrapper">
    <div class="carousel-track">
"""
for service in SERVICES:
    carousel_html += f"""
        <div class="carousel-card">
            <div class="carousel-icon">{service['icon']}</div>
            <div class="carousel-label">{service['label']}</div>
            <div class="carousel-description">{service['description']}</div>
        </div>
    """
carousel_html += """
    </div>
</div>
"""

# Renderiza o carrossel na página inicial
if not st.session_state.cadastro_realizado:
    st.markdown(carousel_html, unsafe_allow_html=True)

# Container principal após o carrossel
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  INTERFACE DO FORMULÁRIO                                              ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if not st.session_state.cadastro_realizado:
    st.markdown("<h3>1. Dados da Empresa</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.text_input("CNPJ *", placeholder="00.000.000/0000-00", key="in_cnpj")
    with col2:
        st.text_input("Razão Social *", placeholder="Sua Empresa LTDA", key="in_razao")
        
    col3, col4 = st.columns(2)
    with col3:
        st.text_input("WhatsApp do Gestor", placeholder="(00) 00000-0000", key="in_wpp")
    with col4:
        st.text_input("E-mail Financeiro", placeholder="financeiro@empresa.com", key="in_email")

    st.markdown("<h3>2. Perfil Operacional</h3>", unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    with col5:
        st.selectbox("Regime Tributário", ["Selecione...", "Simples Nacional", "Lucro Presumido", "Lucro Real"], key="in_regime")
        st.selectbox("Sistema de Gestão Atual (ERP)", ["Nenhum / Excel", "Conta Azul", "Omie", "Nibo", "Bling", "Outro"], key="in_erp")
    with col6:
        st.selectbox("Faturamento Médio Mensal", ["Selecione...", "Até R$ 20.000", "R$ 20.001 a R$ 100.000", "R$ 100.001 a R$ 500.000", "Acima de R$ 500.000"], key="in_fat")
        st.number_input("Volume médio de NFs emitidas/mês", min_value=0, step=10, key="in_notas")

    if st.session_state.erro_validacao:
        st.error("⚠️ Por favor, preencha os campos obrigatórios (*).")

    st.button("Finalizar Cadastro", on_click=processar_envio)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  TELA DE SUCESSO                                                      ║
# ╚═══════════════════════════════════════════════════════════════════════╝
else:
    st.success(f"✅ Cadastro finalizado com sucesso! Nossa equipe analisará seus dados e entrará em contato.")
    st.info("A BSB Contabilidade agradece a confiança. Um consultor enviará os próximos passos no seu WhatsApp.")
    st.balloons()
    
    st.button("⬅️ Novo Cadastro (Modo Demo)", on_click=resetar_tela)

st.markdown('</div>', unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  EASTER EGG: VISÃO INTERNA PARA A SUA REUNIÃO                         ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if st.session_state.cadastro_realizado:
    with st.expander("🔒 VISÃO INTERNA BSB (Mostrar na Reunião)"):
        st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Isso é o que o sistema de Back-office recebe:</p>", unsafe_allow_html=True)
        dados = st.session_state.dados_cliente
        
        # Mantendo as cores do SCORE baseadas em semântica de risco (verde pra bom, vermelho pra ruim)
        risco = "BAIXO"
        cor_risco = "#10b981" 
        recomendacao = "Fluxo padrão de Onboarding. Integração via API do ERP permitida."
        
        if dados['erp'] == "Nenhum / Excel" and dados['faturamento'] in ["R$ 100.001 a R$ 500.000", "Acima de R$ 500.000"]:
            risco = "CRÍTICO"
            cor_risco = "#ef4444"
            recomendacao = "Atenção: Alto volume financeiro sem sistema de gestão. Necessário cobrar taxa extra de setup para organização de passivo."
        elif dados['erp'] == "Nenhum / Excel":
            risco = "MÉDIO"
            cor_risco = "#f59e0b"
            recomendacao = "Cliente desestruturado. Necessário implantar Conta Azul ou Omie antes de iniciar o BPO."

        st.markdown(f"""
        <div style="background: #0b1e2e; padding: 15px; border-radius: 10px; border: 1px solid #334155;">
            <p style="margin: 0; color: #f1f5f9;"><strong>Novo Lead:</strong> {dados['razao']} ({dados['cnpj']})</p>
            <p style="margin: 0; color: #f1f5f9;"><strong>Faturamento Declarado:</strong> {dados['faturamento']}</p>
            <p style="margin: 0; color: #f1f5f9;"><strong>Sistema Atual:</strong> {dados['erp']}</p>
            <hr style="border-color: #334155;">
            <h4 style="color: #38bdf8; margin-bottom: 5px;">🤖 Motor de Inteligência</h4>
            <p style="margin: 0; color: #f1f5f9;">Score Operacional: <strong style='color: {cor_risco}; font-size: 1.1rem;'>{risco}</strong></p>
            <p style="margin: 0; color: #94a3b8; font-size: 0.85rem;">Ação Recomendada: {recomendacao}</p>
        </div>
        """, unsafe_allow_html=True)
