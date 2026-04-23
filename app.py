import streamlit as st
import time
import requests
import re
from datetime import datetime
import pandas as pd

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║ CONFIGURAÇÃO                                                         ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.set_page_config(page_title="BSB Contabilidade | Onboarding", page_icon="🏢", layout="centered")

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║ CSS (MANTIDO ORIGINAL)                                               ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.markdown("""<style>
/* SEU CSS COMPLETO AQUI (mantido exatamente igual, não alterei nada) */
</style>""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║ ESTADO                                                              ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'cadastro_realizado' not in st.session_state: st.session_state.cadastro_realizado = False
if 'dados_cliente' not in st.session_state: st.session_state.dados_cliente = {}
if 'erro_validacao' not in st.session_state: st.session_state.erro_validacao = False
if 'doc_method' not in st.session_state: st.session_state.doc_method = None

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║ FUNÇÕES NOVAS                                                       ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def salvar_dados(dados):
    df = pd.DataFrame([dados])
    try:
        df_existente = pd.read_csv("clientes.csv")
        df = pd.concat([df_existente, df], ignore_index=True)
    except:
        pass
    df.to_csv("clientes.csv", index=False)

def calcular_score(dados):
    score = 0

    if dados.get("tipo_cliente") == "Pessoa Jurídica (PJ)":
        if "Acima de R$ 500.000" in dados.get("faturamento", ""):
            score += 50
        if dados.get("regime") == "Lucro Real":
            score += 40
        if dados.get("funcionarios") != "Nenhum (Sócios)":
            score += 20
        if dados.get("debitos") == "Sim":
            score += 30
    else:
        if dados.get("investidor_bolsa_cripto") == "Sim":
            score += 30
        if dados.get("renda_media") == "Acima de R$ 15.000":
            score += 20

    return score

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║ ENVIO PJ                                                            ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def processar_envio_pj():
    if not st.session_state.in_razao or not st.session_state.in_socio_nome or not st.session_state.in_socio_cpf or st.session_state.in_regime == "Selecione..." or not st.session_state.in_lgpd:
        st.session_state.erro_validacao = True
        return

    dados = {
        "tipo_cliente": "Pessoa Jurídica (PJ)",
        "cnpj": st.session_state.in_cnpj,
        "razao_social": st.session_state.in_razao,
        "nome_fantasia": st.session_state.in_fantasia,
        "segmento": st.session_state.in_segmento,
        "whatsapp": st.session_state.in_wpp,
        "email": st.session_state.in_email,
        "socio": st.session_state.in_socio_nome,
        "cpf_socio": st.session_state.in_socio_cpf,
        "cep": st.session_state.in_cep_pj,
        "regime": st.session_state.in_regime,
        "funcionarios": st.session_state.in_func,
        "faturamento": st.session_state.in_fat,
        "erp": st.session_state.in_erp,
        "emite_nota": st.session_state.in_nota,
        "certificado": st.session_state.in_certificado,
        "debitos": st.session_state.in_debitos,
        "contador": st.session_state.in_contador,
        "dor": st.session_state.in_dor,
        "origem": st.session_state.in_origem,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    dados["score"] = calcular_score(dados)
    salvar_dados(dados)

    st.session_state.dados_cliente = dados
    st.session_state.cadastro_realizado = True

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║ ENVIO PF                                                            ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def processar_envio_pf(doc_ok):
    if not st.session_state.in_cpf or not st.session_state.in_nome_pf or st.session_state.in_necessidade == "Selecione..." or not doc_ok or not st.session_state.in_lgpd:
        st.session_state.erro_validacao = True
        return

    dados = {
        "tipo_cliente": "Pessoa Física (PF)",
        "cpf": st.session_state.in_cpf,
        "nome": st.session_state.in_nome_pf,
        "whatsapp": st.session_state.in_wpp_pf,
        "email": st.session_state.in_email_pf,
        "estado_civil": st.session_state.in_estado_civil,
        "dependentes": st.session_state.in_dependentes,
        "profissao": st.session_state.in_prof,
        "renda_media": st.session_state.in_renda_pf,
        "investidor_bolsa_cripto": "Sim" if st.session_state.in_investidor else "Não",
        "bens": st.session_state.in_bens,
        "rendas_extra": st.session_state.in_rendas_extra,
        "declarou_ir": st.session_state.in_ir,
        "necessidade": st.session_state.in_necessidade,
        "origem": st.session_state.in_origem,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    dados["score"] = calcular_score(dados)
    salvar_dados(dados)

    st.session_state.dados_cliente = dados
    st.session_state.cadastro_realizado = True

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║ UI                                                                  ║
# ╚═══════════════════════════════════════════════════════════════════════╝

st.title("🏢 BSB Contabilidade")
st.subheader("Onboarding Inteligente")

perfil = st.radio("Perfil", ["Empresa (PJ)", "Pessoa Física (PF)"])

st.selectbox("Como conheceu a BSB?", ["Google", "Instagram", "Indicação", "Parceiro", "Outro"], key="in_origem")

if perfil == "Empresa (PJ)":

    st.text_input("CNPJ", key="in_cnpj")
    st.text_input("Razão Social *", key="in_razao")
    st.text_input("Nome Fantasia", key="in_fantasia")

    st.selectbox("Segmento", ["Serviços", "Comércio", "Indústria"], key="in_segmento")

    st.text_input("WhatsApp", key="in_wpp")
    st.text_input("Email", key="in_email")

    st.text_input("Sócio Responsável *", key="in_socio_nome")
    st.text_input("CPF Sócio *", key="in_socio_cpf")
    st.text_input("CEP", key="in_cep_pj")

    st.selectbox("Regime *", ["Selecione...", "Simples Nacional", "Lucro Presumido", "Lucro Real"], key="in_regime")
    st.selectbox("Funcionários", ["Nenhum (Sócios)", "1-5", "6+"], key="in_func")
    st.selectbox("Faturamento", ["Até R$20k", "Até R$100k", "Acima R$500k"], key="in_fat")
    st.selectbox("ERP", ["Nenhum", "Conta Azul", "Omie"], key="in_erp")

    st.selectbox("Emite nota?", ["Sim - Serviço", "Sim - Produto", "Não"], key="in_nota")
    st.selectbox("Certificado digital?", ["Sim", "Não", "Não sei"], key="in_certificado")

    st.selectbox("Possui débitos?", ["Não", "Sim", "Não sei"], key="in_debitos")
    st.selectbox("Possui contador?", ["Não", "Sim", "Trocando"], key="in_contador")
    st.text_area("Principal dor", key="in_dor")

    st.checkbox("Aceito LGPD", key="in_lgpd")

    st.button("Finalizar Cadastro", on_click=processar_envio_pj)

else:

    st.text_input("CPF *", key="in_cpf")
    st.text_input("Nome *", key="in_nome_pf")

    st.text_input("WhatsApp", key="in_wpp_pf")
    st.text_input("Email", key="in_email_pf")

    st.selectbox("Estado civil", ["Solteiro", "Casado"], key="in_estado_civil")
    st.selectbox("Dependentes", ["0", "1", "2+"], key="in_dependentes")

    st.text_input("Profissão", key="in_prof")
    st.selectbox("Renda", ["Até 3k", "3k-8k", "8k+"], key="in_renda_pf")

    st.checkbox("Investidor", key="in_investidor")

    st.selectbox("Possui bens?", ["Não", "Sim"], key="in_bens")
    st.selectbox("Renda extra?", ["Não", "Aluguel", "Investimentos"], key="in_rendas_extra")
    st.selectbox("Já declarou IR?", ["Sim", "Não"], key="in_ir")

    st.selectbox("Necessidade *", ["Selecione...", "IRPF", "Abrir empresa"], key="in_necessidade")

    st.checkbox("Documento enviado", key="doc_ok")
    st.checkbox("Aceito LGPD", key="in_lgpd")

    st.button("Finalizar Cadastro", on_click=processar_envio_pf, args=(st.session_state.doc_ok,))

if st.session_state.erro_validacao:
    st.error("Preencha os campos obrigatórios e aceite LGPD.")

if st.session_state.cadastro_realizado:
    st.success("Cadastro realizado com sucesso!")
    st.json(st.session_state.dados_cliente)
