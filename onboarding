import streamlit as st
import time
import random
from datetime import datetime

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURAÇÃO DA PÁGINA E UX/UI GLOBAL                                ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.set_page_config(page_title="BSB Contabilidade | Onboarding", page_icon="🏢", layout="centered")

# CSS customizado para tirar a "cara de dashboard" e dar "cara de aplicativo web"
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif !important; }

    /* Fundo clean e corporativo */
    .stApp {
        background-color: #f8fafc;
    }

    /* Container do formulário */
    div[data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 2.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }

    h1 {
        color: #0f172a;
        text-align: center;
        font-weight: 800;
        font-size: 2.2rem;
        padding-bottom: 0;
    }
    
    .subtitle {
        color: #64748b;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Títulos de sessão */
    h3 {
        color: #0284c7 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 8px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    /* Botão de Envio */
    div[data-testid="stFormSubmitButton"] button {
        background-color: #0284c7;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        width: 100%;
        transition: all 0.2s ease;
    }
    
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #0369a1;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CABEÇALHO                                                            ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.markdown("<h1>BSB Contabilidade</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Digital Onboarding - BPO Financeiro</div>", unsafe_allow_html=True)

# Variável de estado para controlar a visualização do painel interno
if 'cadastro_realizado' not in st.session_state:
    st.session_state.cadastro_realizado = False
if 'dados_cliente' not in st.session_state:
    st.session_state.dados_cliente = {}

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  INTERFACE DO FORMULÁRIO (VISÃO DO CLIENTE FINAL)                     ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if not st.session_state.cadastro_realizado:
    with st.form("onboarding_form", clear_on_submit=False):
        st.markdown("<h3>1. Dados da Empresa</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            cnpj = st.text_input("CNPJ *", placeholder="00.000.000/0000-00")
        with col2:
            razao_social = st.text_input("Razão Social *", placeholder="Sua Empresa LTDA")
            
        col3, col4 = st.columns(2)
        with col3:
            telefone = st.text_input("WhatsApp do Gestor", placeholder="(00) 00000-0000")
        with col4:
            email = st.text_input("E-mail Financeiro", placeholder="financeiro@empresa.com")

        st.markdown("<h3>2. Perfil Operacional</h3>", unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        with col5:
            regime = st.selectbox("Regime Tributário", ["Selecione...", "Simples Nacional", "Lucro Presumido", "Lucro Real"])
            erp_atual = st.selectbox("Sistema de Gestão Atual (ERP)", ["Nenhum / Excel", "Conta Azul", "Omie", "Nibo", "Bling", "Outro"])
        with col6:
            faturamento = st.selectbox("Faturamento Médio Mensal", ["Selecione...", "Até R$ 20.000", "R$ 20.001 a R$ 100.000", "R$ 100.001 a R$ 500.000", "Acima de R$ 500.000"])
            volume_notas = st.number_input("Volume médio de NFs emitidas/mês", min_value=0, step=10)

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("Finalizar Credenciamento")

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  LÓGICA DE PROCESSAMENTO E SIMULAÇÃO DE BANCO                         ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    if submit:
        if not cnpj or not razao_social or regime == "Selecione..." or faturamento == "Selecione...":
            st.error("⚠️ Por favor, preencha os campos obrigatórios (CNPJ, Razão Social, Regime e Faturamento).")
        else:
            with st.spinner("Estruturando dados e validando informações..."):
                time.sleep(2) # Simula o processamento/API
                
                # Salvando os dados no session_state
                st.session_state.dados_cliente = {
                    "cnpj": cnpj,
                    "razao": razao_social,
                    "faturamento": faturamento,
                    "erp": erp_atual,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
                st.session_state.cadastro_realizado = True
                st.rerun()

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  TELA DE SUCESSO E VISÃO INTERNA DO ESCRITÓRIO                        ║
# ╚═══════════════════════════════════════════════════════════════════════╝
else:
    st.success(f"✅ Credenciamento finalizado com sucesso! Nossa equipe analisará seus dados e entrará em contato.")
    st.info("A BSB Contabilidade agradece a confiança. Um consultor enviará os próximos passos no seu WhatsApp.")
    st.balloons()
    
    if st.button("⬅️ Novo Cadastro (Simulação)"):
        st.session_state.cadastro_realizado = False
        st.session_state.dados_cliente = {}
        st.rerun()

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # AQUI ESTÁ O "EASTER EGG" PARA A SUA REUNIÃO:
    # ---------------------------------------------------------
    with st.expander("🔒 VISÃO INTERNA BSB (Mostrar na Reunião)"):
        st.markdown("Isso é o que o escritório recebe após o cliente clicar em enviar:")
        dados = st.session_state.dados_cliente
        
        # Simulação de Motor de Risco (Lógica SQL adaptada para Python)
        risco = "Baixo"
        cor_risco = "green"
        recomendacao = "Fluxo padrão de Onboarding. Integração via API do ERP."
        
        if dados['erp'] == "Nenhum / Excel" and dados['faturamento'] in ["R$ 100.001 a R$ 500.000", "Acima de R$ 500.000"]:
            risco = "CRÍTICO"
            cor_risco = "red"
            recomendacao = "Atenção: Alto volume financeiro sem sistema de gestão. Necessário cobrar taxa extra de setup para organização de passivo."
        elif dados['erp'] == "Nenhum / Excel":
            risco = "Médio"
            cor_risco = "orange"
            recomendacao = "Cliente desestruturado. Necessário implantar Conta Azul ou Omie antes de iniciar o BPO."

        st.markdown(f"""
        **Novo Lead Capturado:** {dados['razao']} ({dados['cnpj']})  
        **Data:** {dados['data']}  
        **Faturamento Declarado:** {dados['faturamento']}  
        **Sistema Atual:** {dados['erp']}  
        
        ---
        ### 🤖 Inteligência de Dados
        Score Operacional: <strong style='color: {cor_risco}'>{risco}</strong>  
        Ação Recomendada pelo Sistema: {recomendacao}
        """, unsafe_allow_html=True)
