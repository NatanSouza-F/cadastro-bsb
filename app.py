import streamlit as st
import time
import requests
import re
from datetime import datetime

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURAÇÃO DA PÁGINA E UX/UI GLOBAL (PADRÃO BSB AZUL PREMIUM)      ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.set_page_config(page_title="BSB Contabilidade | Onboarding", page_icon="🏢", layout="centered")

# CSS NASA: Glassmorphism, Micro-interações, Acessibilidade e KYC Premium
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
        max-width: 560px !important; 
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
    h4 {
        color: #94a3b8 !important; font-size: 0.85rem !important; font-weight: 600 !important;
        margin-top: 10px; margin-bottom: 5px;
    }
    div[data-testid="column"] { padding: 0 8px; }

    /* Estilização do Radio Button (Seletor de Perfil) */
    div.stRadio > div[role="radiogroup"] {
        background: rgba(11, 30, 46, 0.6); padding: 5px; border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.3); display: flex; gap: 10px;
    }
    div.stRadio > div[role="radiogroup"] label {
        background: transparent !important; padding: 10px 20px; border-radius: 8px; transition: all 0.3s ease;
    }

    /* Inputs Glassmorphism Alto Contraste */
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
    
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stRadio label, .stCameraInput label, .stFileUploader label {
        color: #94a3b8 !important; font-size: 0.72rem !important; font-weight: 700 !important;
        text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px !important; padding-left: 2px;
    }

    /* Estilização File Uploader Premium */
    div[data-testid="stFileUploader"] {
        background: rgba(11, 30, 46, 0.6) !important;
        border: 1px dashed rgba(56, 189, 248, 0.5) !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }

    /* Estilização Câmera (Streamlit native camera widget hackeado) */
    div[data-testid="stCameraInput"] {
        background: rgba(11, 30, 46, 0.4) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 16px !important;
        padding: 16px !important;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.2) !important;
        margin-top: 10px !important;
    }
    div[data-testid="stCameraInput"] video,
    div[data-testid="stCameraInput"] img {
        border-radius: 12px !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
    div[data-testid="stCameraInput"] button {
        background: rgba(56, 189, 248, 0.1) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        color: #38bdf8 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin-top: 12px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stCameraInput"] button:hover {
        background: rgba(56, 189, 248, 0.25) !important;
        transform: translateY(-1px) !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       HACK VISUAL: BOTÕES DE SELEÇÃO DE MÉTODO (KYC)
       ═══════════════════════════════════════════════════════════════ */
    /* Estilizando o componente st.button para parecer o seletor da imagem do usuário */
    div.stButton > button[kind="secondary"] {
        background: rgba(11, 30, 46, 0.8) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 16px !important;
        color: #f1f5f9 !important;
        width: 100% !important;
        height: 80px !important; /* Mais alto igual à referência */
        font-size: 1rem !important;
        font-weight: 700 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-top: 0px !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: rgba(56, 189, 248, 0.9) !important;
        background: rgba(11, 30, 46, 1) !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(56, 189, 248, 0.15) !important;
    }
    div.stButton > button[kind="secondary"]:active {
        transform: translateY(-1px) scale(0.98) !important;
    }

    /* Botão CTA Principal */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: #ffffff !important; font-weight: 800; font-size: 1rem;
        border: none; border-radius: 12px; padding: 0.9rem 2rem; width: 100%;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-top: 20px; text-transform: uppercase; letter-spacing: 0.1em;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.01); box-shadow: 0 10px 30px rgba(14, 165, 233, 0.5);
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
if 'nome_fantasia_api' not in st.session_state:
    st.session_state.nome_fantasia_api = ""
if 'erro_validacao' not in st.session_state:
    st.session_state.erro_validacao = False
# Estado para rastrear o método de envio de documento escolhido (PF)
if 'doc_method' not in st.session_state:
    st.session_state.doc_method = None # 'Anexar' ou 'Foto'

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

def avancar_pf():
    st.session_state.etapa = 2 

# Callbacks para seleção de método de documento
def set_doc_anexar():
    st.session_state.doc_method = "Anexar"
def set_doc_foto():
    st.session_state.doc_method = "Foto"

def processar_envio_pj():
    razao = st.session_state.in_razao
    regime = st.session_state.in_regime
    faturamento = st.session_state.in_fat
    
    if not razao or regime == "Selecione..." or faturamento == "Selecione...":
        st.session_state.erro_validacao = True
    else:
        st.session_state.erro_validacao = False
        st.session_state.dados_cliente = {
            "tipo_cliente": "Pessoa Jurídica (PJ)",
            "documento": st.session_state.in_cnpj,
            "nome_principal": razao,
            "nome_fantasia": st.session_state.in_fantasia,
            "contato_wpp": st.session_state.in_wpp,
            "email": st.session_state.in_email,
            "funcionarios": st.session_state.in_func,
            "regime": regime,
            "faturamento": faturamento,
            "erp": st.session_state.in_erp,
            "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        st.session_state.cadastro_realizado = True

def processar_envio_pf(anexo_arquivo, foto_frente, foto_verso):
    cpf = st.session_state.in_cpf
    nome = st.session_state.in_nome_pf
    necessidade = st.session_state.in_necessidade
    
    # Validação inteligente de documentos
    doc_recebido = False
    if st.session_state.doc_method == "Anexar" and anexo_arquivo is not None:
        doc_recebido = True
        desc_doc = "📄 Arquivo Anexado (PDF/Imagem)"
    elif st.session_state.doc_method == "Foto" and foto_frente is not None and foto_verso is not None:
        doc_recebido = True
        desc_doc = "📸 Fotos Capturadas (Frente e Verso)"

    if not cpf or not nome or necessidade == "Selecione..." or not doc_recebido:
        st.session_state.erro_validacao = True
    else:
        st.session_state.erro_validacao = False
        st.session_state.dados_cliente = {
            "tipo_cliente": "Pessoa Física (PF)",
            "documento": cpf,
            "nome_principal": nome,
            "contato_wpp": st.session_state.in_wpp_pf,
            "email": st.session_state.in_email_pf,
            "profissao": st.session_state.in_prof,
            "renda_media": st.session_state.in_renda_pf,
            "necessidade_principal": necessidade,
            "metodo_kyc": st.session_state.doc_method,
            "documento_identificacao": desc_doc,
            "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        st.session_state.cadastro_realizado = True

def resetar_tela():
    st.session_state.etapa = 1
    st.session_state.cadastro_realizado = False
    st.session_state.dados_cliente = {}
    st.session_state.razao_social_api = ""
    st.session_state.nome_fantasia_api = ""
    st.session_state.erro_validacao = False
    st.session_state.doc_method = None

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
# ║  INTERFACE DO FORMULÁRIO (PROGRESSIVE DISCLOSURE MULTI-PERFIL)        ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if not st.session_state.cadastro_realizado:
    
    st.markdown("<h3>1. Qual é o seu perfil?</h3>", unsafe_allow_html=True)
    
    perfil_cliente = st.radio(
        "Selecione o tipo de cadastro:",
        ["🏢 Empresa (CNPJ)", "👤 Pessoa Física (CPF)"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # =====================================================================
    # FLUXO: EMPRESA (PJ)
    # =====================================================================
    if perfil_cliente == "🏢 Empresa (CNPJ)":
        
        col_cnpj, col_btn = st.columns([3, 1], gap="small")
        with col_cnpj:
            st.text_input("CNPJ da Empresa *", placeholder="00.000.000/0000-00", key="in_cnpj")
        with col_btn:
            # Botão de busca estilizado nativamente no CSS do formulário
            st.button("🔍 Buscar", on_click=buscar_cnpj_api, use_container_width=True, key="btn_buscar_cnpj")

        if st.session_state.etapa == 2:
            st.markdown("<h3>2. Dados Institucionais e Contato</h3>", unsafe_allow_html=True)
            
            col_r, col_f = st.columns([1, 1], gap="medium")
            with col_r:
                st.text_input("Razão Social *", value=st.session_state.razao_social_api, placeholder="Sua Empresa LTDA", key="in_razao")
            with col_f:
                st.text_input("Nome Fantasia", value=st.session_state.nome_fantasia_api, placeholder="Como a empresa é conhecida", key="in_fantasia")
                
            col3, col4 = st.columns([1, 1], gap="medium")
            with col3:
                st.text_input("WhatsApp do Gestor", placeholder="(00) 00000-0000", key="in_wpp")
            with col4:
                st.text_input("E-mail Comercial", placeholder="contato@empresa.com", key="in_email")

            st.markdown("<h3>3. Informações Operacionais</h3>", unsafe_allow_html=True)
            
            col_reg, col_func = st.columns([1, 1], gap="medium")
            with col_reg:
                st.selectbox("Regime Tributário", ["Selecione...", "Simples Nacional", "Lucro Presumido", "Lucro Real", "Não sei / MEI"], key="in_regime")
            with col_func:
                st.selectbox("Quantidade de Funcionários (Folha)", ["Nenhum (Sócios)", "1 a 5 funcionários", "6 a 20 funcionários", "Mais de 20 funcionários"], key="in_func")

            col5, col6 = st.columns([1, 1], gap="medium")
            with col5:
                st.selectbox("Faturamento Médio Mensal", ["Selecione...", "Até R$ 20.000", "R$ 20.001 a R$ 100.000", "R$ 100.001 a R$ 500.000", "Acima de R$ 500.000"], key="in_fat")
            with col6:
                st.selectbox("Sistema de Gestão (ERP)", ["Nenhum / Excel", "Conta Azul", "Omie", "Nibo", "Bling", "Outro"], key="in_erp")

            if st.session_state.erro_validacao:
                st.markdown('<div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.4); color: #ef4444; padding: 12px; border-radius: 8px; text-align: center; font-weight: 600; margin-top: 10px;">⚠️ Por favor, preencha todos os campos obrigatórios (*).</div>', unsafe_allow_html=True)

            st.button("Finalizar Cadastro Seguro", on_click=processar_envio_pj, type="primary", key="btn_finalizar_pj")

    # =====================================================================
    # FLUXO: PESSOA FÍSICA (PF) COM KYC PREMIUM (FLEXIBILIDADE)
    # =====================================================================
    elif perfil_cliente == "👤 Pessoa Física (CPF)":
        
        col_cpf, col_nome = st.columns([1, 2], gap="medium")
        with col_cpf:
            st.text_input("CPF *", placeholder="000.000.000-00", key="in_cpf")
        with col_nome:
            st.text_input("Nome Completo *", placeholder="Digite seu nome", key="in_nome_pf")

        st.button("Avançar", on_click=avancar_pf, use_container_width=True, key="btn_avancar_pf")

        if st.session_state.etapa == 2:
            st.markdown("<h3>2. Contato e Perfil</h3>", unsafe_allow_html=True)
            
            col_c1, col_c2 = st.columns([1, 1], gap="medium")
            with col_c1:
                st.text_input("WhatsApp", placeholder="(00) 00000-0000", key="in_wpp_pf")
            with col_c2:
                st.text_input("E-mail Pessoal", placeholder="seuemail@gmail.com", key="in_email_pf")

            # ══════════════════════════════════════════════════════════════
            # NOVA SEÇÃO 3: KYC PREMIUM - SELEÇÃO DE MÉTODO (REFERÊNCIA DO USUÁRIO)
            # ══════════════════════════════════════════════════════════════
            st.markdown("<h3>3. Validação de Segurança (KYC)</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color:#94a3b8; font-size: 0.85rem; margin-top: -10px; margin-bottom: 20px;'>Para darmos início ao contrato, precisamos de uma cópia do seu documento (RG ou CNH). Escolha como prefere enviar:</p>", unsafe_allow_html=True)
            
            # Botões de Seleção (Hacked CSS para parecer a imagem do usuário)
            col_anexo, col_foto = st.columns(2, gap="medium")
            with col_anexo:
                st.button("👤 Anexar Documento\n(PDF ou Imagem existente)", on_click=set_doc_anexar, key="btn_method_anexar", kind="secondary", use_container_width=True)
            with col_foto:
                st.button("📸 Tirar Foto Agora\n(Usar Câmera do Celular)", on_click=set_doc_foto, key="btn_method_foto", kind="secondary", use_container_width=True)

            # Inicializa variáveis dos documentos como None
            documento_arquivo = None
            foto_frente = None
            foto_verso = None

            # Renderiza o componente baseado na escolha ( Progressive Disclosure)
            if st.session_state.doc_method == "Anexar":
                st.markdown("<h4>Selecione o arquivo do documento (Frente e Verso juntos ou separados)</h4>", unsafe_allow_html=True)
                documento_arquivo = st.file_uploader("Enviar Arquivo *", type=['pdf', 'jpg', 'jpeg', 'png'], key="in_uploader", label_visibility="collapsed")
                if documento_arquivo:
                    st.toast("✅ Arquivo carregado. Preencha os dados finais.")

            elif st.session_state.doc_method == "Foto":
                st.markdown("<h4>Tire a foto da FRENTE (com boa luz)</h4>", unsafe_allow_html=True)
                foto_frente = st.camera_input("📸 Frente do Documento", key="in_camera_frente", label_visibility="hidden")
                
                # Só mostra o verso depois que tirou a frente (melhora fluxo)
                if foto_frente:
                    st.toast("Frente capturada! Agora o Verso.")
                    st.markdown("<h4>Tire a foto do VERSO</h4>", unsafe_allow_html=True)
                    foto_verso = st.camera_input("📸 Verso do Documento", key="in_camera_verso", label_visibility="hidden")
                    if foto_verso:
                        st.toast("✅ Fotos capturadas. Preencha os dados finais.")

            st.markdown("<h3>4. Qual a sua necessidade?</h3>", unsafe_allow_html=True)

            col_p1, col_p2 = st.columns([1, 1], gap="medium")
            with col_p1:
                st.text_input("Profissão / Ocupação Principal", placeholder="Ex: Médico, Advogado, Autônomo...", key="in_prof")
            with col_p2:
                st.selectbox("Renda Média Mensal", ["Até R$ 3.000", "R$ 3.001 a R$ 8.000", "R$ 8.001 a R$ 15.000", "Acima de R$ 15.000"], key="in_renda_pf")

            st.selectbox("Como a BSB pode te ajudar hoje? *", [
                "Selecione...", 
                "Declaração de Imposto de Renda (IRPF)", 
                "Cálculo de Carnê Leão / Autônomo", 
                "Quero abrir uma Empresa (Transformar em PJ)", 
                "Planejamento Tributário / Outros"
            ], key="in_necessidade")

            if st.session_state.erro_validacao:
                if not st.session_state.doc_method or (st.session_state.doc_method == "Foto" and (not foto_frente or not foto_verso)) or (st.session_state.doc_method == "Anexar" and not documento_arquivo):
                     st.markdown('<div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.4); color: #ef4444; padding: 12px; border-radius: 8px; text-align: center; font-weight: 600; margin-top: 10px;">⚠️ Por favor, envie seu documento de identificação (Anexo ou Foto Frente/Verso) e preencha os campos obrigatórios (*).</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.4); color: #ef4444; padding: 12px; border-radius: 8px; text-align: center; font-weight: 600; margin-top: 10px;">⚠️ Por favor, preencha todos os campos obrigatórios (*).</div>', unsafe_allow_html=True)

            st.button("Finalizar Cadastro Seguro", on_click=processar_envio_pf, args=(documento_arquivo, foto_frente, foto_verso), type="primary", key="btn_finalizar_pf")

    # Selo Trust & Compliance (LGPD)
    if st.session_state.etapa == 2:
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
    with st.spinner("Criptografando, processando arquivos e estruturando dados..."):
        time.sleep(2.0)
    st.success(f"✅ Ficha de Cadastro estruturada com sucesso!")
    st.info("A BSB Contabilidade agradece a confiança. Nossa equipe técnica analisará seus dados e arquivos e entrará em contato.")
    st.balloons()
    
    st.button("⬅️ Novo Cadastro (Modo Demo)", on_click=resetar_tela)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  EASTER EGG: ESTRUTURAÇÃO DE DADOS (VISÃO INTERNA/BANCO DE DADOS)     ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if st.session_state.cadastro_realizado:
    with st.expander("🔒 VISÃO INTERNA DO BANCO DE DADOS (Mostrar na Reunião)"):
        st.markdown("<p style='color: #94a3b8; font-size: 0.85rem;'>Este é o formato JSON estruturado pronto para ser enviado ao Banco de Dados Relacional (PostgreSQL/MySQL) do escritório, incluindo os metadados dos documentos coletados:</p>", unsafe_allow_html=True)
        
        dados = st.session_state.dados_cliente
        st.json(dados)
        
        st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #38bdf8; margin-bottom: 5px;'>🤖 Automação Operacional</h4>", unsafe_allow_html=True)
        
        if dados['tipo_cliente'] == "Pessoa Jurídica (PJ)":
            st.markdown(f"<p style='color: #f1f5f9; font-size: 0.9rem;'>Lead PJ capturado. Alerta enviado ao setor <strong>Societário / Fiscal</strong>.</p>", unsafe_allow_html=True)
        else:
            if "abrir uma Empresa" in dados.get('necessidade_principal', ''):
                st.markdown(f"<p style='color: #10b981; font-size: 0.9rem;'><strong>ALERTA DE VENDA:</strong> Cliente deseja transformar CPF em CNPJ. Notificar o time Societário/Comercial imediatamente.</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='color: #f1f5f9; font-size: 0.9rem;'>Lead PF capturado. Alerta enviado ao setor de <strong>Imposto de Renda / Assessoria Pessoal</strong>.</p>", unsafe_allow_html=True)
