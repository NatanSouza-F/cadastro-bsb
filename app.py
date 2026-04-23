import streamlit as st
import time
import requests
import re
from datetime import datetime

╔═══════════════════════════════════════════════════════════════════════╗

║  CONFIGURAÇÃO DA PÁGINA E UX/UI GLOBAL (PADRÃO BSB AZUL PREMIUM)      ║

╚═══════════════════════════════════════════════════════════════════════╝

st.set_page_config(page_title="BSB Contabilidade | Onboarding", page_icon="🏢", layout="centered")

CSS NASA: Glassmorphism, Micro-interações, Acessibilidade e LGPD

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
    .block-container { max-width: 560px !important; padding: 3rem 1rem 1rem 1rem !important; }  
    h1, h2, h3, h4, p, span, div, label { color: #f1f5f9; }  
  
    .bsb-logo {  
        font-size: 2.6rem; font-weight: 900;  
        background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 50%, #2563eb 100%);  
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;  
        text-align: center; margin: 0; letter-spacing: -0.04em;  
        filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.2));  
    }  
    .bsb-slogan {  
        text-align: center; color: #94a3b8 !important; font-size: 1.05rem;  
        font-weight: 500; line-height: 1.5; margin-top: 12px; margin-bottom: 2rem; padding: 0 10px;  
    }  
  
    /* CARROSSEL 3D */  
    .carousel-wrapper { position: relative; width: 100%; height: 180px; margin: 10px 0 40px 0; perspective: 1200px; overflow: hidden; }  
    .carousel-track { position: relative; width: 100%; height: 100%; transform-style: preserve-3d; }  
    .carousel-card {  
        position: absolute; top: 0; left: 50%; width: 280px; height: 160px; margin-left: -140px;  
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);  
        border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 20px; padding: 20px 24px;  
        box-shadow: 0 20px 40px rgba(56, 189, 248, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.05);  
        display: flex; flex-direction: column; justify-content: space-between; opacity: 0; cursor: pointer;  
        animation: carousel-slide 25s infinite ease-in-out;   
    }  
    .carousel-card::before {  
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;  
        background: linear-gradient(90deg, transparent, #38bdf8, transparent); opacity: 0.8;  
    }  
    .carousel-wrapper:hover .carousel-card, .carousel-wrapper:active .carousel-card { animation-play-state: paused !important; }  
    .carousel-card:nth-child(1) { animation-delay: 0s; } .carousel-card:nth-child(2) { animation-delay: 5s; }  
    .carousel-card:nth-child(3) { animation-delay: 10s; } .carousel-card:nth-child(4) { animation-delay: 15s; }  
    .carousel-card:nth-child(5) { animation-delay: 20s; }  
    @keyframes carousel-slide {  
        0% { opacity: 0; transform: translateX(100px) scale(0.9); } 4% { opacity: 1; transform: translateX(0) scale(1); }  
        16% { opacity: 1; transform: translateX(0) scale(1); } 20% { opacity: 0; transform: translateX(-100px) scale(0.9); }  
        100% { opacity: 0; transform: translateX(-100px) scale(0.9); }  
    }  
    .carousel-icon { font-size: 1.8rem; line-height: 1; margin-bottom: 2px;}  
    .carousel-label { font-size: 0.72rem; font-weight: 700; color: #38bdf8 !important; letter-spacing: 0.12em; margin-bottom: -10px; }  
    .carousel-description { font-size: 0.8rem; color: #f1f5f9 !important; font-weight: 400; margin: 4px 0; line-height: 1.3; }  
  
    /* UI NASA: FORMULÁRIO */  
    h3 {  
        display: inline-block; background: rgba(56, 189, 248, 0.1); color: #38bdf8 !important;  
        padding: 10px 20px 10px 24px !important; border-radius: 8px; font-size: 0.85rem !important; font-weight: 800 !important;  
        letter-spacing: 0.15em; text-transform: uppercase; border-left: 4px solid #38bdf8;  
        margin-top: 1rem !important; margin-bottom: 1.5rem !important; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.05);  
    }  
    div[data-testid="column"] { padding: 0 8px; }  
    div.stRadio > div[role="radiogroup"] {  
        background: rgba(11, 30, 46, 0.6); padding: 5px; border-radius: 12px;  
        border: 1px solid rgba(56, 189, 248, 0.3); display: flex; gap: 10px;  
    }  
    div.stRadio > div[role="radiogroup"] label { background: transparent !important; padding: 10px 20px; border-radius: 8px; transition: all 0.3s ease; }  
  
    /* Inputs */  
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-baseweb="number-input"] > div {  
        background: rgba(11, 30, 46, 0.6) !important; backdrop-filter: blur(10px);  
        border: 1px solid rgba(148, 163, 184, 0.3) !important; border-radius: 10px !important; transition: all 0.3s ease;  
    }  
    div[data-baseweb="select"] > div:hover, div[data-baseweb="select"] > div:focus-within,  
    div[data-baseweb="input"] > div:hover, div[data-baseweb="input"] > div:focus-within,  
    div[data-baseweb="number-input"] > div:hover, div[data-baseweb="number-input"] > div:focus-within {  
        background: rgba(11, 30, 46, 0.9) !important; border-color: rgba(56, 189, 248, 0.8) !important;  
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.15);  
    }  
    input, select, div[data-baseweb="select"] span { color: #e2e8f0 !important; font-size: 0.9rem !important; font-weight: 500 !important; }  
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stRadio label, .stCameraInput label, .stFileUploader label, .stCheckbox label {  
        color: #94a3b8 !important; font-size: 0.72rem !important; font-weight: 700 !important;  
        text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px !important; padding-left: 2px;  
    }  
      
    /* Checkbox Premium */  
    div[data-testid="stCheckbox"] { padding: 5px 0 10px 5px; }  
  
    /* Uploader & Câmera */  
    div[data-testid="stFileUploader"] { background: rgba(11, 30, 46, 0.6) !important; border: 1px dashed rgba(56, 189, 248, 0.5) !important; border-radius: 12px !important; padding: 10px !important; }  
    div[data-testid="stCameraInput"] { background: rgba(11, 30, 46, 0.4) !important; border: 1px solid rgba(56, 189, 248, 0.2) !important; border-radius: 16px !important; padding: 16px !important; box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.2) !important; margin-top: 10px !important; }  
    div[data-testid="stCameraInput"] video, div[data-testid="stCameraInput"] img { border-radius: 12px !important; border: 1px solid rgba(148, 163, 184, 0.1) !important; }  
    div[data-testid="stCameraInput"] button { background: rgba(56, 189, 248, 0.1) !important; border: 1px solid rgba(56, 189, 248, 0.3) !important; color: #38bdf8 !important; border-radius: 8px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; margin-top: 12px !important; transition: all 0.3s ease !important; }  
    div[data-testid="stCameraInput"] button:hover { background: rgba(56, 189, 248, 0.25) !important; transform: translateY(-1px) !important; }  
  
    /* Botões */  
    div.stButton > button[kind="secondary"] { background: rgba(11, 30, 46, 0.8) !important; border: 1px solid rgba(56, 189, 248, 0.3) !important; border-radius: 16px !important; color: #f1f5f9 !important; width: 100% !important; height: 80px !important; font-size: 1rem !important; font-weight: 700 !important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; margin-top: 0px !important; }  
    div.stButton > button[kind="secondary"]:hover { border-color: rgba(56, 189, 248, 0.9) !important; background: rgba(11, 30, 46, 1) !important; transform: translateY(-3px) scale(1.02) !important; box-shadow: 0 10px 30px rgba(56, 189, 248, 0.15) !important; }  
    div.stButton > button[kind="secondary"]:active { transform: translateY(-1px) scale(0.98) !important; }  
      
    div[data-testid="stButton"] button[kind="primary"] { background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); color: #ffffff !important; font-weight: 800; font-size: 1rem; border: none; border-radius: 12px; padding: 0.9rem 2rem; width: 100%; box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); margin-top: 20px; text-transform: uppercase; letter-spacing: 0.1em; }  
    div[data-testid="stButton"] button[kind="primary"]:hover { transform: translateY(-3px) scale(1.01); box-shadow: 0 10px 30px rgba(14, 165, 233, 0.5); background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%); }  
  
    /* Badges & Expanders */  
    .lgpd-badge { display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 15px; color: #64748b; font-size: 0.75rem; font-weight: 500; }  
    .lgpd-badge svg { fill: #64748b; width: 14px; height: 14px; }  
    div[data-testid="stExpander"] { background: #1a2e42; border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; margin-top: 40px; }  
    div[data-testid="stExpander"] summary p { color: #38bdf8 !important; font-weight: 700; letter-spacing: 0.05em; }  
</style>  """, unsafe_allow_html=True)

╔═══════════════════════════════════════════════════════════════════════╗

║  LÓGICA E ESTADO                                                      ║

╚═══════════════════════════════════════════════════════════════════════╝

if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'cadastro_realizado' not in st.session_state: st.session_state.cadastro_realizado = False
if 'dados_cliente' not in st.session_state: st.session_state.dados_cliente = {}
if 'razao_social_api' not in st.session_state: st.session_state.razao_social_api = ""
if 'nome_fantasia_api' not in st.session_state: st.session_state.nome_fantasia_api = ""
if 'erro_validacao' not in st.session_state: st.session_state.erro_validacao = False
if 'doc_method' not in st.session_state: st.session_state.doc_method = None

def buscar_cnpj_api():
cnpj_raw = st.session_state.in_cnpj
cnpj_limpo = re.sub(r'\D', '', cnpj_raw)
if len(cnpj_limpo) == 14:
try:
response = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}", timeout=5)
if response.status_code == 200:
dados = response.json()
st.session_state.razao_social_api = dados.get("razao_social", "")
st.session_state.nome_fantasia_api = dados.get("nome_fantasia", "")
st.toast("✅ Empresa localizada com sucesso na Receita Federal!")
else:
st.session_state.razao_social_api = ""
st.session_state.nome_fantasia_api = ""
except:
pass
st.session_state.etapa = 2

def avancar_pf(): st.session_state.etapa = 2
def set_doc_anexar(): st.session_state.doc_method = "Anexar"
def set_doc_foto(): st.session_state.doc_method = "Foto"

def processar_envio_pj():
razao = st.session_state.in_razao
nome_socio = st.session_state.in_socio_nome
cpf_socio = st.session_state.in_socio_cpf

if not razao or not nome_socio or not cpf_socio or st.session_state.in_regime == "Selecione..." or st.session_state.in_fat == "Selecione...":  
    st.session_state.erro_validacao = True  
else:  
    st.session_state.erro_validacao = False  
    st.session_state.dados_cliente = {  
        "tipo_cliente": "Pessoa Jurídica (PJ)",  
        "documento_cnpj": st.session_state.in_cnpj,  
        "razao_social": razao,  
        "nome_fantasia": st.session_state.in_fantasia,  
        "segmento_atuacao": st.session_state.in_segmento,  
        "cep": st.session_state.in_cep_pj,  
        "socio_responsavel": nome_socio,  
        "cpf_socio": cpf_socio,  
        "contato_wpp": st.session_state.in_wpp,  
        "email": st.session_state.in_email,  
        "funcionarios": st.session_state.in_func,  
        "regime": st.session_state.in_regime,  
        "faturamento": st.session_state.in_fat,  
        "erp": st.session_state.in_erp,  
        "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M:%S")  
    }  
    st.session_state.cadastro_realizado = True

def processar_envio_pf(anexo_arquivo, foto_frente, foto_verso):
cpf = st.session_state.in_cpf
nome = st.session_state.in_nome_pf
necessidade = st.session_state.in_necessidade

doc_recebido = False  
desc_doc = "❌ Não anexado"  
if st.session_state.doc_method == "Anexar" and anexo_arquivo is not None:  
    doc_recebido = True; desc_doc = "📄 Arquivo Anexado"  
elif st.session_state.doc_method == "Foto" and foto_frente is not None and foto_verso is not None:  
    doc_recebido = True; desc_doc = "📸 Fotos Capturadas (F/V)"  

if not cpf or not nome or necessidade == "Selecione..." or not doc_recebido:  
    st.session_state.erro_validacao = True  
else:  
    st.session_state.erro_validacao = False  
    st.session_state.dados_cliente = {  
        "tipo_cliente": "Pessoa Física (PF)",  
        "documento_cpf": cpf,  
        "nome_completo": nome,  
        "estado_civil": st.session_state.in_estado_civil,  
        "dependentes": st.session_state.in_dependentes,  
        "cep": st.session_state.in_cep_pf,  
        "contato_wpp": st.session_state.in_wpp_pf,  
        "email": st.session_state.in_email_pf,  
        "profissao": st.session_state.in_prof,  
        "renda_media": st.session_state.in_renda_pf,  
        "investidor_bolsa_cripto": "Sim" if st.session_state.in_investidor else "Não",  
        "necessidade_principal": necessidade,  
        "documento_identificacao": desc_doc,  
        "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M:%S")  
    }  
    st.session_state.cadastro_realizado = True

def resetar_tela():
st.session_state.etapa = 1; st.session_state.cadastro_realizado = False
st.session_state.dados_cliente = {}; st.session_state.razao_social_api = ""
st.session_state.nome_fantasia_api = ""; st.session_state.erro_validacao = False; st.session_state.doc_method = None

╔═══════════════════════════════════════════════════════════════════════╗

║  INTERFACE PRINCIPAL                                                  ║

╚═══════════════════════════════════════════════════════════════════════╝

st.markdown('<h1 class="bsb-logo">BSB Contabilidade</h1>', unsafe_allow_html=True)
st.markdown('<p class="bsb-slogan">Seja bem-vindo(a)! Para darmos continuidade ao seu processo, solicitamos o preenchimento das informações a seguir:</p>', unsafe_allow_html=True)

CARROSSEL 3D

carousel_html = """

<div class="carousel-wrapper">  
    <div class="carousel-track">  
        <div class="carousel-card"><div class="carousel-icon">🏢</div><div class="carousel-label">SOCIETÁRIO</div><div class="carousel-description">Todo negócio precisa estar juridicamente em dia para garantir segurança e conformidade.</div></div>  
        <div class="carousel-card"><div class="carousel-icon">💰</div><div class="carousel-label">RECUPERAÇÃO DE CRÉDITOS</div><div class="carousel-description">Você sabia que sua empresa pode ter valores pagos indevidamente a serem recuperados?</div></div>  
        <div class="carousel-card"><div class="carousel-icon">🧾</div><div class="carousel-label">DEPARTAMENTO FISCAL</div><div class="carousel-description">O cenário tributário brasileiro é desafiador, mas ajudamos na correta apuração e entrega.</div></div>  
        <div class="carousel-card"><div class="carousel-icon">👥</div><div class="carousel-label">DEPARTAMENTO PESSOAL</div><div class="carousel-description">Gerenciar pessoas exige atenção constante à legislação trabalhista e previdenciária.</div></div>  
        <div class="carousel-card"><div class="carousel-label">📊</div><div class="carousel-label">CONTABILIDADE</div><div class="carousel-description">Na BSB Contabilidade, tratamos a contabilidade como uma ferramenta de gestão.</div></div>  
    </div>  
    <div style="text-align: center; color: #64748b; font-size: 0.65rem; margin-top: 155px; opacity: 0.7;">👉 Pressione ou passe o mouse no card para pausar a leitura</div>  
</div>  
"""  
if not st.session_state.cadastro_realizado: st.markdown(carousel_html, unsafe_allow_html=True)  ╔═══════════════════════════════════════════════════════════════════════╗

║  FORMULÁRIO (PROGRESSIVE DISCLOSURE MULTI-PERFIL)                     ║

╚═══════════════════════════════════════════════════════════════════════╝

if not st.session_state.cadastro_realizado:
st.markdown("<h3>1. Qual é o seu perfil?</h3>", unsafe_allow_html=True)
perfil_cliente = st.radio("Selecione:", ["🏢 Empresa (CNPJ)", "👤 Pessoa Física (CPF)"], horizontal=True, label_visibility="collapsed")

# ================= EMPRESA (PJ) =================  
if perfil_cliente == "🏢 Empresa (CNPJ)":  
    col_cnpj, col_btn = st.columns([3, 1], gap="small")  
    with col_cnpj: st.text_input("CNPJ da Empresa *", placeholder="00.000.000/0000-00", key="in_cnpj")  
    with col_btn: st.button("🔍 Buscar", on_click=buscar_cnpj_api, use_container_width=True)  

    if st.session_state.etapa == 2:  
        st.markdown("<h3>2. Dados Institucionais e Contato</h3>", unsafe_allow_html=True)  
        col_r, col_f = st.columns([1, 1], gap="medium")  
        with col_r: st.text_input("Razão Social *", value=st.session_state.razao_social_api, placeholder="Sua Empresa LTDA", key="in_razao")  
        with col_f: st.text_input("Nome Fantasia", value=st.session_state.nome_fantasia_api, placeholder="Como é conhecida", key="in_fantasia")  
          
        st.selectbox("Segmento Principal de Atuação", ["Selecione...", "Prestação de Serviços", "Comércio / Varejo", "Indústria", "Tecnologia / Startup", "Saúde / Clínicas"], key="in_segmento")  
          
        col_w, col_e = st.columns([1, 1], gap="medium")  
        with col_w: st.text_input("WhatsApp do Gestor", placeholder="(00) 00000-0000", key="in_wpp")  
        with col_e: st.text_input("E-mail Comercial", placeholder="contato@empresa.com", key="in_email")  

        # NOVOS CAMPOS COMERCIAIS (Representante e Endereço)  
        st.markdown("<h3>3. Representante Legal</h3>", unsafe_allow_html=True)  
        st.text_input("Nome do Sócio Responsável (Para Contrato) *", placeholder="Nome completo do assinante legal", key="in_socio_nome")  
        col_socio, col_cep = st.columns([1, 1], gap="medium")  
        with col_socio: st.text_input("CPF do Sócio *", placeholder="000.000.000-00", key="in_socio_cpf")  
        with col_cep: st.text_input("CEP da Empresa *", placeholder="00000-000", key="in_cep_pj")  

        st.markdown("<h3>4. Informações Operacionais</h3>", unsafe_allow_html=True)  
        col_reg, col_func = st.columns([1, 1], gap="medium")  
        with col_reg: st.selectbox("Regime Tributário *", ["Selecione...", "Simples Nacional", "Lucro Presumido", "Lucro Real", "Não sei / MEI"], key="in_regime")  
        with col_func: st.selectbox("Qtde. de Funcionários (DP) *", ["Nenhum (Sócios)", "1 a 5 funcionários", "6 a 20 funcionários", "Mais de 20 funcionários"], key="in_func")  
          
        col_fat, col_erp = st.columns([1, 1], gap="medium")  
        with col_fat: st.selectbox("Faturamento Mensal *", ["Selecione...", "Até R$ 20.000", "R$ 20.001 a R$ 100.000", "R$ 100.001 a R$ 500.000", "Acima de R$ 500.000"], key="in_fat")  
        with col_erp: st.selectbox("Sistema de Gestão (ERP)", ["Nenhum / Excel", "Conta Azul", "Omie", "Nibo", "Bling", "Outro"], key="in_erp")  

        if st.session_state.erro_validacao:  
            st.markdown('<div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.4); color: #ef4444; padding: 12px; border-radius: 8px; text-align: center; font-weight: 600; margin-top: 10px;">⚠️ Preencha todos os campos obrigatórios (*).</div>', unsafe_allow_html=True)  

        st.button("Finalizar Cadastro Seguro", on_click=processar_envio_pj, type="primary")  

# ================= PESSOA FÍSICA (PF) =================  
elif perfil_cliente == "👤 Pessoa Física (CPF)":  
    col_cpf, col_nome = st.columns([1, 2], gap="medium")  
    with col_cpf: st.text_input("CPF *", placeholder="000.000.000-00", key="in_cpf")  
    with col_nome: st.text_input("Nome Completo *", placeholder="Digite seu nome", key="in_nome_pf")  
    st.button("Avançar", on_click=avancar_pf, use_container_width=True)  

    if st.session_state.etapa == 2:  
        st.markdown("<h3>2. Contato e Perfil</h3>", unsafe_allow_html=True)  
        col_c1, col_c2 = st.columns([1, 1], gap="medium")  
        with col_c1: st.text_input("WhatsApp", placeholder="(00) 00000-0000", key="in_wpp_pf")  
        with col_c2: st.text_input("E-mail Pessoal", placeholder="seuemail@gmail.com", key="in_email_pf")  

        # NOVOS CAMPOS COMERCIAIS (IRPF e Complexidade)  
        col_civ, col_dep = st.columns([1, 1], gap="medium")  
        with col_civ: st.selectbox("Estado Civil", ["Solteiro(a)", "Casado(a) / União Estável", "Divorciado(a)", "Viúvo(a)"], key="in_estado_civil")  
        with col_dep: st.selectbox("Possui Dependentes?", ["Não", "Sim (1 dependente)", "Sim (2 dependentes)", "Sim (3 ou mais)"], key="in_dependentes")  
          
        st.text_input("CEP de Residência", placeholder="00000-000", key="in_cep_pf")  
        st.checkbox("📈 Opero ou já operei na Bolsa de Valores / Criptomoedas", key="in_investidor")  

        # KYC  
        st.markdown("<h3>3. Validação de Segurança (KYC)</h3>", unsafe_allow_html=True)  
        st.markdown("<p style='color:#94a3b8; font-size: 0.85rem; margin-top:-10px; margin-bottom:20px;'>Envie uma cópia do seu documento (RG ou CNH). Escolha como prefere enviar:</p>", unsafe_allow_html=True)  
          
        col_anexo, col_foto = st.columns(2, gap="medium")  
        with col_anexo: st.button("👤 Anexar Documento\n(PDF/Imagem)", on_click=set_doc_anexar, type="secondary", use_container_width=True)  
        with col_foto: st.button("📸 Tirar Foto Agora\n(Celular/Webcam)", on_click=set_doc_foto, type="secondary", use_container_width=True)  

        documento_arquivo = foto_frente = foto_verso = None  
        if st.session_state.doc_method == "Anexar":  
            st.markdown("<h4>Selecione o arquivo (Frente e Verso)</h4>", unsafe_allow_html=True)  
            documento_arquivo = st.file_uploader("Enviar Arquivo *", type=['pdf', 'jpg', 'jpeg', 'png'], key="in_uploader", label_visibility="collapsed")  
        elif st.session_state.doc_method == "Foto":  
            st.markdown("<h4>Tire a foto da FRENTE (com boa luz)</h4>", unsafe_allow_html=True)  
            foto_frente = st.camera_input("📸 Frente", key="in_camera_frente", label_visibility="hidden")  
            if foto_frente:  
                st.markdown("<h4>Tire a foto do VERSO</h4>", unsafe_allow_html=True)  
                foto_verso = st.camera_input("📸 Verso", key="in_camera_verso", label_visibility="hidden")  

        st.markdown("<h3>4. Qual a sua necessidade?</h3>", unsafe_allow_html=True)  
        col_p1, col_p2 = st.columns([1, 1], gap="medium")  
        with col_p1: st.text_input("Profissão / Ocupação Principal", placeholder="Ex: Médico, Advogado...", key="in_prof")  
        with col_p2: st.selectbox("Renda Média Mensal", ["Até R$ 3.000", "R$ 3.001 a R$ 8.000", "R$ 8.001 a R$ 15.000", "Acima de R$ 15.000"], key="in_renda_pf")  

        st.selectbox("Como a BSB pode te ajudar hoje? *", ["Selecione...", "Declaração de Imposto de Renda (IRPF)", "Cálculo de Carnê Leão / Autônomo", "Quero abrir uma Empresa (Transformar em PJ)", "Planejamento Tributário / Outros"], key="in_necessidade")  

        if st.session_state.erro_validacao:  
             st.markdown('<div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.4); color: #ef4444; padding: 12px; border-radius: 8px; text-align: center; font-weight: 600; margin-top: 10px;">⚠️ Envie seu documento (KYC) e preencha os campos obrigatórios (*).</div>', unsafe_allow_html=True)  

        st.button("Finalizar Cadastro Seguro", on_click=processar_envio_pf, args=(documento_arquivo, foto_frente, foto_verso), type="primary")  

if st.session_state.etapa == 2:  
    st.markdown('<div class="lgpd-badge"><svg viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>Ambiente criptografado e 100% aderente à LGPD.</div>', unsafe_allow_html=True)

╔═══════════════════════════════════════════════════════════════════════╗

║  TELA DE SUCESSO & VISÃO INTERNA DO BANCO DE DADOS                    ║

╚═══════════════════════════════════════════════════════════════════════╝

else:
with st.spinner("Criptografando, processando arquivos e estruturando dados..."): time.sleep(2.0)
st.success(f"✅ Ficha de Cadastro estruturada com sucesso!")
st.info("A BSB Contabilidade agradece a confiança. Nossa equipe analisará seus dados e entrará em contato.")
st.button("⬅️ Novo Cadastro (Modo Demo)", on_click=resetar_tela)

with st.expander("🔒 VISÃO INTERNA DO BANCO DE DADOS (Mostrar na Reunião)"):  
    st.markdown("<p style='color: #94a3b8; font-size: 0.85rem;'>JSON estruturado pronto para ERP/CRM:</p>", unsafe_allow_html=True)  
    st.json(st.session_state.dados_cliente)  
      
    st.markdown("<hr style='border-color: #334155;'><h4 style='color: #38bdf8; margin-bottom: 5px;'>🤖 Automação de Back-office</h4>", unsafe_allow_html=True)  
    dados = st.session_state.dados_cliente  
      
    if dados['tipo_cliente'] == "Pessoa Jurídica (PJ)":  
        if dados['regime'] == "Lucro Real": st.markdown(f"<p style='color: #f59e0b; font-size: 0.9rem;'>⚠️ <strong>ALERTA COMPLEXIDADE:</strong> Empresa do Lucro Real. Direcionar para Consultoria Tributária Sênior.</p>", unsafe_allow_html=True)  
        else: st.markdown(f"<p style='color: #10b981; font-size: 0.9rem;'>✅ Lead PJ Padrão. Alerta enviado ao setor Societário/Fiscal.</p>", unsafe_allow_html=True)  
    else:  
        if "abrir uma Empresa" in dados.get('necessidade_principal', ''):  
            st.markdown(f"<p style='color: #10b981; font-size: 0.9rem;'>🚀 <strong>ALERTA DE VENDA (UPSELL):</strong> Cliente deseja transformar CPF em CNPJ. Notificar o Societário para abertura.</p>", unsafe_allow_html=True)  
        elif dados.get('investidor_bolsa_cripto') == "Sim":  
            st.markdown(f"<p style='color: #f59e0b; font-size: 0.9rem;'>📈 <strong>ALERTA DE COMPLEXIDADE IRPF:</strong> Cliente opera Bolsa/Cripto. Direcionar para especialista em Renda Variável (Ticket Médio Maior).</p>", unsafe_allow_html=True)  
        else:  
            st.markdown(f"<p style='color: #f1f5f9; font-size: 0.9rem;'>✅ Lead PF Padrão. Alerta enviado ao setor de Imposto de Renda.</p>", unsafe_allow_html=True)
